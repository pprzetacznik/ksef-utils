from json import dumps
from pytest_bdd import scenario, given, when, then
from ksef_utils.utils import KSEFUtils
from tests.test_e2e import *


@scenario("e2e.feature", "Self-invoicing")
def test_selfinvoicing(service):
    pass


@then("grant context")
def test_context_grant(config, service, testing_context):
    testing_context["NIP_TO_GRANT"] = "2222222239"
    identifier = "0000"
    response = service.get_generate_internal_identifier(identifier)
    print(dumps(response, indent=4))
    internal_identifier = response.get("internalIdentifier")
    response = service.post_credentials_grant(
        onip=testing_context.get("NIP_TO_GRANT")
    )
    print(dumps(response, indent=4))
    response = service.wait_until_token(response.get("elementReferenceNumber"))
    print(dumps(response, indent=4))
    response = service.post_context_grant(
        credentials_identifier=testing_context.get("NIP_TO_GRANT"),
        credentials_identifier_type="nip",
        context_identifier=internal_identifier,
        context_identifier_type="int",
    )
    print(dumps(response, indent=4))

    response = service.wait_until_token(response.get("elementReferenceNumber"))
    print(dumps(response, indent=4))

    response = service.get_credentials_grant()
    print(dumps(response, indent=4))


@then("generate new certs")
def test_generate_new_certs(config, testing_context):
    result = KSEFUtils.generate_certs(
        testing_context.get("NIP_TO_GRANT"),
        KSEFUtils.SerialNumberType.NIP,
        output_dir=".",
    )
    print(result)
    config.KSEF_NIP = testing_context.get("NIP_TO_GRANT")
    config.KSEF_SIGN_CERT_PATH = result.get("KSEF_SIGN_CERT_PATH")
    config.KSEF_SIGN_KEY_PATH = result.get("KSEF_SIGN_KEY_PATH")
    config.KSEF_SIGN_CA_PATH = result.get("KSEF_SIGN_CA_PATH")
