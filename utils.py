from datetime import datetime, timezone
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


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


def round_to_nearest_thousand(milliseconds: int) -> int:
    return round(milliseconds / 1000) * 1000


def render_init_session(**kwargs):
    from jinja2 import (
        Environment,
        PackageLoader,
        select_autoescape,
        FileSystemLoader,
    )
    from os.path import join

    env = Environment(loader=FileSystemLoader("templates"), autoescape=False)
    template = env.get_template("InitSession.xml")
    return template.render(**kwargs)
