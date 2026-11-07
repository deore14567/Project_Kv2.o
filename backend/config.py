"""
Application configuration module.
Loads environment variables and exposes them as a Settings instance.

This is the LOCAL / OFFLINE version — uses SQLite by default (no cloud DB).
"""
import os
import base64
import hashlib
from typing import Optional

from dotenv import load_dotenv

# Load .env file (created automatically by setup.sh on first run)
# override=True ensures .env values take precedence over any stale
# environment variables that might be set in the shell.
load_dotenv(override=True)


class Settings:
    """Centralized application settings sourced from environment variables."""

    # --- Database -----------------------------------------------------------
    # LOCAL OFFLINE MODE — SQLite file database (default).
    # No cloud database, no internet connection required.
    # The database file is created at ./village_setu.db on first run.
    #
    # If you want PostgreSQL/MySQL instead, set DATABASE_URL in .env:
    #   postgresql+psycopg2://user:pass@host:port/db
    #   mysql+pymysql://user:pass@host:port/db
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./village_setu.db",
    )

    # --- Auth / JWT ---------------------------------------------------------
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me-in-production-please")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))  # 8h

    # --- Bootstrap admin ----------------------------------------------------
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@villagesetu.gov.in")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "Admin@12345")

    # --- File uploads -------------------------------------------------------
    # LOCAL mode — files stored in ./uploads/ folder (or in DB as BLOB).
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_UPLOAD_MB: int = int(os.getenv("MAX_UPLOAD_MB", "5"))

    # --- Encryption (Aadhaar) ----------------------------------------------
    # Fernet key used for reversible encryption of sensitive fields.
    # Auto-generated from a passphrase if not set (for offline convenience).
    ENCRYPTION_KEY: str = os.getenv(
        "ENCRYPTION_KEY",
        # Derive a stable key from a default passphrase — works offline
        # without manual key generation. Replace with a real key for production.
        base64.urlsafe_b64encode(
            hashlib.sha256(b"village-setu-offline-default-key").digest()
        ).decode(),
    )

    # --- CORS ---------------------------------------------------------------
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")

    # --- App meta -----------------------------------------------------------
    APP_NAME: str = os.getenv("APP_NAME", "Village Setu")
    APP_ENV: str = os.getenv("APP_ENV", "local")


settings = Settings()


def ensure_upload_folder() -> None:
    """Create the upload folder if it does not exist."""
    try:
        os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    except OSError:
        pass
