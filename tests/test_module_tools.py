import os
from silk.module_tools import import_module_from_path

var = 0


def func():
    return 11235813


class A:
    attr = "Class A"


def test_import_module_from_path():
    module = import_module_from_path("module", os.path.abspath(__file__))
    assert module.test_import_module_from_path
    assert module.var == var
    assert module.func() == func()
    assert module.A().attr == A().attr
    assert module.os is os
