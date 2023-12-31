from time import sleep
from datetime import datetime
import json
import base64
import hashlib
import requests
from ksef_utils.utils import (
    render_template,
    encrypt,
    iso_to_milliseconds,
    sign_xml,
)


class KSEFServer:
    def __init__(self, config):
        self.config = config

    def init_token(self, **kwargs):
        rendered_template = render_template("InitSession.xml", **kwargs)
        print(rendered_template)
        response = requests.post(
            f"{self.config.URL}/api/online/Session/InitToken",
            data=rendered_template,
            headers={
                "Content-Type": "application/octet-stream",
                "Accept": "application/json",
            },
        )
        return response

    def init_signed(self, data):
        response = requests.post(
            f"{self.config.URL}/api/online/Session/InitSigned",
            data=data,
            headers={
                "Content-Type": "application/octet-stream",
                "Accept": "application/json",
            },
        )
        return response

    def get_status(self, session_token):
        headers = {
            "accept": "application/json",
            "SessionToken": session_token,
            "Content-Type": "application/json",
        }
        response = requests.get(
            f"{self.config.URL}/api/online/Session/Status?PageSize=10&PageOffset=0&IncludeDetails=true",
            headers=headers,
        )
        return response

    def get_upo(self, session_token, reference_number):
        headers = {
            # "accept": "application/json",
            "accept": "application/vnd.v3+json",
            "SessionToken": session_token,
            "Content-Type": "application/json",
        }
        response = requests.get(
            f"{self.config.URL}/api/common/Status/{reference_number}",
            headers=headers,
        )
        return response

    def authorization_challenge(self):
        data = {
            "contextIdentifier": {
                "type": "onip",
                "identifier": self.config.KSEF_NIP,
            }
        }
        response = requests.post(
            f"{self.config.URL}/api/online/Session/AuthorisationChallenge?PageSize=10&PageOffset=0&IncludeDetails=false",
            json=data,
        )

        print(type(response.json()))
        print(dir(response))
        print(response.text)
        print(response.reason)
        response_json = response.json()
        return response_json

    def get_session_terminate(self, session_token):
        headers = {
            "accept": "application/json",
            "SessionToken": session_token,
            "Content-Type": "application/json",
        }
        response = requests.get(
            f"{self.config.URL}/api/online/Session/Terminate",
            headers=headers,
        )
        return response

    def get_invoices(self, session_token, from_date=None, to_date=None):
        if not from_date:
            from_date = datetime(
                datetime.now().year,
                datetime.now().month,
                1,
                tzinfo=self.config.TIMEZONE,
            )
        if not to_date:
            to_date = datetime.now()
        from_string = from_date.isoformat(timespec="milliseconds")
        to_string = datetime.now(self.config.TIMEZONE).isoformat(
            timespec="milliseconds"
        )
        data = {
            "queryCriteria": {
                "subjectType": "subject1",
                "type": "incremental",
                "acquisitionTimestampThresholdFrom": from_string,
                "acquisitionTimestampThresholdTo": to_string,
            }
        }
        headers = {
            "accept": "application/json",
            "SessionToken": session_token,
            "Content-Type": "application/json",
        }
        response = requests.post(
            f"{self.config.URL}/api/online/Query/Invoice/Sync?PageSize=10&PageOffset=0",
            json=data,
            headers=headers,
        )
        return response

    def generate_token(self, session_token):
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
                "description": "0_ksef-utils_test_token",
            }
        }
        response = requests.post(
            f"{self.config.URL}/api/online/Credentials/GenerateToken",
            json=data,
            headers={
                "Content-Type": "application/json",
                "SessionToken": session_token,
                "Accept": "application/json",
            },
        )
        return response

    def get_token_status(self, session_token, reference_number):
        response = requests.get(
            f"{self.config.URL}/api/online/Credentials/Status/{reference_number}",
            headers={
                "Content-Type": "application/json",
                "SessionToken": session_token,
                "Accept": "application/json",
            },
        )
        return response

    def get_invoice_status(self, reference_number: str, session_token: str):
        headers = {
            "accept": "application/json",
            "SessionToken": session_token,
            "Content-Type": "application/json",
        }
        url = f"{self.config.URL}/api/online/Invoice/Status/{reference_number}"
        response = requests.get(url, headers=headers)
        return response

    def get_invoice(self, reference_number: str, session_token: str):
        headers = {
            "accept": "application/octet-stream",
            "SessionToken": session_token,
        }
        url = f"{self.config.URL}/api/online/Invoice/Get/{reference_number}"
        response = requests.get(url, headers=headers)
        return response

    def send_invoice(self, data: dict, session_token: str):
        url = f"{self.config.URL}/api/online/Invoice/Send"
        headers = {
            "accept": "application/json",
            "SessionToken": session_token,
            "Content-Type": "application/json",
        }
        response = requests.put(url, data=json.dumps(data), headers=headers)
        return response


