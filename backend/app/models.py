from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, Date, Enum, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class AccountType(str, enum.Enum):
    checking = "checking"
    savings = "savings"
    investment = "investment"
    cma = "cma"

class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"
    transfer = "transfer"

class CategoryType(str, enum.Enum):
    income = "income"
    expense = "expense"

class Frequency(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1)
    name = Column(String(100), nullable=False)
    type = Column(Enum(AccountType), nullable=False)
    balance = Column(Numeric(15, 2), default=0)
    institution = Column(String(100))
    account_number = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
    recurring_transactions = relationship("RecurringTransaction", back_populates="account", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1)
    name = Column(String(50), nullable=False)
    type = Column(Enum(CategoryType), nullable=False)
    is_fixed = Column(Boolean, default=False) # True for Fixed expenses (e.g., Rent), False for Variable
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    children = relationship("Category", backref="parent", remote_side=[id])
    transactions = relationship("Transaction", back_populates="category")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False) # Changed from String to FK
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    description = Column(Text)
    transaction_date = Column(Date, nullable=False)
    is_recurring = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

class RecurringTransaction(Base):
    __tablename__ = "recurring_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False) # Changed from String to FK
    amount = Column(Numeric(15, 2), nullable=False)
    description = Column(Text)
    frequency = Column(Enum(Frequency), default=Frequency.monthly)
    day_of_month = Column(Integer)
    is_active = Column(Boolean, default=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    account = relationship("Account", back_populates="recurring_transactions")
    category = relationship("Category")

class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    monthly_limit = Column(Numeric(15, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    category = relationship("Category")

class AssetSnapshot(Base):
    __tablename__ = "asset_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1)
    total_assets = Column(Numeric(15, 2), nullable=False)
    net_worth = Column(Numeric(15, 2), nullable=False, default=0) # Added Net Worth
    accounts_summary = Column(JSON)
    snapshot_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

