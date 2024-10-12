from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from passlib.context import CryptContext
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import hashlib

from app.core.config import settings


class Security:
    def __init__(self):
        # Sử dụng bcrypt để mã hóa mật khẩu
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Hàm mã hóa mật khẩu với bcrypt
    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    # Hàm xác thực mật khẩu
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

        # Hàm mã hóa private key bằng AES

    def encrypt_private_key(self, private_key: str, secret_key: str) -> bytes:
        """Mã hóa chuỗi private_key bằng AES."""
        iv = os.urandom(16)  # Tạo IV ngẫu nhiên 16 byte
        secret_key_bytes = self._get_secret_key_bytes(secret_key)  # Chuyển secret_key thành byte

        # Tạo AES cipher object với IV và secret key
        cipher = Cipher(algorithms.AES(secret_key_bytes), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(private_key.encode()) + encryptor.finalize()  # Mã hóa private_key
        return iv + ct  # Kết hợp IV với ciphertext

        # Hàm giải mã private key bằng AES

    def decrypt_private_key(self, ciphertext: bytes, secret_key: str) -> str:
        """Giải mã chuỗi private_key đã mã hóa bằng AES."""
        iv = ciphertext[:16]  # Tách IV từ dữ liệu mã hóa
        actual_ciphertext = ciphertext[16:]  # Phần còn lại là ciphertext
        secret_key_bytes = self._get_secret_key_bytes(secret_key)  # Chuyển secret_key thành byte

        # Đảm bảo IV phải là chuỗi bytes
        if not isinstance(iv, bytes):
            raise TypeError("Initialization vector must be bytes-like")

        # Tạo AES cipher object với IV và secret key
        cipher = Cipher(algorithms.AES(secret_key_bytes), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_key = decryptor.update(actual_ciphertext) + decryptor.finalize()  # Giải mã ciphertext
        return decrypted_key.decode()  # Trả về chuỗi gốc

        # Hàm phụ trợ để xử lý secret_key và đảm bảo nó có độ dài 16, 24, hoặc 32 byte

    def _get_secret_key_bytes(self, secret_key: str) -> bytes:
        secret_key_bytes = secret_key.encode()  # Chuyển chuỗi secret_key thành bytes
        if len(secret_key_bytes) not in (16, 24, 32):
            # Nếu độ dài không hợp lệ, sử dụng SHA-256 để tạo khóa có độ dài 32 byte
            secret_key_bytes = hashlib.sha256(secret_key_bytes).digest()
        return secret_key_bytes

    def generate_rsa_key_pair(self) -> [str, str]:
        """Sinh ra cặp khóa RSA (khóa công khai và khóa riêng tư)."""

        # Sinh khóa riêng tư với kích thước 2048-bit
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Tạo khóa công khai từ khóa riêng tư
        public_key = private_key.public_key()

        # Xuất khóa riêng tư ở định dạng PEM (chuỗi byte)
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()  # Không sử dụng mật khẩu để mã hóa
        )

        # Xuất khóa công khai ở định dạng PEM (chuỗi byte)
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return private_pem.decode('utf-8'), public_pem.decode('utf-8')


# Hàm giả lập verify token (được sử dụng trong API bảo mật)
def verify_token(token: str):
    return True


# Khởi tạo đối tượng Security
security = Security()

if __name__ == '__main__':

    private_key, public_key = security.generate_rsa_key_pair()
    # Mã hóa private key
    encrypted = security.encrypt_private_key(private_key, settings.MASTER_KEY)
    print("Mã hóa:", encrypted)

    # Giải mã private key
    decrypted = security.decrypt_private_key(encrypted, settings.MASTER_KEY)
    print("Giải mã:", decrypted)
