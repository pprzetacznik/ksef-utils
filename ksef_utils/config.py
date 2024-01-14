from os import getenv
from os.path import join
from pytz import timezone
from ksef_utils.utils import readfile


class Config:
    TIMEZONE = timezone("Europe/Warsaw")
    KSEF_TOKEN = getenv("KSEF_TOKEN")
    KSEF_NIP = getenv("KSEF_NIP")
    KSEF_ID = getenv("KSEF_ID")
    PUBLIC_KEY = readfile(join("cert", "pem"))
    KSEF_SIGN_CERT_PATH = getenv("KSEF_SIGN_CERT_PATH")
    KSEF_SIGN_KEY_PATH = getenv("KSEF_SIGN_KEY_PATH")
    KSEF_SIGN_CA_PATH = getenv("KSEF_SIGN_CA_PATH")
    LOGS_VERBOSE = True


class ProdConfig(Config):
    URL = "https://ksef.mf.gov.pl"
    LOGS_VERBOSE = False


class DemoConfig(Config):
    URL = "https://ksef-demo.mf.gov.pl"


class TestConfig(Config):
    URL = "https://ksef-test.mf.gov.pl"
