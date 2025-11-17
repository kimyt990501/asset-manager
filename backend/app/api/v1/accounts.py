from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.api.deps import get_db
from app.services.account_service import AccountService
from app.core.exceptions import AccountNotFoundError, InsufficientBalanceError

router = APIRouter()

@router.get("/", response_model=List[schemas.Account])
def get_accounts(db: Session = Depends(get_db)):
    """모든 계좌 조회"""
    service = AccountService(db)
    return service.get_all_accounts()

@router.get("/{account_id}", response_model=schemas.Account)
def get_account(account_id: int, db: Session = Depends(get_db)):
    """특정 계좌 조회"""
    service = AccountService(db)
    try:
        return service.get_account(account_id)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=schemas.Account, status_code=status.HTTP_201_CREATED)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    """새 계좌 생성"""
    service = AccountService(db)
    return service.create_account(account)

@router.patch("/{account_id}", response_model=schemas.Account)
def update_account(
    account_id: int,
    account_update: schemas.AccountUpdate,
    db: Session = Depends(get_db)
):
    """계좌 정보 수정"""
    service = AccountService(db)
    try:
        return service.update_account(account_id, account_update)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    """계좌 삭제"""
    service = AccountService(db)
    try:
        service.delete_account(account_id)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InsufficientBalanceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
