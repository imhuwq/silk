import os
from fabric.api import env


def __get_gitlab_ci_variable(name):
    return os.environ.get(name, None)


env.__class__.ARTIFACT_DOWNLOAD_ATTEMPTS = property(lambda self: __get_gitlab_ci_variable("ARTIFACT_DOWNLOAD_ATTEMPTS"))

env.__class__.CHAT_INPUT = property(lambda self: __get_gitlab_ci_variable("CHAT_INPUT"))

env.__class__.CHAT_CHANNEL = property(lambda self: __get_gitlab_ci_variable("CHAT_CHANNEL"))

env.__class__.CI = property(lambda self: __get_gitlab_ci_variable("CI"))

env.__class__.CI_COMMIT_REF_NAME = property(lambda self: __get_gitlab_ci_variable("CI_COMMIT_REF_NAME"))

env.__class__.CI_COMMIT_REF_SLUG = property(lambda self: __get_gitlab_ci_variable("CI_COMMIT_REF_SLUG"))

env.__class__.CI_COMMIT_SHA = property(lambda self: __get_gitlab_ci_variable("CI_COMMIT_SHA"))

env.__class__.CI_COMMIT_BEFORE_SHA = property(lambda self: __get_gitlab_ci_variable("CI_COMMIT_BEFORE_SHA"))

env.__class__.CI_COMMIT_TAG = property(lambda self: __get_gitlab_ci_variable("CI_COMMIT_TAG"))

env.__class__.CI_COMMIT_MESSAGE = property(lambda self: __get_gitlab_ci_variable("CI_COMMIT_MESSAGE"))

env.__class__.CI_COMMIT_TITLE = property(lambda self: __get_gitlab_ci_variable("CI_COMMIT_TITLE"))

env.__class__.CI_COMMIT_DESCRIPTION = property(lambda self: __get_gitlab_ci_variable("CI_COMMIT_DESCRIPTION"))

env.__class__.CI_CONFIG_PATH = property(lambda self: __get_gitlab_ci_variable("CI_CONFIG_PATH"))

env.__class__.CI_DEBUG_TRACE = property(lambda self: __get_gitlab_ci_variable("CI_DEBUG_TRACE"))

env.__class__.CI_DEPLOY_USER = property(lambda self: __get_gitlab_ci_variable("CI_DEPLOY_USER"))

env.__class__.CI_DEPLOY_PASSWORD = property(lambda self: __get_gitlab_ci_variable("CI_DEPLOY_PASSWORD"))

env.__class__.CI_DISPOSABLE_ENVIRONMENT = property(lambda self: __get_gitlab_ci_variable("CI_DISPOSABLE_ENVIRONMENT"))

env.__class__.CI_ENVIRONMENT_NAME = property(lambda self: __get_gitlab_ci_variable("CI_ENVIRONMENT_NAME"))

env.__class__.CI_ENVIRONMENT_SLUG = property(lambda self: __get_gitlab_ci_variable("CI_ENVIRONMENT_SLUG"))

env.__class__.CI_ENVIRONMENT_URL = property(lambda self: __get_gitlab_ci_variable("CI_ENVIRONMENT_URL"))

env.__class__.CI_JOB_ID = property(lambda self: __get_gitlab_ci_variable("CI_JOB_ID"))

env.__class__.CI_JOB_MANUAL = property(lambda self: __get_gitlab_ci_variable("CI_JOB_MANUAL"))

env.__class__.CI_JOB_NAME = property(lambda self: __get_gitlab_ci_variable("CI_JOB_NAME"))

env.__class__.CI_JOB_STAGE = property(lambda self: __get_gitlab_ci_variable("CI_JOB_STAGE"))

env.__class__.CI_JOB_TOKEN = property(lambda self: __get_gitlab_ci_variable("CI_JOB_TOKEN"))

env.__class__.CI_JOB_URL = property(lambda self: __get_gitlab_ci_variable("CI_JOB_URL"))

env.__class__.CI_REPOSITORY_URL = property(lambda self: __get_gitlab_ci_variable("CI_REPOSITORY_URL"))

env.__class__.CI_RUNNER_DESCRIPTION = property(lambda self: __get_gitlab_ci_variable("CI_RUNNER_DESCRIPTION"))

env.__class__.CI_RUNNER_ID = property(lambda self: __get_gitlab_ci_variable("CI_RUNNER_ID"))

env.__class__.CI_RUNNER_TAGS = property(lambda self: __get_gitlab_ci_variable("CI_RUNNER_TAGS"))

env.__class__.CI_RUNNER_VERSION = property(lambda self: __get_gitlab_ci_variable("CI_RUNNER_VERSION"))

