from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from app import schemas, models
from app.repositories.account_repository import AccountRepository
from app.core.exceptions import AccountNotFoundError, InsufficientBalanceError

class AccountService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AccountRepository(db)
    
    def get_all_accounts(self, user_id: int = 1) -> List[schemas.Account]:
        accounts = self.repo.get_all(user_id)
        return [schemas.Account.model_validate(acc) for acc in accounts]
    
    def get_account(self, account_id: int) -> schemas.Account:
        account = self.repo.get_by_id(account_id)
        if not account:
            raise AccountNotFoundError(f"Account {account_id} not found")
        return schemas.Account.model_validate(account)
    
    def create_account(self, account: schemas.AccountCreate, user_id: int = 1) -> schemas.Account:
        account_data = account.model_dump()
        account_data['user_id'] = user_id
        
        db_account = self.repo.create(account_data)
        self.db.commit()
        self.db.refresh(db_account)
        
        return schemas.Account.model_validate(db_account)
    
    def update_account(self, account_id: int, account_update: schemas.AccountUpdate) -> schemas.Account:
        db_account = self.repo.get_by_id(account_id)
        if not db_account:
            raise AccountNotFoundError(f"Account {account_id} not found")
        
        update_data = account_update.model_dump(exclude_unset=True)
        updated_account = self.repo.update(db_account, update_data)
        
        self.db.commit()
        self.db.refresh(updated_account)
        
        return schemas.Account.model_validate(updated_account)
    
    def delete_account(self, account_id: int) -> bool:
        db_account = self.repo.get_by_id(account_id)
        if not db_account:
            raise AccountNotFoundError(f"Account {account_id} not found")
        
        # 비즈니스 로직: 잔액이 0이 아니면 삭제 불가
        if db_account.balance != 0:
            raise InsufficientBalanceError("Cannot delete account with non-zero balance")
        
        self.repo.delete(db_account)
        self.db.commit()
        return True
    
    def adjust_balance(self, account_id: int, amount: Decimal, operation: str) -> schemas.Account:
        """계좌 잔액 조정 (내부 사용)"""
        db_account = self.repo.get_by_id(account_id)
        if not db_account:
            raise AccountNotFoundError(f"Account {account_id} not found")
        
        if operation == "add":
            db_account.balance += amount
        elif operation == "subtract":
            if db_account.balance < amount:
                raise InsufficientBalanceError("Insufficient balance")
            db_account.balance -= amount
        
        self.db.flush()
        return schemas.Account.model_validate(db_account)

    def calculate_net_worth(self, user_id: int = 1) -> Decimal:
        """순자산 계산 (모든 계좌 잔액 합계)"""
        accounts = self.repo.get_all(user_id)
        total_assets = sum(acc.balance for acc in accounts)
        # 추후 부채(Liabilities)가 추가되면 여기서 차감
        return total_assets

