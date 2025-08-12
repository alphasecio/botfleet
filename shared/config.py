import os

def get_env(key, default=None, required=False):
    value = os.getenv(key, default)
    if required and (value is None or not value.strip()):
        raise ValueError(f"Missing required environment variable: {key}")
    return value.strip() if isinstance(value, str) else value
