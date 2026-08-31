"""
Banking module for Andishkadeh Management & Market.
Specialized banking education module.
Structure:
- data.py      → Curriculum, chapters, lessons, questions
- service.py   → Module services and business logic
- handlers.py  → Telegram handlers and callback routing
"""
from __future__ import annotations
MODULE_ID = "banking"
MODULE_TITLE = "🏦 بانکداری تخصصی"
MODULE_DESCRIPTION = (
    "آموزش تخصصی و کاربردی بانکداری، عملیات بانکی، "
    "قوانین، اعتبارات، ریسک، بانکداری بین‌الملل و "
    "تحولات نوین صنعت بانکداری."
)
__version__ = "1.0.0"
__all__ = [
    "MODULE_ID",
    "MODULE_TITLE",
    "MODULE_DESCRIPTION",
]
