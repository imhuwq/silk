import os
import shutil
from typing import IO
from typing import Generator
from random import Random
from string import digits
from string import ascii_letters
from contextlib import contextmanager

characters = ascii_letters + digits


def generate_random_str(length: int) -> str:
    selector = Random()
    return "".join(selector.choice(characters) for _ in range(length))


@contextmanager
def generate_random_dir(parent: str = "/tmp", auto_create: bool = True, auto_delete: bool = True) -> Generator[str, None, None]:
    dir_ = os.path.join(parent, generate_random_str(12))
    if auto_create:
        os.makedirs(dir_, exist_ok=True)
    yield dir_
    if auto_create and auto_delete and os.path.exists(dir_):
        try:
            shutil.rmtree(dir_)
        except FileNotFoundError:
            pass


@contextmanager
def generate_random_file(parent: str = "/tmp", auto_delete: bool = True) -> Generator[IO, None, None]:
    file_ = os.path.join(parent, generate_random_str(12))
    os.makedirs(os.path.dirname(file_), exist_ok=True)
    with open(file_, "w") as fd:
        yield fd
    if auto_delete and os.path.exists(file_):
        try:
            os.remove(file_)
        except FileNotFoundError:
            pass


def generate_random_file_path(parent: str = "/tmp") -> str:
    file_ = os.path.join(parent, generate_random_str(12))
    return file_


def touch_file(file_path: str, create_parents=False) -> bool:
    if os.path.exists(file_path):
        return False
    parent_dir = os.path.dirname(file_path)
    if not os.path.exists(parent_dir) and not create_parents:
        raise FileNotFoundError("无法创建文件, 父目录不存在")
    os.makedirs(parent_dir, exist_ok=True)
    f = open(file_path, "w")
    f.close()
    return True


def echo_file(content: str, mode: str, path: str) -> bool:
    if not os.path.exists(os.path.dirname(path)):
        raise FileNotFoundError("无法创建文件或追加内容, 父目录不存在")
    open_mode = "w" if mode == ">" else "a"
    with open(path, open_mode) as f:
        f.write(content)
    return True


__all__ = ["generate_random_str",
           "generate_random_dir",
           "generate_random_file",
           "generate_random_file_path",
           "touch_file",
           "echo_file"]
