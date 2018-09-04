import os
import pytest
import shutil

from silk.git_tools import GitProject
from silk.file_tools import touch_file
from silk.file_tools import generate_random_dir

test_git_repo = "https://gitlab.com/imhuwq/test.git"
test_dep_git_repo = "https://gitlab.com/imhuwq/test-dep.git"


def test_create_git_project():
    with generate_random_dir() as test_repo_dir:
        test_repo = GitProject("test", test_git_repo, test_repo_dir)
        assert test_repo.name == "test"
        assert test_repo.url == test_git_repo


def test_create_git_duplicate_will_raise():
    with generate_random_dir() as test_repo_dir:
        with pytest.raises(Exception):
            GitProject("test", test_git_repo, test_repo_dir)


def test_add_submodule():
    with generate_random_dir() as test_repo_dir:
        test_repo = GitProject("repo", test_git_repo, test_repo_dir)
        test_dep_repo = test_repo.add_submodule("repo_dep", test_dep_git_repo, "dep")
        assert test_dep_repo.path == os.path.join(test_repo.path, "dep")
        assert test_dep_repo.url == test_repo.submodules["repo_dep"].url

        with pytest.raises(Exception):
            test_repo.add_submodule("repo_dep", test_dep_git_repo, "dep")


def test_git_clone():
    with generate_random_dir(auto_delete=False) as test_repo_dir:
        test_repo = GitProject("test_repo", test_git_repo, test_repo_dir)
        test_dep_repo = test_repo.add_submodule("test_repo_dep", test_dep_git_repo, "dep")

        test_repo.clone_project()
        test_repo.clone_project(clone_submodules=True)
        assert os.path.exists(os.path.join(test_repo.path, ".git"))
        assert os.path.exists(os.path.join(test_dep_repo.path, ".git"))

        shutil.rmtree(test_repo.path)
        os.makedirs(test_repo.path)
        touch_file(os.path.join(test_repo.path, "aabb"))
        test_repo.clone_project(clone_submodules=True)

        test_repo.get_commit_hash("develop")
        test_repo.fetch_commit_ref("develop")
        test_repo.fetch_commit_ref("master")

        touch_file(os.path.join(test_repo.path, "aabb"))
        test_repo.fetch_commit_ref("v0.0.2")
        test_repo.get_current_state()
