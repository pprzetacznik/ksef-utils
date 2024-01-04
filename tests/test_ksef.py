from datetime import datetime
from json import dumps
from pytest import mark, fixture
from ksef_utils.utils import format_xml


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
def test_auth(config, service):
    response = service.init_session()
    service.wait_until_logged()
    response = service.generate_token()
    print(response)


@mark.functional
def test_init_session(config, service):
    response = service.init_session()
    print(dumps(response, indent=4))


@mark.functional
def test_send_invoice(service, invoice_data):
    response = service.init_session()
    print(dumps(response, indent=4))
    response_send_invoice = service.send_invoice(**invoice_data)
    print(response_send_invoice.status_code)
    print(dumps(response_send_invoice.json(), indent=4))
    reference_number = response_send_invoice.json().get(
        "elementReferenceNumber"
    )
    response = service.wait_until_invoice(reference_number)
    invoice_status = response.get("invoiceStatus")
    invoice = service.get_invoice(invoice_status.get("ksefReferenceNumber"))
    print(invoice)


@mark.functional
@mark.init_signed
def test_send_invoice_signed(service, invoice_data):
    session_token = service.init_signed()
    print(f"session_token: {session_token}")
    response_send_invoice = service.send_invoice(**invoice_data)
    print(response_send_invoice.status_code)
    print(dumps(response_send_invoice.json(), indent=4))
    reference_number = response_send_invoice.json().get(
        "elementReferenceNumber"
    )
    response = service.wait_until_invoice(reference_number)
    invoice_status = response.get("invoiceStatus")
    invoice = service.get_invoice(invoice_status.get("ksefReferenceNumber"))
    print(invoice)
    response = service.session_terminate()
    print(dumps(response, indent=4))


@mark.current
def test_payment_identifier(config, service):
    service.init_signed()
    response = service.post_payment_identifier()
    print(dumps(response, indent=4))
