import os
import json
import base64
from django.conf import settings
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad


def load_icici_public_key():
    cert_path = os.path.join(settings.BASE_DIR, "certs", "icici_public.pem")
    with open(cert_path, "rb") as f:
        key = RSA.import_key(f.read())
    return key


def hybrid_encrypt(payload_dict):
    """
    Implements:
    1. Generate 16-byte session key
    2. Encrypt session key with RSA
    3. Encrypt payload with AES
    4. Return encryptedKey, iv, encryptedData
    """

    # Convert payload to JSON string
    payload = json.dumps(payload_dict)

    # 1️⃣ Generate 16-byte random session key
    session_key = get_random_bytes(16)

    # 2️⃣ Encrypt session key using ICICI public key (RSA)
    public_key = load_icici_public_key()
    cipher_rsa = PKCS1_v1_5.new(public_key)
    encrypted_key = cipher_rsa.encrypt(session_key)
    encrypted_key_b64 = base64.b64encode(encrypted_key).decode()

    # 3️⃣ AES Encryption (CBC mode)
    iv = get_random_bytes(16)
    cipher_aes = AES.new(session_key, AES.MODE_CBC, iv)
    encrypted_data = cipher_aes.encrypt(pad(payload.encode(), AES.block_size))
    encrypted_data_b64 = base64.b64encode(encrypted_data).decode()

    iv_b64 = base64.b64encode(iv).decode()

    return {
        "encryptedKey": encrypted_key_b64,
        "iv": iv_b64,
        "encryptedData": encrypted_data_b64
    }

from Crypto.Util.Padding import unpad


def load_private_key():
    private_key_path = os.path.join(settings.BASE_DIR, "private.pem")
    with open(private_key_path, "rb") as f:
        key = RSA.import_key(f.read())
    return key


def hybrid_decrypt(encrypted_key_b64, iv_b64, encrypted_data_b64):
    """
    1. Decrypt encryptedKey using RSA private key
    2. Use decrypted session key to AES decrypt encryptedData
    """

    # Decode from base64
    encrypted_key = base64.b64decode(encrypted_key_b64)
    iv = base64.b64decode(iv_b64)
    encrypted_data = base64.b64decode(encrypted_data_b64)

    # Decrypt session key using private key
    private_key = load_private_key()
    cipher_rsa = PKCS1_v1_5.new(private_key)
    session_key = cipher_rsa.decrypt(encrypted_key, None)

    # Decrypt AES payload
    cipher_aes = AES.new(session_key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher_aes.decrypt(encrypted_data), AES.block_size)

    return json.loads(decrypted_data.decode())
