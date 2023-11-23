from utils import render_init_session
import requests
from utils import (
    encrypt,
    iso_to_milliseconds,
    round_to_nearest_thousand,
)


class KSEFServer:
    def __init__(self, config):
        self.config = config

    def init_token(self, **kwargs):
        rendered_template = render_init_session(**kwargs)
        print(rendered_template)
        s = requests.Session()
        response = s.post(
            f"{self.config.URL}/api/online/Session/InitToken",
            data=rendered_template,
            headers={
                "Content-Type": "application/octet-stream",
                "Accept": "application/json",
            },
        )
        return response

    def get_status(self):
        s = requests.Session()
        response = s.get(
            f"{self.config.URL}/api/online/Session/Status?PageSize=10&PageOffset=0&IncludeDetails=false",
        )
        return response

    def authorization_challenge(self):
        data = {
            "contextIdentifier": {
                "type": "onip",
                "identifier": self.config.KSEF_NIP,
            }
        }
        s = requests.Session()
        response = s.post(
            f"{self.config.URL}/api/online/Session/AuthorisationChallenge?PageSize=10&PageOffset=0&IncludeDetails=false",
            json=data,
        )

        print(type(response.json()))
        print(dir(response))
        print(response.text)
        print(response.reason)

        # challenge = response.json.get("challenge")
        # print(f"challenge: {challenge}")
        # print(response.json["challenge"])
        response_json = response.json()
        return response_json

    def get_invoices(self):
        data = {
            "queryCriteria": {
                "subjectType": "subject1",
                "type": "incremental",
                "acquisitionTimestampThresholdFrom": "2023-10-22T00:00:00+00:00",
                "acquisitionTimestampThresholdTo": "2023-10-22T23:59:59+00:00",
            }
        }
        s = requests.Session()
        response = s.post(
            f"{self.config.URL}/api/online/Query/Invoice/Sync?PageSize=10&PageOffset=0",
            json=data,
        )
        return response

    def generate_token(self):
        data = {
            "generateToken": {
                "credentialsRoleList": [
                    {
                        "roleType": "credentials_read",
                        "roleDescription": "read others credentials",
                    },
                    {
                        "roleType": "credentials_manage",
                        "roleDescription": "read others credentials",
                    },
                    {
                        "roleType": "invoice_write",
                        "roleDescription": "write invoices",
                    },
                ],
                "description": "token_to_grant_acess",
            }
        }
        s = requests.Session()
        response = s.post(
            f"{self.config.URL}/api/online/Credentials/GenerateToken",
            json=data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        return response.json()


class KSEFUtils:
    @staticmethod
    def get_encrypted_token(
        response_json: dict, public_key: str, ksef_token: str
    ) -> str:
        challenge = response_json.get("challenge")
        if not challenge:
            exception = response_json.get("exception")
            print(f"exception: {exception}")

        challenge_time_iso = response_json.get("timestamp")
        challenge_time = iso_to_milliseconds(challenge_time_iso)
        print("challenge_time:  ", challenge_time)

        encrypted_token = encrypt(public_key, ksef_token, str(challenge_time))
        return encrypted_token
