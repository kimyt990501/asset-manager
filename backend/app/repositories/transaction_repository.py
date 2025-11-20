from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app import models

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, account_id: Optional[int] = None, limit: int = 100, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[models.Transaction]:
        query = self.db.query(models.Transaction)
        if account_id:
            query = query.filter(models.Transaction.account_id == account_id)
        if start_date:
            query = query.filter(models.Transaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(models.Transaction.transaction_date <= end_date)
        return query.order_by(models.Transaction.transaction_date.desc()).limit(limit).all()
    
    def get_by_id(self, transaction_id: int) -> Optional[models.Transaction]:
        return self.db.query(models.Transaction).filter(
            models.Transaction.id == transaction_id
        ).first()
    
    def get_by_date_range(self, account_id: int, start_date: date, end_date: date) -> List[models.Transaction]:
        return self.db.query(models.Transaction).filter(
            models.Transaction.account_id == account_id,
            models.Transaction.transaction_date >= start_date,
            models.Transaction.transaction_date <= end_date
        ).all()
    
    def create(self, transaction_data: dict) -> models.Transaction:
        db_transaction = models.Transaction(**transaction_data)
        self.db.add(db_transaction)
        self.db.flush()
        return db_transaction

    
    def update(self, transaction: models.Transaction, update_data: dict) -> models.Transaction:
        for key, value in update_data.items():
            if value is not None:
                setattr(transaction, key, value)
        self.db.flush()
        return transaction
    
    def delete(self, transaction: models.Transaction) -> None:
        self.db.delete(transaction)
        self.db.flush()
