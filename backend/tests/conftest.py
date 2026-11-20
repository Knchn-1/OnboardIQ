import pytest
from pathlib import Path
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.seed_org import seed_organization
from app.db.seed_knowledge import seed_knowledge

TEST_DB_NAME = "onboardiq_test"

@pytest.fixture(scope="session")
def test_db_setup():
    """Create onboardiq_test database, run alembic migrations, seed it, and drop it after tests."""
    admin_engine = create_engine(
        settings.get_database_url(database="postgres"),
        isolation_level="AUTOCOMMIT",
    )
    with admin_engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME} WITH (FORCE)"))
        conn.execute(text(f"CREATE DATABASE {TEST_DB_NAME}"))

    # Run alembic migrations against onboardiq_test
    alembic_cfg = Config("alembic.ini")
    test_db_url = settings.get_database_url(database=TEST_DB_NAME).render_as_string(hide_password=False)
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
    command.upgrade(alembic_cfg, "head")

    test_engine = create_engine(settings.get_database_url(database=TEST_DB_NAME))
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    # Initial seed
    with TestSessionLocal() as session:
        seed_organization(session)
        seed_knowledge(session)

    yield TestSessionLocal

    test_engine.dispose()
    with admin_engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME} WITH (FORCE)"))
    admin_engine.dispose()

@pytest.fixture
def db_session(test_db_setup):
    """Provide a database session for each test function."""
    session = test_db_setup()
    try:
        yield session
    finally:
        session.close()
