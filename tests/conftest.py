import logging
from os import getenv
from pytest import fixture
from ksef_utils.server import KSEFServer, KSEFService
from ksef_utils.config import TestConfig, DemoConfig, ProdConfig


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


def debug_requests():
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


debug_requests()
