from os.path import join
import subprocess
from enum import Enum
import logging
from datetime import datetime, timezone
from base64 import b64encode
from xml.dom import minidom
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from jinja2 import (
    Environment,
    FileSystemLoader,
)
from lxml import etree
from lxml.etree import tostring
from signxml import XMLSigner, XMLVerifier


def readfile(filename):
    with open(filename) as f:
        return f.read()


def encrypt(public_key_str, token, timestamp: int):
    public_key = RSA.importKey(public_key_str)
    e = public_key.e
    n = public_key.n
    pubkey = RSA.construct((n, e))
    text = f"{token}|{timestamp}"
    print(f"text: {text}")
    cipher = PKCS1_v1_5.new(pubkey)
    encrypted_text = cipher.encrypt(bytes(text, encoding="utf-8"))
    return b64encode(encrypted_text).decode("utf-8")


def iso_to_milliseconds(timestamp: str) -> int:
    dt_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    print(f"dt_obj: {dt_obj}")
    dt_obj_utc = dt_obj.replace(tzinfo=timezone.utc)
    print(f"dt_obj_utc: {dt_obj_utc}")
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    delta = dt_obj_utc - epoch
    milliseconds = int(delta.total_seconds() * 1000)
    return milliseconds


def render_template(template_name, **kwargs):
    env = Environment(loader=FileSystemLoader("templates"), autoescape=False)
    template = env.get_template(template_name)
    return template.render(**kwargs)


def format_xml(input_string):
    return minidom.parseString(input_string).toprettyxml(indent="  ")


def sign_xml(content, config):
    print(content)
    cert = readfile(config.KSEF_SIGN_CERT_PATH)
    key = readfile(config.KSEF_SIGN_KEY_PATH)
    ca = readfile(config.KSEF_SIGN_CA_PATH)

    root = etree.fromstring(content)
    signed_root = XMLSigner().sign(root, key=key, cert=cert)
    print(signed_root)
    verified_data = XMLVerifier().verify(signed_root, x509_cert=ca).signed_xml
    print(verified_data)
    print(tostring(verified_data))
    output = tostring(signed_root).decode()
    return output


def debug_requests():
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


class KSEFUtils:
    class SerialNumberType(Enum):
        NIP = "NIP"
        PESEL = "PESEL"

        def __str__(self):
            return f"{self.value}"

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

    @staticmethod
    def generate_certs(
        serial_number: str,
        serial_number_type: SerialNumberType = SerialNumberType.NIP,
        output_dir: str = "/tmp",
    ) -> str:
        KSEF_SIGN_CERT_PATH = f"{serial_number}-cert.pem"
        KSEF_SIGN_KEY_PATH = f"{serial_number}-privkey.pem"
        KSEF_SIGN_CA_PATH = f"{serial_number}-cert.pem"
        KSEF_SUBJECT = (
            "/CN=Jan Kowalski/SN=Kowalski/GN=Jan/O=Testowa firma"
            "/C=PL/L=Mazowieckie"
            f"/serialNumber={serial_number_type}-{serial_number}"
            f"/description=Jan Kowalski {serial_number_type}-{serial_number}"
        )
        result = subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-nodes",
                "-subj",
                KSEF_SUBJECT,
                "-days",
                "365",
                "-newkey",
                "rsa",
                "-keyout",
                join(output_dir, KSEF_SIGN_KEY_PATH),
                "-out",
                join(output_dir, KSEF_SIGN_CERT_PATH),
            ],
            capture_output=True,
        )
        print(result)
        return {
            "output_dir": output_dir,
            "KSEF_SIGN_CERT_PATH": join(output_dir, KSEF_SIGN_CERT_PATH),
            "KSEF_SIGN_KEY_PATH": join(output_dir, KSEF_SIGN_KEY_PATH),
            "KSEF_SIGN_CA_PATH": join(output_dir, KSEF_SIGN_CA_PATH),
            "serial_number": serial_number,
            "serial_number_type": serial_number_type.value,
        }
