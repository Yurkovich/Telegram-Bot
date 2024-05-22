import time
from functools import wraps

def rate_limit(seconds):
    def decorator(func):
        last_called = 0

        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal last_called
            current_time = time.time()
            if current_time - last_called < seconds:
                await args[0].message.reply_text("Пожалуйста, подождите некоторое время перед отправкой нового запроса.")
                return
            last_called = current_time
            return await func(*args, **kwargs)
        return wrapper
    return decorator