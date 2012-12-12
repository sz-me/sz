def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except Exception:
        return default
