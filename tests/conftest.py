from datetime import datetime
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


@fixture
def invoice_data(config):
    creation_date = datetime.now(config.TIMEZONE).isoformat(
        timespec="milliseconds"
    )
    return {
        "vendor1": {
            "nip": config.KSEF_NIP,
            "name": "KSeF-utils Kraków",
            "address1": "ul. Github 11/12",
            "address2": "40-100 Kraków",
            "country_code": "PL",
            "contact": {
                "email": "test.ksef-utils@test.speedwell.pl",
                "phone": 12121212121212,
            },
            "bank_account": {
                "nr": "PL11111111111111111111111",
                "swift": "KSEFTEST",
                "bank_name": "KSeF Bank",
                "description": "Business account",
                "type": 1,
            },
        },
        "vendor2": {
            "nip": 2222222239,
            "name": "KSeF-utils Kraków",
            "address1": "ul. Github 11/12",
            "address2": "40-100 Kraków",
            "country_code": "PL",
        },
        "invoice": {
            "creation_date": creation_date,
            "currency": "PLN",
            "type": "VAT",
            "number": "FV-2023/12/10",
            "location": "Kraków",
            "date_of_sale": "2023-12-11",
            "services": [
                {
                    "number": "1",
                    "gross_value": "",
                    "net_price": "100",
                    "net_value": "200",
                    "quantity": "2",
                    "title": "Service",
                    "vat": "23",
                    "vat_value": "",
                    "unit": "szt",
                }
            ],
            "total_gross_value": "246",
            "total_value": "200",
            "total_vat_value": "46",
            "payment": {
                "due_date": "2023-12-20",
                "description": "10 days",
                "form": 6,
            },
            "footer_note": "Tests: https://github.com/pprzetacznik/ksef-utils",
        },
    }
