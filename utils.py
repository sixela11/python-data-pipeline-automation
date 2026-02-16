from datetime import datetime, timedelta
import json

def get_previous_week_range(start_weekday=5):
    """
    Returns start and end datetime for previous full week.
    Default: Saturday → Friday
    """
    today = datetime.today()
    days_since_start = (today.weekday() - start_weekday) % 7

    start_date = (today - timedelta(days=days_since_start + 7)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    end_date = (start_date + timedelta(days=6)).replace(
        hour=23, minute=59, second=59, microsecond=999999
    )

    return start_date, end_date


def safe_json(fields, key):
    value = fields.get(key)
    if not value:
        return ""

    try:
        if isinstance(value, str):
            parsed = json.loads(value)
            if isinstance(parsed, list) and parsed:
                return parsed[0].get("value", "")
    except Exception:
        return str(value)

    return str(value)
