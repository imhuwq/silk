import os
import shutil

import pytest

from silk.file_tools import generate_random_str
from silk.file_tools import generate_random_dir
from silk.file_tools import generate_random_file
from silk.file_tools import generate_random_file_path
from silk.file_tools import touch_file
from silk.file_tools import echo_file


def test_generate_random_str_working():
    str1 = generate_random_str(12)
    assert len(str1) == 12

    str2 = generate_random_str(12)
    assert str1 != str2


def test_generate_random_dir_default():
    with generate_random_dir() as random_dir:
        assert os.path.exists(random_dir)
    assert not os.path.exists(random_dir)
    assert random_dir.startswith("/tmp/")


def test_generate_random_dir_set_parent_dir():
    cur_dir = os.path.abspath(os.path.curdir)
    with generate_random_dir(cur_dir) as random_dir:
        assert os.path.exists(random_dir)
    assert not os.path.exists(random_dir)
    assert random_dir.startswith(cur_dir)


def test_generate_random_dir_no_auto_create():
    with generate_random_dir(auto_create=False) as random_dir:
        assert not os.path.exists(random_dir)


def test_generate_random_dir_auto_delete_but_delete_manually_first():
    with generate_random_dir(auto_delete=True) as random_dir:
        assert os.path.exists(random_dir)
        shutil.rmtree(random_dir)
    assert not os.path.exists(random_dir)


def test_generate_random_dir_no_auto_delete():
    with generate_random_dir(auto_delete=False) as random_dir:
        assert os.path.exists(random_dir)
    assert os.path.exists(random_dir)
    shutil.rmtree(random_dir)


def test_generate_random_file_default():
    with generate_random_file() as f:
        f.write("test")
        assert os.path.exists(f.name)
    assert not os.path.exists(f.name)
    assert f.name.startswith("/tmp/")


def test_generate_random_file_set_parent_dir():
    cur_dir = os.path.abspath(os.path.curdir)
    with generate_random_file(parent=cur_dir) as f:
        f.write("test")
        assert os.path.exists(f.name)
    assert not os.path.exists(f.name)
    assert f.name.startswith(cur_dir)


def test_generate_random_file_auto_delete_but_delete_manually_first():
    with generate_random_file(auto_delete=True) as f:
        assert os.path.exists(f.name)
        os.remove(f.name)
    assert not os.path.exists(f.name)


def test_generate_random_file_no_auto_delete():
    with generate_random_file(auto_delete=False) as f:
        f.write("test")
        assert os.path.exists(f.name)
    assert os.path.exists(f.name)
    os.remove(f.name)


def test_generate_random_file_path_default():
    path1 = generate_random_file_path()
    path2 = generate_random_file_path()
    assert path1 != path2
    assert path1.startswith("/tmp/")
    assert not os.path.exists(path1)
    assert not os.path.exists(path2)


def test_generate_random_file_path_set_parent():
    cur_dir = os.path.abspath(os.path.curdir)
    path = generate_random_file_path(cur_dir)
    assert not os.path.exists(path)
    assert path.startswith(cur_dir)


def test_touch_file_default():
    file_path = generate_random_file_path()
    assert touch_file(file_path)
    assert os.path.exists(file_path)
    assert not touch_file(file_path)  # 文件已存在
    os.remove(file_path)


def test_touch_file_in_none_exist_dir_will_raise():
    parent = generate_random_str(12)
    file_path = generate_random_file_path(parent)
    with pytest.raises(FileNotFoundError):
        touch_file(file_path)


def test_echo_file_in_none_exist_dir_will_raise():
    parent = generate_random_str(12)
    file_path = generate_random_file_path(parent)
    with pytest.raises(FileNotFoundError):
        echo_file("test", ">", file_path)


def test_echo_file_in_truncate_mode():
    file_path = generate_random_file_path()
    echo_file("testA", ">", file_path)
    echo_file("testB", ">", file_path)
    with open(file_path, "r") as f:
        assert f.read() == "testB"


def test_echo_file_in_append_mode():
    file_path = generate_random_file_path()
    echo_file("testA", ">>", file_path)
    echo_file("testB", ">>", file_path)
    with open(file_path, "r") as f:
        assert f.read() == "testAtestB"
