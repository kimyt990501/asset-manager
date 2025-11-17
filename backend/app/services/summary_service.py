from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from typing import List
from app import schemas, models
from app.repositories.account_repository import AccountRepository
from app.repositories.recurring_transaction_repository import RecurringTransactionRepository

class SummaryService:
    def __init__(self, db: Session):
        self.db = db
        self.account_repo = AccountRepository(db)
        self.recurring_repo = RecurringTransactionRepository(db)
    
    def get_total_assets(self, user_id: int = 1) -> Decimal:
        """총 자산 계산"""
        accounts = self.account_repo.get_all(user_id)
        total = sum(acc.balance for acc in accounts)
        return Decimal(str(total))
    
    def get_monthly_fixed_expenses(self, user_id: int = 1) -> Decimal:
        """월 고정 지출 계산"""
        accounts = self.account_repo.get_all(user_id)
        account_ids = [acc.id for acc in accounts]
        
        if not account_ids:
            return Decimal("0")
        
        return self.recurring_repo.get_monthly_sum_by_type(
            account_ids, 
            models.TransactionType.expense
        )
    
    def get_monthly_fixed_income(self, user_id: int = 1) -> Decimal:
        """월 고정 수입 계산"""
        accounts = self.account_repo.get_all(user_id)
        account_ids = [acc.id for acc in accounts]
        
        if not account_ids:
            return Decimal("0")
        
        return self.recurring_repo.get_monthly_sum_by_type(
            account_ids, 
            models.TransactionType.income
        )
    
    def get_full_summary(self, user_id: int = 1) -> schemas.Summary:
        """전체 요약 정보"""
        accounts = self.account_repo.get_all(user_id)
        total_assets = self.get_total_assets(user_id)
        monthly_income = self.get_monthly_fixed_income(user_id)
        monthly_expenses = self.get_monthly_fixed_expenses(user_id)
        
        return schemas.Summary(
            total_assets=total_assets,
            monthly_fixed_expenses=monthly_expenses,
            monthly_fixed_income=monthly_income,
            net_monthly_cashflow=monthly_income - monthly_expenses,
            accounts=[schemas.Account.model_validate(acc) for acc in accounts]
        )
