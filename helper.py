import os
import sys
from functools import wraps

commands = {}


def register_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    commands[func.__name__] = wrapper

    return wrapper


@register_command
def clean_pyc():
    for top, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".pyc"):
                file = os.path.join(top, file)
                os.remove(file)


if __name__ == '__main__':
    command = sys.argv[1]
    command = commands[command]
    command()
