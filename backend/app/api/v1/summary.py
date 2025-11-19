from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from decimal import Decimal
from app import schemas
from app.api.deps import get_db
from app.services.summary_service import SummaryService

router = APIRouter()

@router.get("/total-assets", response_model=dict)
def get_total_assets(db: Session = Depends(get_db)):
    """총 자산 조회"""
    service = SummaryService(db)
    total = service.get_total_assets()
    return {"total_assets": float(total)}

@router.get("/monthly-expenses", response_model=dict)
def get_monthly_expenses(db: Session = Depends(get_db)):
    """월 고정 지출 조회"""
    service = SummaryService(db)
    expenses = service.get_monthly_fixed_expenses()
    return {"monthly_fixed_expenses": float(expenses)}

@router.get("/monthly-income", response_model=dict)
def get_monthly_income(db: Session = Depends(get_db)):
    """월 고정 수입 조회"""
    service = SummaryService(db)
    income = service.get_monthly_fixed_income()
    return {"monthly_fixed_income": float(income)}

@router.get("/", response_model=schemas.Summary)
def get_full_summary(db: Session = Depends(get_db)):
    """전체 재정 요약"""
    service = SummaryService(db)
    return service.get_full_summary()

@router.get("/net-worth-trend", response_model=dict)
def get_net_worth_trend(months: int = 6, db: Session = Depends(get_db)):
    """순자산 추이 조회"""
    service = SummaryService(db)
    return service.get_net_worth_trend(months=months)
