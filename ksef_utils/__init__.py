from os.path import join, dirname
from importlib import metadata
from importlib.metadata import PackageNotFoundError


def read(fname):
    with open(join(dirname(__file__), fname)) as f:
        return f.read()


try:
    __version__ = metadata.version("ksef-utils")
except PackageNotFoundError:
    __version__ = read(join("..", "VERSION")).strip()
