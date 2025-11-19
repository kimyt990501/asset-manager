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
            net_worth=total_assets,
            monthly_fixed_expenses=monthly_expenses,
            monthly_variable_expenses=Decimal("0"),
            monthly_income=monthly_income,
            net_monthly_cashflow=monthly_income - monthly_expenses,
            accounts=[schemas.Account.model_validate(acc) for acc in accounts]
        )

    def get_net_worth_trend(self, user_id: int = 1, months: int = 6) -> dict:
        """순자산 추이 조회 (최근 N개월)"""
        # 1. Get snapshots ordered by date desc
        snapshots = self.db.query(models.AssetSnapshot)\
            .filter(models.AssetSnapshot.user_id == user_id)\
            .order_by(models.AssetSnapshot.snapshot_date.desc())\
            .limit(months)\
            .all()
        
        # 2. If no snapshots, return current state as a single point
        if not snapshots:
            current_assets = self.get_total_assets(user_id)
            # For simplicity, we assume liabilities are 0 for now or need a way to calculate them.
            # But get_total_assets only sums account balances (which are assets).
            # If we want true net worth, we need to subtract liabilities.
            # For now, let's assume net_worth ~= total_assets (unless we have liability accounts).
            # Let's check AccountType.
            
            # Create a pseudo-snapshot for today
            from datetime import date
            return {
                "labels": [date.today().strftime("%Y-%m")],
                "data": [float(current_assets)]
            }

        # 3. Process snapshots
        # Reverse to show chronological order
        snapshots.reverse()
        
        labels = [s.snapshot_date.strftime("%Y-%m") for s in snapshots]
        data = [float(s.net_worth) for s in snapshots]
        
        return {
            "labels": labels,
            "data": data
        }
