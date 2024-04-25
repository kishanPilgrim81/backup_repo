import base64
import hashlib
import hmac
import json
from Crypto.Cipher import AES
from datetime import datetime

class ShopifyMultipass:
    def __init__(self, multipass_secret):
        key_material = hashlib.sha256(multipass_secret.encode("utf-8")).digest()
        self.encryption_key = key_material[:16]
        self.signature_key = key_material[16:]

    def generate_token(self, customer_data):
        customer_data["created_at"] = datetime.utcnow().isoformat()
        plaintext = json.dumps(customer_data).encode("utf-8")

        cipher = AES.new(self.encryption_key, AES.MODE_CBC)
        iv = cipher.iv
        ciphertext = iv + cipher.encrypt(self._pad(plaintext))

        mac = hmac.new(self.signature_key, ciphertext, hashlib.sha256).digest()
        token = base64.urlsafe_b64encode(ciphertext + mac)

        return token.decode("utf-8")

    def _pad(self, s):
        pad_size = 16 - len(s) % 16
        return s + bytes([pad_size] * pad_size)