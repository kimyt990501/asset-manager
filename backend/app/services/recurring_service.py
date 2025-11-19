from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta
from app import schemas, models
from app.repositories.recurring_transaction_repository import RecurringTransactionRepository
from app.repositories.account_repository import AccountRepository
from app.services.transaction_service import TransactionService
from app.core.exceptions import AccountNotFoundError

class RecurringTransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = RecurringTransactionRepository(db)
        self.account_repo = AccountRepository(db)
    
    def get_all_recurring(self, account_id: int = None) -> List[schemas.RecurringTransaction]:
        """모든 활성 정기 거래 조회"""
        recurring_list = self.repo.get_all_active(account_id)
        return [schemas.RecurringTransaction.model_validate(r) for r in recurring_list]
    
    def get_recurring(self, recurring_id: int) -> schemas.RecurringTransaction:
        """특정 정기 거래 조회"""
        recurring = self.repo.get_by_id(recurring_id)
        if not recurring:
            raise AccountNotFoundError(f"Recurring transaction {recurring_id} not found")
        return schemas.RecurringTransaction.model_validate(recurring)
    
    def create_recurring(self, recurring: schemas.RecurringTransactionCreate) -> schemas.RecurringTransaction:
        """정기 거래 생성"""
        # 계좌 존재 확인
        account = self.account_repo.get_by_id(recurring.account_id)
        if not account:
            raise AccountNotFoundError(f"Account {recurring.account_id} not found")
        
        recurring_data = recurring.model_dump()
        db_recurring = self.repo.create(recurring_data)
        
        self.db.commit()
        self.db.refresh(db_recurring)
        
        return schemas.RecurringTransaction.model_validate(db_recurring)
    
    def update_recurring(
        self, 
        recurring_id: int, 
        recurring_update: schemas.RecurringTransactionUpdate
    ) -> schemas.RecurringTransaction:
        """정기 거래 수정"""
        db_recurring = self.repo.get_by_id(recurring_id)
        if not db_recurring:
            raise AccountNotFoundError(f"Recurring transaction {recurring_id} not found")
        
        update_data = recurring_update.model_dump(exclude_unset=True)
        updated_recurring = self.repo.update(db_recurring, update_data)
        
        self.db.commit()
        self.db.refresh(updated_recurring)
        
        return schemas.RecurringTransaction.model_validate(updated_recurring)
    
    def deactivate_recurring(self, recurring_id: int) -> bool:
        """정기 거래 비활성화"""
        db_recurring = self.repo.get_by_id(recurring_id)
        if not db_recurring:
            raise AccountNotFoundError(f"Recurring transaction {recurring_id} not found")
        
        db_recurring.is_active = False
        self.db.commit()
        return True

    
    def delete_recurring(self, recurring_id: int) -> bool:
        """정기 거래 삭제"""
        db_recurring = self.repo.get_by_id(recurring_id)
        if not db_recurring:
            raise AccountNotFoundError(f"Recurring transaction {recurring_id} not found")
        
        self.repo.delete(db_recurring)
        self.db.commit()
        return True
    
    def process_due_recurring_transactions(self, target_date: date = None) -> int:
        """
        오늘(또는 지정 날짜) 실행해야 할 정기 거래를 실제 거래로 생성
        비즈니스 로직: 스케줄러가 매일 실행
        """
        if target_date is None:
            target_date = date.today()
        
        all_recurring = self.repo.get_all_active()
        processed_count = 0
        
        transaction_service = TransactionService(self.db)
        
        for recurring in all_recurring:
            # 월간 거래이고 오늘이 설정된 날짜인 경우
            if recurring.frequency == models.Frequency.monthly:
                if recurring.day_of_month == target_date.day:
                    # 종료일 체크
                    if recurring.end_date and target_date > recurring.end_date:
                        continue
                    
                    # 실제 거래 생성
                    transaction = schemas.TransactionCreate(
                        account_id=recurring.account_id,
                        type=recurring.type,
                        category=recurring.category,
                        amount=recurring.amount,
                        description=f"[자동] {recurring.description or recurring.category}",
                        transaction_date=target_date,
                        is_recurring=True
                    )
                    
                    try:
                        transaction_service.create_transaction(transaction)
                        processed_count += 1
                    except Exception as e:
                        # 로깅 처리 (실제로는 logging 모듈 사용)
                        print(f"Failed to process recurring transaction {recurring.id}: {e}")
        
        return processed_count
