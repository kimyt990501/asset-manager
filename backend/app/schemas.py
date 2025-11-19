from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import date, datetime
from typing import Optional, List
from app.models import AccountType, TransactionType, Frequency, CategoryType

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    type: CategoryType
    is_fixed: bool = False
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)

# Account Schemas
class AccountBase(BaseModel):
    name: str
    type: AccountType
    institution: Optional[str] = None
    account_number: Optional[str] = None

class AccountCreate(AccountBase):
    balance: Decimal = Decimal("0")

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    balance: Optional[Decimal] = None
    institution: Optional[str] = None
    account_number: Optional[str] = None

class Account(AccountBase):
    id: int
    user_id: int
    balance: Decimal
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Transaction Schemas
class TransactionBase(BaseModel):
    account_id: int
    type: TransactionType
    category: str  # Changed from category_id to match DB schema
    amount: Decimal
    description: Optional[str] = None
    transaction_date: date

class TransactionCreate(TransactionBase):
    is_recurring: bool = False

class Transaction(TransactionBase):
    id: int
    is_recurring: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Recurring Transaction Schemas
class RecurringTransactionBase(BaseModel):
    account_id: int
    type: TransactionType
    category: str  # Changed from category_id to match DB schema
    amount: Decimal
    description: Optional[str] = None
    frequency: Frequency
    day_of_month: Optional[int] = None
    start_date: date
    end_date: Optional[date] = None

class RecurringTransactionCreate(RecurringTransactionBase):
    is_active: bool = True

class RecurringTransactionUpdate(BaseModel):
    amount: Optional[Decimal] = None
    is_active: Optional[bool] = None
    end_date: Optional[date] = None

class RecurringTransaction(RecurringTransactionBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Summary Schemas
class TotalAssets(BaseModel):
    total_balance: Decimal
    account_count: int

class MonthlyExpense(BaseModel):
    category_name: str
    amount: Decimal
    is_fixed: bool

class Summary(BaseModel):
    total_assets: Decimal
    net_worth: Decimal
    monthly_fixed_expenses: Decimal
    monthly_variable_expenses: Decimal
    monthly_income: Decimal
    net_monthly_cashflow: Decimal
    accounts: List[Account]
