from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from app import models, schemas

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, user_id: int) -> List[models.Account]:
        return self.db.query(models.Account).filter(
            models.Account.user_id == user_id
        ).all()
    
    def get_by_id(self, account_id: int) -> Optional[models.Account]:
        return self.db.query(models.Account).filter(
            models.Account.id == account_id
        ).first()
    
    def create(self, account_data: dict) -> models.Account:
        db_account = models.Account(**account_data)
        self.db.add(db_account)
        self.db.flush()  # commit은 서비스 레이어에서
        return db_account
    
    def update(self, account: models.Account, update_data: dict) -> models.Account:
        for key, value in update_data.items():
            setattr(account, key, value)
        self.db.flush()
        return account
    
    def delete(self, account: models.Account) -> None:
        self.db.delete(account)
        self.db.flush()
    
    def update_balance(self, account_id: int, amount_delta: Decimal) -> Optional[models.Account]:
        account = self.get_by_id(account_id)
        if account:
            account.balance += amount_delta
            self.db.flush()
        return account
