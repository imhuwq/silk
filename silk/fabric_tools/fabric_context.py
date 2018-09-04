import os
from typing import Sequence
from functools import wraps

from silk.fabric_tools import env
from silk.fabric_tools import hosts
from silk.fabric_tools import roles
from silk.fabric_tools import execute
from silk.fabric_tools import parallel


class Host:
    def __init__(self, name: str, address: str, user="deploy"):
        self.name = name
        self.user = user
        self.address = address
        self.full_address = "{0}@{1}".format(self.user, self.address)
        self.roles = set()

    def add_role(self, role: "Role"):
        self.roles.add(role)
        if not role.has_host(self):
            role.add_host(self)

    def has_role(self, role: "Role"):
        return role in self.roles

    def __repr__(self):
        return "Host(\"{0}\", \"{1}\")".format(self.name, self.address)


class Role:
    def __init__(self, name, hosts: Sequence["Host"]):
        self.name = name
        self.hosts = set() if not hosts else set(hosts)
        for host in self.hosts:
            host.add_role(self)

    def add_host(self, host: "Host"):
        self.hosts.add(host)
        if not host.has_role(self):
            host.add_role(self)

    def has_host(self, host: "Host"):
        return host in self.hosts

    def __repr__(self):
        return "Role(\"{0}\")".format(self.name)


class Environment:
    created_environments = dict()

    def __init__(self, name, roles, **options):
        self.name = name
        self.roles = set(roles)
        self.options = options
        self.hosts = set()
        for role in self.roles:
            for host in role.hosts:
                self.hosts.add(host)

        if Environment.created_environments.get(name, None):
            raise Exception("{0} 已经存在".format(self))
        Environment.created_environments[name] = self

    @staticmethod
    def get_environment(name) -> "Environment":
        return Environment.created_environments.get(name, None)

    @staticmethod
    def finalize_environment(name: str) -> dict:
        environment = Environment.get_environment(name)
        roledefs = dict()
        for role in environment.roles:
            roledefs[role.name] = {"hosts": [host.full_address for host in role.hosts]}
        env.roledefs = roledefs
        return roledefs

    def are_all_roles(self, roles):
        return set(roles) == set(self.roles)

    def __getattr__(self, item):
        try:
            return self.__dict__[item]
        except KeyError as e:
            value = self.options.get(item, None)
            if value:
                return value
            raise AttributeError("Class {0} does not have attribute {1}".format(self.__class__.name, item))

    def __repr__(self):
        return "Environment(\"{0}\")".format(self.name)


def run_per_host(*args, inputs: Sequence[str] = None, prompts: dict = None, run_parallel: bool = True):
    def task_runner_decorator(inputs_, prompts_):
        def task_runner_wrapper(task_func):
            @wraps(task_func)
            def task_runner(*args_, **kwargs_):
                if isinstance(prompts_, dict):
                    env.prompts.update(prompts)

                for input_prompt in inputs_:
                    input_value = os.environ.get(input_prompt.split(":")[0], None) or input(input_prompt)
                    env.prompts[input_prompt] = input_value

                if len(args_) < 2:
                    err_msg = "必须提供目标环境和服务器名称, 比如 fab {0}:internal,lvs-028(all)".format(task_func.__name__)
                    raise Exception(err_msg)

                args_ = list(args_)
                environment_name, host_name, *args_ = args_
                environment = Environment.get_environment(environment_name)
                Environment.finalize_environment(environment_name)
                env.environment_name = environment_name

                hosts_ = []
                for host in environment.hosts:
                    if host_name in [host.name, "all"]:
                        hosts_.append(host.full_address)

                hosted_task_func = hosts(*hosts_)(task_func)

                if run_parallel:
                    paralleled_task_func = parallel(hosted_task_func)
                    return execute(paralleled_task_func, *args_, **kwargs_)
                else:
                    return execute(hosted_task_func, *args_, **kwargs_)

            return task_runner

        return task_runner_wrapper

    inputs = inputs or list()
    prompts = prompts or dict()
    if len(args) == 0:
        return task_runner_decorator(inputs, prompts)
    elif len(args) == 1:
        if callable(args[0]):
            return task_runner_decorator(inputs, prompts)(*args)
        raise TypeError("@run_per_host() 的第 1 个 positional argument 必须是 callable")
    else:
        raise TypeError("@run_per_host() 只接受 1 个 positional argument, 实际收到 {0} 个".format(len(args)))


def run_per_role(*args, inputs=None, prompts=None, run_parallel: bool = True):
    def task_runner_decorator(inputs_, prompts_):
        def task_runner_wrapper(task_func):
            @wraps(task_func)
            def task_runner(*args_, **kwargs_):
                if isinstance(prompts_, dict):
                    env.prompts.update(prompts)

                for input_prompt in inputs_:
                    input_value = os.environ.get(input_prompt.split(":")[0], None) or input(input_prompt)
                    env.prompts[input_prompt] = input_value

                if len(args_) < 2:
                    err_msg = "必须提供目标环境和 role 名称, 比如 fab {0}:internal,web(all)".format(task_func.__name__)
                    raise Exception(err_msg)

                args_ = list(args_)
                environment_name, role_name, *args_ = args_
                environment = Environment.get_environment(environment_name)
                Environment.finalize_environment(environment_name)
                env.environment_name = environment_name

                roles_ = []
                for role in environment.roles:
                    if role_name in [role.name, "all"]:
                        roles_.append(role.name)

                roled_task_func = roles(*roles_)(task_func)

                if run_parallel:
                    paralleled_task_func = parallel(roled_task_func)
                    return execute(paralleled_task_func, *args_, **kwargs_)
                else:
                    return execute(roled_task_func, *args_, **kwargs_)

            return task_runner

        return task_runner_wrapper

    inputs = inputs or list()
    prompts = prompts or dict()
    if len(args) == 0:
        return task_runner_decorator(inputs, prompts)
    elif len(args) == 1:
        if callable(args[0]):
            return task_runner_decorator(inputs, prompts)(*args)
        raise TypeError("@run_per_role() 的第 1 个 positional argument 必须是 callable")
    else:
        raise TypeError("@run_per_role() 只接受 1 个 positional argument, 实际收到 {0} 个".format(len(args)))


def get_current_environment(self) -> "Environment":
    environment_name = env.environment_name  # 在 run_per_host 和 run_per_host 里面设置的
    if not environment_name:
        raise RuntimeError("fabric 没有运行在特定 environment 下")
    environment = Environment.get_environment(environment_name)
    return environment


env.__class__.environment = property(get_current_environment)


def get_current_host(self) -> "Host":
    if not env.environment:
        return Host(env.host_string, env.host_string)

    for host in env.environment.hosts:
        if host.full_address == env.host_string:
            return host


env.__class__.host = property(get_current_host)


def get_current_roles(self) -> Sequence["Role"]:
    roles_ = list()
    for role_name in env.effective_roles:
        for role in env.environment.roles:
            if role_name == role.name:
                roles_.append(role)
    return roles_


env.__class__.roles = property(get_current_roles)


def check_current_roles_are_all(self) -> bool:
    roles_ = env.roles
    for role in env.environment.roles:
        if role not in roles_:
            return False
    return True


env.__class__.for_all_roles = property(check_current_roles_are_all)

__all__ = ["Host", "Role", "Environment"]
