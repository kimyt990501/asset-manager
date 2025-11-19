import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from decimal import Decimal

from app.database import Base
from app.models import Account, Category, Transaction, AccountType, TransactionType, CategoryType
from app.services.transaction_service import TransactionService
from app.services.account_service import AccountService
from app.schemas import TransactionCreate, AccountCreate

# Setup in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_monthly_summary(db):
    # 1. Setup Data
    # Create Account
    account = Account(name="Test Bank", type=AccountType.checking, balance=1000)
    db.add(account)
    db.commit()
    db.refresh(account)

    # Create Categories
    cat_salary = Category(name="Salary", type=CategoryType.income, is_fixed=False)
    cat_rent = Category(name="Rent", type=CategoryType.expense, is_fixed=True)
    cat_food = Category(name="Food", type=CategoryType.expense, is_fixed=False)
    db.add_all([cat_salary, cat_rent, cat_food])
    db.commit()

    # Create Transactions via Service (to test logic) or directly (to test query)
    # Let's use Service for creation to test it too, but we need schemas.
    # Actually, let's just insert raw data to test the "Summary" logic specifically.
    
    tx1 = Transaction(
        account_id=account.id,
        category_id=cat_salary.id,
        type=TransactionType.income,
        amount=Decimal(5000),
        transaction_date=date(2023, 11, 5)
    )
    tx2 = Transaction(
        account_id=account.id,
        category_id=cat_rent.id,
        type=TransactionType.expense,
        amount=Decimal(1000),
        transaction_date=date(2023, 11, 10)
    )
    tx3 = Transaction(
        account_id=account.id,
        category_id=cat_food.id,
        type=TransactionType.expense,
        amount=Decimal(500),
        transaction_date=date(2023, 11, 15)
    )
    db.add_all([tx1, tx2, tx3])
    db.commit()

    # 2. Test TransactionService.get_monthly_summary
    service = TransactionService(db)
    summary = service.get_monthly_summary(2023, 11, user_id=1)

    assert summary["income"] == Decimal(5000)
    assert summary["fixed_expenses"] == Decimal(1000)
    assert summary["variable_expenses"] == Decimal(500)
    assert summary["net_cashflow"] == Decimal(3500) # 5000 - 1500

def test_net_worth(db):
    # 1. Setup Data
    acc1 = Account(name="Bank", type=AccountType.checking, balance=1000, user_id=1)
    acc2 = Account(name="Savings", type=AccountType.savings, balance=5000, user_id=1)
    acc3 = Account(name="Other User", type=AccountType.checking, balance=9999, user_id=2)
    db.add_all([acc1, acc2, acc3])
    db.commit()

    # 2. Test AccountService.calculate_net_worth
    service = AccountService(db)
    net_worth = service.calculate_net_worth(user_id=1)

    assert net_worth == Decimal(6000)
