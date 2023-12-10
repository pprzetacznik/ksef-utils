from time import sleep
from json import dumps
from pytest import mark
from utils import format_xml


@mark.current
@mark.functional
def test_get_invoice(server, service, config):
    response = service.init_session()
    service.wait_until_logged()
    response = server.get_invoices(service.init_token)
    print(dumps(response.json(), indent=4))
    print(response.status_code)
    invoices = response.json().get("invoiceHeaderList")
    if invoices:
        last_invoice_id = invoices[0].get("ksefReferenceNumber")
        print(last_invoice_id)
        invoice = service.get_invoice(last_invoice_id)
        print(format_xml(invoice))


@mark.functional
def test_get_session(service, server, config):
    response = service.init_session()
    response = server.get_status(service.init_token)
    print(dumps(response.json(), indent=4))


@mark.functional
def test_auth(config, server):
    response = server.generate_token()
    print(response)


@mark.functional
def test_init_session(config, service):
    response = service.init_session()
    print(dumps(response, indent=4))


@mark.functional
@mark.e2e
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
