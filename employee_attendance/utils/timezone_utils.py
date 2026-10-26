"""Timezone-aware date and time helpers."""

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def _timezone(timezone_name: str) -> ZoneInfo:
    try:
        return ZoneInfo(timezone_name)
    except (ZoneInfoNotFoundError, ValueError) as error:
        raise ValueError(f"Unknown timezone: {timezone_name}") from error


def get_current_date_str(timezone_name: str = "Asia/Karachi") -> str:
    return datetime.now(_timezone(timezone_name)).date().isoformat()


def get_current_time(timezone_name: str = "Asia/Karachi") -> datetime:
    return datetime.now(_timezone(timezone_name))
