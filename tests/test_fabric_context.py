import os
import pytest
import getpass
import unittest.mock as mock

from silk.fabric_tools.fabric_context import Host
from silk.fabric_tools.fabric_context import Role
from silk.fabric_tools.fabric_context import Environment
from silk.fabric_tools.fabric_context import run_per_host
from silk.fabric_tools.fabric_context import run_per_role
from silk.fabric_tools import env
from silk.fabric_tools import run
from silk.fabric_tools import local
from silk.fabric_tools import sudo
from silk.fabric_tools import exists
from silk.file_tools import generate_random_file_path


def test_create_host():
    host = Host("localhost", "127.0.0.1")
    assert host.name == "localhost"
    assert host.address == "127.0.0.1"
    assert repr(host) == "Host(\"localhost\", \"127.0.0.1\")"


def test_create_role():
    host = Host("localhost", "127.0.0.1")
    role = Role("test", [host])
    assert role.name == "test"
    assert role.hosts == {host}
    assert repr(role) == "Role(\"test\")"


def test_host_role_relationship():
    host1 = Host("host1", "127.0.0.1")
    host2 = Host("host2", "127.0.0.1")

    role1 = Role("role1", [host1, host2])
    role2 = Role("role2", [host2])

    assert host1.has_role(role1)
    assert not host1.has_role(role2)

    assert host2.has_role(role1)
    assert host2.has_role(role2)

    assert role1.has_host(host1)
    assert role1.has_host(host2)

    assert not role2.has_host(host1)
    assert role2.has_host(host2)

    role3 = Role("role3", [])
    role3.add_host(host1)
    host2.add_role(role3)
    assert host1.has_role(role3)
    assert host2.has_role(role3)
    assert role3.has_host(host1)
    assert role3.has_host(host2)


def test_create_environment():
    localhost = Host("localhost", "127.0.0.1")
    test_role = Role("test", [localhost])
    test_env = Environment("test_env", [test_role], aabb="aabb", attr="attr")

    assert Environment.get_environment("test_env") is test_env

    assert test_env.aabb == "aabb"
    assert test_env.attr == "attr"
    with pytest.raises(AttributeError):
        assert test_env.aabb_attr is None

    assert repr(test_env) == "Environment(\"test_env\")"


def test_create_environment_with_duplicate_name_will_raise():
    localhost = Host("localhost", "127.0.0.1")
    test_role = Role("test", [localhost])
    Environment("test_env_dup", [test_role], aabb="aabb", attr="attr")

    with pytest.raises(Exception):
        Environment("test_env_dup", [test_role], aabb="aabb", attr="attr")


def test_environment_are_all_roles():
    host1 = Host("host1", "127.0.0.1")
    host2 = Host("host2", "127.0.0.1")

    role1 = Role("role1", [host1, host2])
    role2 = Role("role2", [host2])

    test_env = Environment("test_env_are_all_roles", [role1, role2])
    assert test_env.are_all_roles([role1, role2])
    assert not test_env.are_all_roles([role1])


def test_finalize_environment():
    host1 = Host("host1", "127.0.0.1")
    host2 = Host("host2", "127.0.0.1")

    role1 = Role("role1", [host1, host2])
    role2 = Role("role2", [host2])

    test_env = Environment("test_env_finalize_environment", [role1, role2])
    Environment.finalize_environment("test_env_finalize_environment")

    roledefs = dict()
    for role in test_env.roles:
        roledefs[role.name] = {"hosts": [host.full_address for host in role.hosts]}
    assert env.roledefs == roledefs


def setup_key():
    pubkey_file = os.path.join(os.path.expanduser("~"), ".ssh/id_rsa.pub")
    if not os.path.exists(pubkey_file):
        local("ssh-keygen -t rsa -N \"\" -f {0}".format(pubkey_file))
    with open(pubkey_file, "r") as f:
        pubkey = f.read()

    auth_file = os.path.join(os.path.expanduser("~"), ".ssh/authorized_keys")
    with open(auth_file, "r") as f:
        auth_keys = f.readlines()

    if not pubkey in auth_keys:
        with open(auth_file, "a") as f:
            f.write("\n")
            f.write(pubkey)

    env.key_filename = os.path.join(os.path.expanduser("~"), ".ssh/id_rsa")


