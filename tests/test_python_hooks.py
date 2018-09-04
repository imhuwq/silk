import pytest
from silk.python_hooks import atexcp
from silk.python_hooks import atexit


def run_on_exit():
    print("running exiting hook")


def func_exit_0():
    atexit.register(run_on_exit)
    exit(0)


@pytest.mark.xfail(strict=True)
def test_atexit_working():
    func_exit_0()


def run_on_exception():
    print("running exception hook")


def func_raise_exception():
    atexcp.register(run_on_exception)
    raise Exception("Intentionally raised exception")


@pytest.mark.xfail(strict=True)
def test_atexcp_register():
    func_raise_exception()


def test_atexcp_register_twice_will_raise():
    with pytest.raises(Exception) as err:
        atexcp.register(run_on_exception)
        atexcp.register(run_on_exception)
    assert str(err.value) == "已经注册了同名的 exception 函数"


def test_atexcp_unregister():
    atexcp.unregister(run_on_exception)
    assert not atexcp._callbacks.get("func_raise_exception")


if __name__ == '__main__':
    test_atexcp_register()
    test_atexcp_register_twice_will_raise()
    test_atexcp_unregister()
