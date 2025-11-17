from fastapi import APIRouter
from app.api.v1 import accounts, transactions, recurring, summary

api_router = APIRouter()

api_router.include_router(
    accounts.router,
    prefix="/accounts",
    tags=["accounts"]
)

api_router.include_router(
    transactions.router,
    prefix="/transactions",
    tags=["transactions"]
)

api_router.include_router(
    recurring.router,
    prefix="/recurring",
    tags=["recurring-transactions"]
)

api_router.include_router(
    summary.router,
    prefix="/summary",
    tags=["summary"]
)
