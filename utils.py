from datetime import datetime, timezone
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from jinja2 import (
    Environment,
    FileSystemLoader,
)
import xml.dom.minidom


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
    return base64.b64encode(encrypted_text).decode("utf-8")


def iso_to_milliseconds(timestamp: str) -> int:
    dt_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    print(f"dt_obj: {dt_obj}")
    dt_obj = dt_obj.replace(tzinfo=timezone.utc)
    print(f"dt_obj: {dt_obj}")
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    delta = dt_obj - epoch
    milliseconds = int(delta.total_seconds() * 1000)
    return milliseconds


def render_template(template_name, **kwargs):
    env = Environment(loader=FileSystemLoader("templates"), autoescape=False)
    template = env.get_template(template_name)
    return template.render(**kwargs)


def format_xml(input_string):
    return xml.dom.minidom.parseString(input_string).toprettyxml(indent="  ")
