
def handle_field_error(func):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return None
    return wrap