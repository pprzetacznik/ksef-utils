from os import getenv
from os.path import join
import pytz
from ksef_utils.utils import readfile


class Config:
    TIMEZONE = pytz.timezone("Europe/Warsaw")
    KSEF_TOKEN = getenv("KSEF_TOKEN")
    KSEF_NIP = getenv("KSEF_NIP")
    PUBLIC_KEY = readfile(join("cert", "pem"))


class ProdConfig(Config):
    URL = "https://ksef.mf.gov.pl"


class DemoConfig(Config):
    URL = "https://ksef-demo.mf.gov.pl"


class TestConfig(Config):
    URL = "https://ksef-test.mf.gov.pl"
