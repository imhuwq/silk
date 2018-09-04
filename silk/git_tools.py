import os
import random
import weakref
from copy import deepcopy
from typing import Dict

import subprocess
from subprocess import check_output
from subprocess import CalledProcessError

from fabric.api import local
from silk.file_tools import touch_file
from silk.python_hooks import atexit
from silk.python_hooks import atexcp


class GitProject:
    __names = list()
    __max_index = 65536
    instances = dict()

    def __init__(self, name: str, url: str, path: str, is_submodule: bool = False):
        if name in self.__names:
            raise Exception("已经存在同名 {0} 的项目了".format(name))

        self.name = name
        self.url = url
        self.__path = path
        self.__index_record_dir = os.path.join(self.__path, ".index")
        self.__working_index = 0
        self.is_submodule = is_submodule
        self.__submodules = dict()
        self.__names.append(name)

        self.__select_working_index()
        self.instances[name] = weakref.ref(self)

    def add_submodule(self, name: str, url: str, relative_path: str) -> "GitProject":
        if self.__submodules.get(name, None):
            raise Exception("{0} 已经存在同名的 submodule".format(self.name))
        sub_module = GitProject(name, url, os.path.abspath(os.path.join(self.path, relative_path)), is_submodule=True)
        self.__submodules[name] = sub_module
        return sub_module

    @property
    def submodules(self) -> Dict[str, "GitProject"]:
        return deepcopy(self.__submodules)

    def __select_working_index(self):
        if self.is_submodule:
            return
        for index in range(0, self.__max_index):
            busy_flag = os.path.join(self.__index_record_dir, str(index))
            if not os.path.exists(busy_flag):
                touch_file(busy_flag, create_parents=True)
                self.__working_index = index
                return

    def __unselect_working_index(self):
        if self.is_submodule:
            return
        busy_flag = os.path.join(self.__index_record_dir, str(self.__working_index))
        if os.path.exists(busy_flag):
            os.remove(busy_flag)

    @property
    def path(self):
        if self.is_submodule:
            return self.__path
        return os.path.join(self.__path, str(self.__working_index))

    def __clone_project(self):
        if not os.path.exists(self.path):
            local("mkdir -p {0}".format(os.path.dirname(self.path)))
            local("git clone {0} {1}".format(self.url, self.path))
        if not os.path.exists(os.path.join(self.path, ".git")):
            tmp_dir = "/tmp/git_temp_clone"
            local("mkdir -p {0}".format(tmp_dir))
            tmp_path = os.path.join(tmp_dir, str(random.randint(0, 100)))
            local("git clone {0} {1}".format(self.url, tmp_path))
            local("mv {0}/.git {1}/.git".format(tmp_path, self.path))
            local("cd {0} && git add . && git checkout -f".format(self.path))
            local("rm -rf {0}".format(tmp_path))

    def clone_project(self, clone_submodules: bool = False) -> "GitProject":
        self.__clone_project()
        if clone_submodules:
            for submodule in self.submodules.values():
                submodule.__clone_project()
        return self

    def get_commit_hash(self, commit_ref: str = None, length: int = 0) -> str:
        if commit_ref:
            self.fetch_commit_ref(commit_ref)
        result = check_output("cd {0} && git rev-parse HEAD".format(self.path, commit_ref), shell=True, stderr=subprocess.DEVNULL)
        result = result.decode().strip("\n")
        return result[:length] if length else result

    def check_is_branch(self, commit_ref: str) -> bool:
        try:
            check_output("cd {0} && git show-ref --verify refs/heads/{1}".format(self.path, commit_ref), shell=True, stderr=subprocess.DEVNULL)
        except CalledProcessError:
            return False
        else:
            return True

    def check_is_tag(self, commit_ref: str) -> bool:
        try:
            check_output("cd {0} && git show-ref --verify refs/tags/{1}".format(self.path, commit_ref), shell=True, stderr=subprocess.DEVNULL)
        except CalledProcessError:
            return False
        else:
            return True

    def fetch_commit_ref(self, commit_ref: str):
        local("cd {0} && git add . && git checkout -f && git checkout master".format(self.path))
        if self.check_is_branch(commit_ref):
            if commit_ref == "master":
                local("cd {0} && git fetch origin && git fetch origin --tags && git pull".format(self.path, commit_ref))
            else:
                local("cd {0} && git branch -d {1} && git fetch origin && git fetch origin --tags && git checkout {1}".format(self.path, commit_ref))
        elif self.check_is_tag(commit_ref):
            local("cd {0} && git tag -d {1} && git fetch origin && git fetch origin --tags && git checkout {1}".format(self.path, commit_ref))
        else:
            local("cd {0} && git fetch origin && git fetch origin --tags && git checkout {1}".format(self.path, commit_ref))
        return self.get_commit_hash()

    def get_current_state(self) -> Dict[str, str]:
        result = dict()
        result[self.name] = self.get_commit_hash()
        for dep_name, dep_project in self.__submodules.items():
            if os.path.exists(os.path.join(dep_project.path, ".git")):
                result[dep_name] = dep_project.get_commit_hash()
        return result

    def __del__(self):
        self.__unselect_working_index()

    @staticmethod
    @atexit.register
    @atexcp.register
    def clean_git_projects_state():
        for name, instance_weak_ref in GitProject.instances.items():
            instance = instance_weak_ref()
            if instance:
                instance._GitProject__unselect_working_index()


__all__ = ["GitProject"]
