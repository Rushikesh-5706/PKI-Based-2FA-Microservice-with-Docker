import base64
import pyotp
import time

def get_totp_manager(hex_seed: str):
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    return pyotp.TOTP(base32_seed, interval=30, digits=6, digest='sha1')

def generate_code(hex_seed: str):
    totp = get_totp_manager(hex_seed)
    current_time = int(time.time())
    valid_for = 30 - (current_time % 30)
    return totp.now(), valid_for

def verify_code(hex_seed: str, code: str):
    totp = get_totp_manager(hex_seed)
    return totp.verify(code, valid_window=1)
