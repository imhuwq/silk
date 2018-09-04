from setuptools import setup, find_packages

VERSION = "0.0.1"

setup(
    name="silk",
    version=VERSION,
    author="huweiqiang",
    author_email="huweiqiang@gizmotech.cn",
    packages=find_packages(exclude=["tests"]),
    install_requires=["requests", "fabric3"],
)
