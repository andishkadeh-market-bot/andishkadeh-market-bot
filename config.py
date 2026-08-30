"""
Andishkadeh Management & Market
Central configuration
"""

import os


# =========================
# Telegram
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is not configured."
    )


# =========================
# Application
# =========================

APP_NAME = "Andishkadeh Management & Market"
APP_VERSION = "2.0.0"

DEBUG = os.getenv("DEBUG", "false").lower() == "true"


# =========================
# Database
# =========================

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "database/andishkadeh.db"
)


# =========================
# User / Gamification
# =========================

DEFAULT_POINTS = 0
DEFAULT_LEVEL = 1


# =========================
# Pagination
# =========================

ITEMS_PER_PAGE = 8


# =========================
# Render / Health Server
# =========================

PORT = int(os.getenv("PORT", "10000"))

HEALTH_HOST = "0.0.0.0"
HEALTH_PATH = "/health"


# =========================
# Logging
# =========================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
