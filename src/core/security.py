from bcrypt import checkpw, gensalt, hashpw
from cryptography.fernet import Fernet


class Security:
    def __init__(self, secret_key: str) -> None:
        self.cipher = Fernet(secret_key)


    def encrypt(self, data: str | bytes) -> bytes:
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data)


    def decrypt(self, encrypted_data: bytes | str) -> str:
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        return self.cipher.decrypt(encrypted_data).decode()


    def encrypt_passphrase(self, passphrase: str) -> bytes:
        return hashpw(passphrase.encode(), gensalt())


    def check_passphrase(self, passphrase: str, hashed_passphrase: bytes) -> bool:
        return checkpw(passphrase.encode(), hashed_passphrase)
