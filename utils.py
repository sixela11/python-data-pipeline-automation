from datetime import datetime, timedelta

def get_previous_week_range(start_weekday=5):
    """
    Returns start and end datetime for previous full week.
    Default: Saturday (5) → Friday (4)
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
    """
    Safely parse JSON-like fields from API response.
    """
    value = fields.get(key)
    if not value:
        return ""
    try:
        if isinstance(value, str):
            parsed = json.loads(value)
            return parsed[0]["value"]
    except Exception:
        return str(value)
    return str(value)