env.__class__.CI_RUNNER_REVISION = property(lambda self: __get_gitlab_ci_variable("CI_RUNNER_REVISION"))

env.__class__.CI_RUNNER_EXECUTABLE_ARCH = property(lambda self: __get_gitlab_ci_variable("CI_RUNNER_EXECUTABLE_ARCH"))

env.__class__.CI_PIPELINE_ID = property(lambda self: __get_gitlab_ci_variable("CI_PIPELINE_ID"))

env.__class__.CI_PIPELINE_IID = property(lambda self: __get_gitlab_ci_variable("CI_PIPELINE_IID"))

env.__class__.CI_PIPELINE_TRIGGERED = property(lambda self: __get_gitlab_ci_variable("CI_PIPELINE_TRIGGERED"))

env.__class__.CI_PIPELINE_SOURCE = property(lambda self: __get_gitlab_ci_variable("CI_PIPELINE_SOURCE"))

env.__class__.CI_PROJECT_DIR = property(lambda self: __get_gitlab_ci_variable("CI_PROJECT_DIR"))

env.__class__.CI_PROJECT_ID = property(lambda self: __get_gitlab_ci_variable("CI_PROJECT_ID"))

env.__class__.CI_PROJECT_NAME = property(lambda self: __get_gitlab_ci_variable("CI_PROJECT_NAME"))

env.__class__.CI_PROJECT_NAMESPACE = property(lambda self: __get_gitlab_ci_variable("CI_PROJECT_NAMESPACE"))

env.__class__.CI_PROJECT_PATH = property(lambda self: __get_gitlab_ci_variable("CI_PROJECT_PATH"))

env.__class__.CI_PROJECT_PATH_SLUG = property(lambda self: __get_gitlab_ci_variable("CI_PROJECT_PATH_SLUG"))

env.__class__.CI_PIPELINE_URL = property(lambda self: __get_gitlab_ci_variable("CI_PIPELINE_URL"))

env.__class__.CI_PROJECT_URL = property(lambda self: __get_gitlab_ci_variable("CI_PROJECT_URL"))

env.__class__.CI_PROJECT_VISIBILITY = property(lambda self: __get_gitlab_ci_variable("CI_PROJECT_VISIBILITY"))

env.__class__.CI_REGISTRY = property(lambda self: __get_gitlab_ci_variable("CI_REGISTRY"))

env.__class__.CI_REGISTRY_IMAGE = property(lambda self: __get_gitlab_ci_variable("CI_REGISTRY_IMAGE"))

env.__class__.CI_REGISTRY_PASSWORD = property(lambda self: __get_gitlab_ci_variable("CI_REGISTRY_PASSWORD"))

env.__class__.CI_REGISTRY_USER = property(lambda self: __get_gitlab_ci_variable("CI_REGISTRY_USER"))

env.__class__.CI_SERVER = property(lambda self: __get_gitlab_ci_variable("CI_SERVER"))

env.__class__.CI_SERVER_NAME = property(lambda self: __get_gitlab_ci_variable("CI_SERVER_NAME"))

env.__class__.CI_SERVER_REVISION = property(lambda self: __get_gitlab_ci_variable("CI_SERVER_REVISION"))

env.__class__.CI_SERVER_VERSION = property(lambda self: __get_gitlab_ci_variable("CI_SERVER_VERSION"))

env.__class__.CI_SHARED_ENVIRONMENT = property(lambda self: __get_gitlab_ci_variable("CI_SHARED_ENVIRONMENT"))

env.__class__.GET_SOURCES_ATTEMPTS = property(lambda self: __get_gitlab_ci_variable("GET_SOURCES_ATTEMPTS"))

env.__class__.GITLAB_CI = property(lambda self: __get_gitlab_ci_variable("GITLAB_CI"))

env.__class__.GITLAB_USER_EMAIL = property(lambda self: __get_gitlab_ci_variable("GITLAB_USER_EMAIL"))

env.__class__.GITLAB_USER_ID = property(lambda self: __get_gitlab_ci_variable("GITLAB_USER_ID"))

env.__class__.GITLAB_USER_LOGIN = property(lambda self: __get_gitlab_ci_variable("GITLAB_USER_LOGIN"))

env.__class__.GITLAB_USER_NAME = property(lambda self: __get_gitlab_ci_variable("GITLAB_USER_NAME"))

env.__class__.GITLAB_FEATURES = property(lambda self: __get_gitlab_ci_variable("GITLAB_FEATURES"))

env.__class__.RESTORE_CACHE_ATTEMPTS = property(lambda self: __get_gitlab_ci_variable("RESTORE_CACHE_ATTEMPTS"))

__all__ = ["env"]
