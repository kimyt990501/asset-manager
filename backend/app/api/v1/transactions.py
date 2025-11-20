from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app import schemas
from app.api.deps import get_db
from app.services.transaction_service import TransactionService
from app.core.exceptions import AccountNotFoundError, InvalidTransactionError

router = APIRouter()

@router.get("/", response_model=List[schemas.Transaction])
def get_transactions(
    account_id: Optional[int] = Query(None, description="필터링할 계좌 ID"),
    start_date: Optional[date] = Query(None, description="시작 날짜 (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="종료 날짜 (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000, description="조회할 최대 거래 수"),
    db: Session = Depends(get_db)
):
    """거래 내역 조회"""
    service = TransactionService(db)
    return service.get_transactions(account_id, limit, start_date, end_date)

@router.post("/", response_model=schemas.Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    """새 거래 생성"""
    service = TransactionService(db)
    try:
        return service.create_transaction(transaction)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidTransactionError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int,
    transaction_update: schemas.TransactionUpdate,
    db: Session = Depends(get_db)
):
    """거래 수정 (잔액 자동 조정)"""
    service = TransactionService(db)
    try:
        return service.update_transaction(transaction_id, transaction_update)
    except InvalidTransactionError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    """거래 삭제 (잔액 원복됨)"""
    service = TransactionService(db)
    try:
        service.delete_transaction(transaction_id)
    except InvalidTransactionError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/monthly-spending/{account_id}/{year}/{month}")
def get_monthly_spending(
    account_id: int,
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    """월별 카테고리별 지출 집계"""
    service = TransactionService(db)
    try:
        return service.get_monthly_spending_by_category(account_id, year, month)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
