from json import dumps
from pytest import fixture
from pytest_bdd import scenario, given, when, then


@scenario("e2e.feature", "End to end")
def test_e2e(config, service):
    pass


@fixture
def testing_context():
    return {}


@given("signed in using cert")
def given_signed_in_cert(config, service):
    session_token = service.init_signed()
    print(f"session_token: {session_token}")


@when("generate token")
def when_generate_token(config, service, testing_context):
    response = service.generate_token()
    print(response)
    print(response.get("authorisationToken"))
    testing_context["authorisationToken"] = response.get("authorisationToken")
    service.wait_until_token(response.get("elementReferenceNumber"))


@then("sign in using token")
def then_sign_in_token(config, service, testing_context):
    print(dumps(testing_context, indent=4))
    config.KSEF_TOKEN = testing_context.get("authorisationToken")
    response = service.init_session()
    print(response)
