from json import dumps
from base64 import b64decode
from pytest import fixture
from pytest_bdd import scenario, given, when, then
from ksef_utils.utils import format_xml


@scenario("e2e.feature", "End to end")
def test_e2e(service):
    pass


@fixture
def testing_context():
    return {}


@then("signed in using cert")
@given("signed in using cert")
def given_signed_in_cert(service):
    session_token = service.init_signed()
    print(f"session_token: {session_token}")


@when("generate token")
def when_generate_token(service, testing_context):
    response = service.generate_token()
    print(dumps(response, indent=4))
    print(response.get("authorisationToken"))
    testing_context["authorisationToken"] = response.get("authorisationToken")
    service.wait_until_token(response.get("elementReferenceNumber"))


@then("sign in using token")
def then_sign_in_token(config, service, testing_context):
    print(dumps(testing_context, indent=4))
    config.KSEF_TOKEN = testing_context.get("authorisationToken")
    response = service.init_session()
    print(response)
    response = service.wait_until_logged()


@then("send an invoice")
def then_send_invoice(service, invoice_data, testing_context):
    response_send_invoice = service.send_invoice(**invoice_data)
    print(response_send_invoice.status_code)
    print(dumps(response_send_invoice.json(), indent=4))
    testing_context["invoice_response"] = response_send_invoice.json()
    reference_number = response_send_invoice.json().get(
        "elementReferenceNumber"
    )
    response = service.wait_until_invoice(reference_number)
    invoice_status = response.get("invoiceStatus")
    invoice = service.get_invoice(invoice_status.get("ksefReferenceNumber"))
    print(invoice)
    testing_context["invoice_response"] = response


@then("terminate session")
def then_terminate_session(service):
    response = service.session_terminate()
    print(dumps(response, indent=4))


@then("get upo")
def then_get_upo(service, testing_context):
    response = service.wait_until_upo(
        testing_context["invoice_response"].get("referenceNumber")
    )
    print(format_xml(b64decode(response.get("upo"))))


@then("get invoices")
def then_get_upo(service, testing_context):
    response = service.get_invoices()
    print(dumps(response, indent=4))
    invoices = response.get("invoiceHeaderList")
    if invoices:
        last_invoice_id = invoices[0].get("ksefReferenceNumber")
        print(last_invoice_id)
        invoice = service.get_invoice(last_invoice_id)
        print(format_xml(invoice))
