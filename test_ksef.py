from json import dumps
from os import getenv
from server import KSEFServer, KSEFUtils
from config import TestConfig, DemoConfig, ProdConfig
from pytest import fixture
from pytest import mark


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


# /openapi/gtw/svc/api/KSeF-common.yaml
# /openapi/gtw/svc/api/KSeF-batch.yaml
# /openapi/gtw/svc/api/KSeF-online.yaml

# from k_se_f_client import AuthenticatedClient
#
#
# client = AuthenticatedClient(
#     base_url=TestConfig().URL,
#     # token="SuperSecretToken",
#     verify_ssl=".cert/pem",
# )


# data = {
#     "timestamp": "2023-10-22T00:00:00+00:00",
#     "queryCriteria": {
#         "subjectType": "subject2",
#         "type": "range",
#         "invoicingDateFrom": "2023-01-01T00:00:00",
#         "invoicingDateTo": "2023-10-20T12:00:00",
#     },
# }


@mark.skip
def test_get_invoice(server, config):
    response = server.get_invoices()
    print(response.json)
    print(dir(response))
    print(response.text)
    print(response.reason)


@mark.skip
def test_get_session(server, config):
    response = server.get_status()
    print(response.json)
    print(dir(response))
    print(response.text)
    print(response.reason)


def test_auth(config, server):
    response = server.generate_token()
    print(response)

    response_json = server.authorization_challenge()
    # challenge = response.json.get("challenge")
    # print(f"challenge: {challenge}")
    # print(response.json["challenge"])
    print(response_json.get("challenge"))

    challenge = response_json.get("challenge")
    encrypted_token = KSEFUtils.get_encrypted_token(
        response_json, config.PUBLIC_KEY, config.KSEF_TOKEN
    )
    print(f"encrypted_token: {encrypted_token}")

    response = server.init_token(
        challenge=challenge, token=encrypted_token, nip=config.KSEF_NIP
    )
    print(type(response.json()))
    print(dir(response))
    print(response.text)
    print(response.status_code)
    print(response.reason)
    print(dumps(response.json(), indent=4))
