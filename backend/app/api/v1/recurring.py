from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app import schemas
from app.api.deps import get_db
from app.services.recurring_service import RecurringTransactionService
from app.core.exceptions import AccountNotFoundError

router = APIRouter()

@router.get("/", response_model=List[schemas.RecurringTransaction])
def get_recurring_transactions(
    account_id: Optional[int] = Query(None, description="필터링할 계좌 ID"),
    db: Session = Depends(get_db)
):
    """정기 거래 목록 조회"""
    service = RecurringTransactionService(db)
    return service.get_all_recurring(account_id)

@router.get("/{recurring_id}", response_model=schemas.RecurringTransaction)
def get_recurring_transaction(
    recurring_id: int,
    db: Session = Depends(get_db)
):
    """특정 정기 거래 조회"""
    service = RecurringTransactionService(db)
    try:
        return service.get_recurring(recurring_id)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=schemas.RecurringTransaction, status_code=status.HTTP_201_CREATED)
def create_recurring_transaction(
    recurring: schemas.RecurringTransactionCreate,
    db: Session = Depends(get_db)
):
    """정기 거래 생성"""
    service = RecurringTransactionService(db)
    try:
        return service.create_recurring(recurring)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch("/{recurring_id}", response_model=schemas.RecurringTransaction)
def update_recurring_transaction(
    recurring_id: int,
    recurring_update: schemas.RecurringTransactionUpdate,
    db: Session = Depends(get_db)
):
    """정기 거래 수정"""
    service = RecurringTransactionService(db)
    try:
        return service.update_recurring(recurring_id, recurring_update)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{recurring_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_recurring_transaction(
    recurring_id: int,
    db: Session = Depends(get_db)
):
    """정기 거래 비활성화"""
    service = RecurringTransactionService(db)
    try:
        service.deactivate_recurring(recurring_id)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{recurring_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recurring_transaction(
    recurring_id: int,
    db: Session = Depends(get_db)
):
    """정기 거래 삭제"""
    service = RecurringTransactionService(db)
    try:
        service.delete_recurring(recurring_id)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/process-due", status_code=status.HTTP_200_OK)
def process_due_transactions(
    target_date: Optional[date] = Query(None, description="처리할 날짜 (기본: 오늘)"),
    db: Session = Depends(get_db)
):
    """
    정기 거래 자동 실행
    스케줄러나 수동으로 호출
    """
    service = RecurringTransactionService(db)
    processed_count = service.process_due_recurring_transactions(target_date)
    return {"processed": processed_count, "date": target_date or date.today()}
