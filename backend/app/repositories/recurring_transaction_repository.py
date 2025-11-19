from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from decimal import Decimal
from app import models

class RecurringTransactionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_active(self, account_id: Optional[int] = None) -> List[models.RecurringTransaction]:
        query = self.db.query(models.RecurringTransaction).filter(
            models.RecurringTransaction.is_active == True
        )
        if account_id:
            query = query.filter(models.RecurringTransaction.account_id == account_id)
        return query.all()
    
    def get_by_id(self, recurring_id: int) -> Optional[models.RecurringTransaction]:
        return self.db.query(models.RecurringTransaction).filter(
            models.RecurringTransaction.id == recurring_id
        ).first()
    
    def create(self, recurring_data: dict) -> models.RecurringTransaction:
        db_recurring = models.RecurringTransaction(**recurring_data)
        self.db.add(db_recurring)
        self.db.flush()
        return db_recurring
    
    def update(self, recurring: models.RecurringTransaction, update_data: dict) -> models.RecurringTransaction:
        for key, value in update_data.items():
            setattr(recurring, key, value)
        self.db.flush()
        return recurring

    
    def delete(self, recurring: models.RecurringTransaction) -> None:
        self.db.delete(recurring)
        self.db.flush()
    
    def get_monthly_sum_by_type(self, account_ids: List[int], transaction_type: models.TransactionType) -> Decimal:
        result = self.db.query(func.sum(models.RecurringTransaction.amount)).filter(
            models.RecurringTransaction.account_id.in_(account_ids),
            models.RecurringTransaction.type == transaction_type,
            models.RecurringTransaction.is_active == True,
            models.RecurringTransaction.frequency == models.Frequency.monthly
        ).scalar()
        return result or Decimal("0")
