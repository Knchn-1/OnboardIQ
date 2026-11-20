"""
Convenience entry point: seed the dev database with organization + knowledge data.

Usage:
    python -m app.db.seed_all
"""
from app.db.session import SessionLocal
from app.db.seed_org import seed_organization
from app.db.seed_knowledge import seed_knowledge


def seed_all() -> None:
    """Run organization and knowledge seeds in one session."""
    with SessionLocal() as session:
        seed_organization(session)
        seed_knowledge(session)


if __name__ == "__main__":
    seed_all()
