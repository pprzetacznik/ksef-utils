from os.path import join, dirname
from setuptools import setup, find_packages


def read(fname):
    with open(join(dirname(__file__), fname)) as f:
        return f.read()


setup(
    packages=find_packages(),
    package_data={"": ["*.txt"]},
    install_requires=read("requirements.txt").splitlines(),
)