class KSEFService:
    def __init__(self, server: KSEFServer):
        self.server = server

    def init_session(self):
        response_json = self.server.authorization_challenge()
        challenge = response_json.get("challenge")
        if not challenge:
            print(json.dumps(response_json, indent=4))
            raise Exception(
                response_json.get("exception").get("exceptionDetailList")
            )
        encrypted_token = KSEFUtils.get_encrypted_token(
            response_json,
            self.server.config.PUBLIC_KEY,
            self.server.config.KSEF_TOKEN,
        )
        response = self.server.init_token(
            challenge=challenge,
            token=encrypted_token,
            nip=self.server.config.KSEF_NIP,
        )
        self.init_token = response.json().get("sessionToken").get("token")
        self.init_token_all = response.json()
        return self.init_token

    def init_signed(self):
        response_json = self.server.authorization_challenge()
        challenge = response_json.get("challenge")
        if not challenge:
            print(json.dumps(response_json, indent=4))
            raise Exception(
                response_json.get("exception").get("exceptionDetailList")
            )
        rendered_template = render_template(
            "InitSessionSignedRequest.xml",
            challenge=challenge,
            nip=self.server.config.KSEF_NIP,
        )
        print(rendered_template)
        response_signed = sign_xml(rendered_template, self.server.config)
        print(response_signed)
        response = self.server.init_signed(
            data=response_signed,
        )
        self.init_token = response.json().get("sessionToken").get("token")
        self.init_token_all = response.json()
        return response

    def session_terminate(self):
        response = self.server.get_session_terminate(self.init_token)
        return response.json()

    def wait_until_logged(self):
        logged = False
        while not logged:
            response = self.server.get_status(self.init_token)
            print(json.dumps(response.json(), indent=4))
            if response.json().get("processingCode") == 310:
                logged = True
            sleep(1)

    def send_invoice(self, **kwargs):
        invoice = render_template("invoice_example.xml", **kwargs)
        print(invoice)
        invoice_encoded = invoice.encode("utf-8")
        invoice_hash = {
            "fileSize": len(invoice_encoded),
            "hashSHA": {
                "algorithm": "SHA-256",
                "encoding": "Base64",
                "value": base64.b64encode(
                    hashlib.sha256(invoice_encoded).digest()
                ).decode("utf-8"),
            },
        }
        invoice_payload = {
            "invoiceBody": base64.b64encode(invoice_encoded).decode("utf-8"),
            "type": "plain",
        }
        data = {"invoiceHash": invoice_hash, "invoicePayload": invoice_payload}
        return self.server.send_invoice(data, self.init_token)

    def wait_until_invoice(self, reference_number):
        invoice_status = {}
        while not invoice_status:
            response = self.get_invoice_status(reference_number)
            print(response.status_code)
            print(json.dumps(response.json(), indent=4))
            invoice_status = response.json().get("invoiceStatus")
            if not invoice_status.get("ksefReferenceNumber"):
                invoice_status = {}
            if not invoice_status:
                sleep(1)
        return invoice_status

    def get_invoice_status(self, reference_number: str):
        return self.server.get_invoice_status(
            reference_number, self.init_token
        )

    def get_invoice(self, reference_number: str) -> str:
        response = self.server.get_invoice(reference_number, self.init_token)
        return response.text

    def get_upo(self, reference_number: str) -> str:
        response = self.server.get_upo(self.init_token, reference_number)
        return response.json()

    def generate_token(self):
        response = self.server.generate_token(self.init_token)
        return response.json()

    def wait_until_token(self, element_reference_number):
        response = self.server.get_token_status(
            self.init_token, element_reference_number
        )
        processing_code = 302
        while processing_code != 200:
            response_status = self.server.get_token_status(
                self.init_token, element_reference_number
            )
            processing_code = response_status.json().get("processingCode")
            print(response)
            if processing_code != 200:
                sleep(1)
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
