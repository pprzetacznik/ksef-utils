from os import getenv
from os.path import join
from pytz import timezone
from ksef_utils.utils import readfile


class Config:
    TIMEZONE = timezone("Europe/Warsaw")
    KSEF_TOKEN = getenv("KSEF_TOKEN")
    KSEF_NIP = getenv("KSEF_NIP")
    PUBLIC_KEY = readfile(join("cert", "pem"))
    KSEF_SIGN_CERT_PATH = getenv("KSEF_SIGN_CERT_PATH")
    KSEF_SIGN_KEY_PATH = getenv("KSEF_SIGN_KEY_PATH")
    KSEF_SIGN_CA_PATH = getenv("KSEF_SIGN_CA_PATH")


class ProdConfig(Config):
    URL = "https://ksef.mf.gov.pl"


class DemoConfig(Config):
    URL = "https://ksef-demo.mf.gov.pl"


class TestConfig(Config):
    URL = "https://ksef-test.mf.gov.pl"
