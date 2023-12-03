from os import getenv
from pytest import fixture, mark
from server import KSEFServer, KSEFService
from config import TestConfig, DemoConfig, ProdConfig


@fixture
def config():
    env = getenv("KSEF_ENV", "test")
    config_dict = {
        "test": TestConfig,
        "demo": DemoConfig,
        "prod": ProdConfig,
    }
    return config_dict[env]()


@fixture
def server(config):
    return KSEFServer(config)


@fixture
def service(server):
    return KSEFService(server)
