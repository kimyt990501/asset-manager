from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import date
from decimal import Decimal
from app import schemas, models
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.account_repository import AccountRepository
from app.core.exceptions import AccountNotFoundError, InvalidTransactionError

class TransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.transaction_repo = TransactionRepository(db)
        self.account_repo = AccountRepository(db)
    
    def get_transactions(self, account_id: Optional[int] = None, limit: int = 100) -> List[schemas.Transaction]:
        transactions = self.transaction_repo.get_all(account_id, limit)
        return [schemas.Transaction.model_validate(tx) for tx in transactions]
    
    def create_transaction(self, transaction: schemas.TransactionCreate) -> schemas.Transaction:
        # 비즈니스 로직: 계좌 존재 확인
        account = self.account_repo.get_by_id(transaction.account_id)
        if not account:
            raise AccountNotFoundError(f"Account {transaction.account_id} not found")
        
        # 비즈니스 로직: 지출 시 잔액 확인
        if transaction.type == models.TransactionType.expense:
            if account.balance < transaction.amount:
                raise InvalidTransactionError("Insufficient balance for expense")
        
        # 거래 생성
        transaction_data = transaction.model_dump()
        db_transaction = self.transaction_repo.create(transaction_data)
        
        # 비즈니스 로직: 계좌 잔액 업데이트
        if transaction.type == models.TransactionType.income:
            self.account_repo.update_balance(transaction.account_id, transaction.amount)
        elif transaction.type == models.TransactionType.expense:
            self.account_repo.update_balance(transaction.account_id, -transaction.amount)
        
        self.db.commit()
        self.db.refresh(db_transaction)
        
        return schemas.Transaction.model_validate(db_transaction)

    
    def update_transaction(self, transaction_id: int, transaction_update: schemas.TransactionUpdate) -> schemas.Transaction:
        """거래 수정 (잔액 조정 포함)"""
        db_transaction = self.transaction_repo.get_by_id(transaction_id)
        if not db_transaction:
            raise InvalidTransactionError(f"Transaction {transaction_id} not found")
        
        # 기존 거래 정보 저장
        old_amount = db_transaction.amount
        old_type = db_transaction.type
        
        # 거래 정보 업데이트
        update_data = transaction_update.model_dump(exclude_unset=True)
        updated_transaction = self.transaction_repo.update(db_transaction, update_data)
        
        # 금액이나 타입이 변경된 경우 잔액 조정
        if 'amount' in update_data or 'type' in update_data:
            # 기존 거래 롤백
            if old_type == models.TransactionType.income:
                self.account_repo.update_balance(db_transaction.account_id, -old_amount)
            elif old_type == models.TransactionType.expense:
                self.account_repo.update_balance(db_transaction.account_id, old_amount)
            
            # 새 거래 적용
            new_type = updated_transaction.type
            new_amount = updated_transaction.amount
            if new_type == models.TransactionType.income:
                self.account_repo.update_balance(db_transaction.account_id, new_amount)
            elif new_type == models.TransactionType.expense:
                self.account_repo.update_balance(db_transaction.account_id, -new_amount)
        
        self.db.commit()
        self.db.refresh(updated_transaction)
        
        return schemas.Transaction.model_validate(updated_transaction)
    
    def delete_transaction(self, transaction_id: int) -> bool:
        """거래 삭제 및 잔액 롤백"""
        db_transaction = self.transaction_repo.get_by_id(transaction_id)
        if not db_transaction:
            raise InvalidTransactionError(f"Transaction {transaction_id} not found")
        
        # 비즈니스 로직: 잔액 원복
        if db_transaction.type == models.TransactionType.income:
            self.account_repo.update_balance(db_transaction.account_id, -db_transaction.amount)
        elif db_transaction.type == models.TransactionType.expense:
            self.account_repo.update_balance(db_transaction.account_id, db_transaction.amount)
        
        self.transaction_repo.delete(db_transaction)
        self.db.commit()
        return True
    
    def get_monthly_summary(self, year: int, month: int, user_id: int = 1) -> dict:
        """월별 수입/지출(고정/변동) 요약"""
        transactions = self.db.query(models.Transaction).join(models.Category).filter(
            models.Transaction.account.has(user_id=user_id),
            extract('year', models.Transaction.transaction_date) == year,
            extract('month', models.Transaction.transaction_date) == month
        ).all()

        income = Decimal(0)
        fixed_expenses = Decimal(0)
        variable_expenses = Decimal(0)

        for tx in transactions:
            if tx.type == models.TransactionType.income:
                income += tx.amount
            elif tx.type == models.TransactionType.expense:
                if tx.category.is_fixed:
                    fixed_expenses += tx.amount
                else:
                    variable_expenses += tx.amount

        return {
            "income": income,
            "fixed_expenses": fixed_expenses,
            "variable_expenses": variable_expenses,
            "net_cashflow": income - (fixed_expenses + variable_expenses)
        }

