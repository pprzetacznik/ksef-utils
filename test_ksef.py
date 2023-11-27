from time import sleep
from json import dumps
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


# @mark.skip
def test_get_invoice(server, service, config):
    response = service.init_session()
    response = server.get_invoices(service.init_token)
    print(dumps(response.json(), indent=4))
    print(response.status_code)


@mark.skip
def test_get_session(service, server, config):
    response = service.init_session()
    response = server.get_status(service.init_token)
    print(dumps(response.json(), indent=4))


@mark.skip
def test_auth(config, server):
    response = server.generate_token()
    print(response)


@mark.skip
def test_init_session(config, service):
    response = service.init_session()
    print(dumps(response, indent=4))


@mark.skip
def test_send_invoice(config, service):
    response = service.init_session()
    print(dumps(response, indent=4))
    response_send_invoice = service.send_invoice(
        vendor1={
            "nip": config.KSEF_NIP,
            "name": "Markosoft-owner Krakow Sp.z o.o.",
            "address1": "ul. Bracka 11/12",
            "address2": "40-100 Krakow",
            "country_code": "PL",
        },
        vendor2={
            "nip": 2222222222,
            "name": "Markosoft3 Krakow Sp.z o.o.",
            "address1": "ul. Bracka 11/12",
            "address2": "40-100 Krakow",
            "country_code": "PL",
        },
        invoice={"creation_date": "2023-11-24T15:19:25Z"},
    )
    print(response_send_invoice.status_code)
    print(dumps(response_send_invoice.json(), indent=4))

    reference_number = response_send_invoice.json().get(
        "elementReferenceNumber"
    )
    invoice_status = {}
    while not invoice_status:
        response = service.get_invoice_status(reference_number)
        print(response.status_code)
        print(dumps(response.json(), indent=4))
        invoice_status = response.json().get("invoiceStatus")
        if not invoice_status.get("ksefReferenceNumber"):
            invoice_status = {}
        if not invoice_status:
            sleep(1)

    invoice = service.get_invoice(invoice_status.get("ksefReferenceNumber"))
    print(invoice)
