def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except Exception:
        return default


def safe_get(val, func, default=None):
    try:
        return func(val)
    except Exception:
        return default
