from datetime import datetime
from json import dumps
from pytest import mark, fixture
from ksef_utils.utils import format_xml, KSEFUtils


@mark.functional
def test_get_invoice(service, config):
    response = service.init_session()
    service.wait_until_logged()
    response = service.get_invoices()
    print(dumps(response, indent=4))
    invoices = response.get("invoiceHeaderList")
    if invoices:
        last_invoice_id = invoices[0].get("ksefReferenceNumber")
        print(last_invoice_id)
        invoice = service.get_invoice(last_invoice_id)
        print(format_xml(invoice))


@mark.functional
def test_get_session(service, server, config):
    response = service.init_session()
    response = service.get_status()
    print(dumps(response, indent=4))


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
    service.wait_until_logged()
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


@mark.functional
def test_payment_identifier(config, service):
    service.init_signed()
    response = service.post_payment_identifier()
    print(dumps(response, indent=4))


@mark.current
@mark.functional
def test_context_grant(config, service):
    NIP_TO_GRANT = "2222222239"
    service.init_signed()
    identifier = "0000"
    response = service.get_generate_internal_identifier(identifier)
    print(dumps(response, indent=4))
    internal_identifier = response.get("internalIdentifier")
    response = service.post_credentials_grant(onip=NIP_TO_GRANT)
    print(dumps(response, indent=4))
    response = service.wait_until_token(response.get("elementReferenceNumber"))
    print(dumps(response, indent=4))
    response = service.post_context_grant(
        credentials_identifier=NIP_TO_GRANT,
        credentials_identifier_type="nip",
        context_identifier=internal_identifier,
        context_identifier_type="int",
    )
    print(dumps(response, indent=4))

    response = service.wait_until_token(response.get("elementReferenceNumber"))
    print(dumps(response, indent=4))

    response = service.get_credentials_grant()
    print(dumps(response, indent=4))

    result = KSEFUtils.generate_certs(
        NIP_TO_GRANT, KSEFUtils.SerialNumberType.NIP, output_dir="."
    )
    print(result)
    config.KSEF_NIP = NIP_TO_GRANT
    config.KSEF_SIGN_CERT_PATH = result.get("KSEF_SIGN_CERT_PATH")
    config.KSEF_SIGN_KEY_PATH = result.get("KSEF_SIGN_KEY_PATH")
    config.KSEF_SIGN_CA_PATH = result.get("KSEF_SIGN_CA_PATH")
    service.init_signed()