def fab_task():
    file_path = generate_random_file_path()
    run("touch {0}".format(file_path))
    assert exists(file_path)
    run("rm {0}".format(file_path))


def fab_sudo_task():
    file_path = generate_random_file_path()
    sudo("touch {0}".format(file_path))
    assert exists(file_path)
    sudo("rm {0}".format(file_path))


setup_key()
host = Host("host", "127.0.0.1", user=getpass.getuser())
host2 = Host("host2", "localhost", user=getpass.getuser())
role = Role("role", [host, host2])
role2 = Role("role2", [host2])
environment = Environment("test", [role, role2])


def test_run_per_host():
    fab_task_ = run_per_host(fab_task)
    fab_task_("test", "all")


def test_run_per_host_ask_input():
    fab_task_ = run_per_host(inputs=["sudo password:"])(fab_sudo_task)
    with mock.patch("builtins.input", lambda x: os.environ.get("sudo_password")):
        fab_task_("test", "all")


def test_run_per_host_default_input():
    fab_task_ = run_per_host(prompts={"sudo password:": os.environ.get("sudo_password")})(fab_sudo_task)
    fab_task_("test", "all")


def fab_task_for_host2():
    run("ls")
    assert env.host == host2


def test_run_per_host_for_specific_host():
    fab_task_ = run_per_host(fab_task_for_host2)
    fab_task_("test", "host2")


def test_run_per_host_not_provide_env_and_host_will_raise():
    fab_task_ = run_per_host(fab_task)
    with pytest.raises(Exception):
        fab_task_()


def test_run_per_host_provide_more_than_one_position_arg_will_raise():
    with pytest.raises(TypeError):
        fab_task_ = run_per_host(fab_task, "whatever")


def test_run_per_host_first_arg_is_not_callable_will_raise():
    with pytest.raises(TypeError):
        fab_task_ = run_per_host("whatever")


def test_run_per_role():
    fab_task_ = run_per_role(fab_task)
    fab_task_("test", "all")


def test_run_per_role_ask_input():
    fab_task_ = run_per_role(inputs=["sudo password:"])(fab_sudo_task)
    with mock.patch("builtins.input", lambda x: os.environ.get("sudo_password")):
        fab_task_("test", "all")


def test_run_per_role_default_input():
    fab_task_ = run_per_role(prompts={"sudo password:": os.environ.get("sudo_password")})(fab_sudo_task)
    fab_task_("test", "all")


def fab_task_for_role2():
    run("ls")
    assert env.roles == [role2]
    assert not env.for_all_roles


def test_run_per_role_for_specific_role():
    fab_task_ = run_per_role(fab_task_for_role2)
    fab_task_("test", "role2")


def test_run_per_role_not_provide_env_and_role_will_raise():
    fab_task_ = run_per_role(fab_task)
    with pytest.raises(Exception):
        fab_task_()


def test_run_per_role_provide_more_thon_one_position_arg_will_raise():
    with pytest.raises(TypeError):
        fab_task_ = run_per_role(fab_task, "whatever")


def test_run_per_role_first_arg_is_not_callable_will_raise():
    with pytest.raises(TypeError):
        fab_task_ = run_per_role("whatever")


def fab_task_check_environment():
    assert env.environment == environment


def test_env_environment():
    fab_task_ = run_per_host(fab_task_check_environment)
    fab_task_("test", "all")


def fab_task_check_host():
    assert env.host == host


def test_env_host():
    fab_task_ = run_per_host(fab_task_check_host)
    fab_task_("test", "host")


def fab_task_check_roles():
    assert set(env.roles) == {role, role2}
    assert env.for_all_roles


def test_env_roles():
    fab_task_ = run_per_role(fab_task_check_roles)
    fab_task_("test", "all")


def fab_task_check_role2():
    assert set(env.roles) == {role2}
    assert not env.for_all_roles


def test_env_role2():
    fab_task_ = run_per_role(fab_task_check_role2)
    fab_task_("test", "role2")
