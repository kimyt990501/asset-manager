from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
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
            self.account_repo.update_balance(transaction.account_id, float(transaction.amount))
        elif transaction.type == models.TransactionType.expense:
            self.account_repo.update_balance(transaction.account_id, -float(transaction.amount))
        
        self.db.commit()
        self.db.refresh(db_transaction)
        
        return schemas.Transaction.model_validate(db_transaction)
    
    def delete_transaction(self, transaction_id: int) -> bool:
        """거래 삭제 및 잔액 롤백"""
        db_transaction = self.transaction_repo.get_by_id(transaction_id)
        if not db_transaction:
            raise InvalidTransactionError(f"Transaction {transaction_id} not found")
        
        # 비즈니스 로직: 잔액 원복
        if db_transaction.type == models.TransactionType.income:
            self.account_repo.update_balance(db_transaction.account_id, -float(db_transaction.amount))
        elif db_transaction.type == models.TransactionType.expense:
            self.account_repo.update_balance(db_transaction.account_id, float(db_transaction.amount))
        
        self.transaction_repo.delete(db_transaction)
        self.db.commit()
        return True
    
    def get_monthly_spending_by_category(self, account_id: int, year: int, month: int) -> dict:
        """월별 카테고리별 지출 집계 (비즈니스 로직)"""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        transactions = self.transaction_repo.get_by_date_range(account_id, start_date, end_date)
        
        category_totals = {}
        for tx in transactions:
            if tx.type == models.TransactionType.expense:
                category_totals[tx.category] = category_totals.get(tx.category, 0) + float(tx.amount)
        
        return category_totals
