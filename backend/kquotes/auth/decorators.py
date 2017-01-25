from functools import wraps
from django.http import HttpRequest

from .exceptions import LoginNeeded


def login_required(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        request = next((arg for arg in args if isinstance(arg, HttpRequest)), None)

        if not request or not request.user.is_authenticated():
            raise LoginNeeded()

        function(*args, **kwargs)

    return decorator
