import hashlib
import secrets
from Crypto.Cipher import AES

alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate_random_salt(length):
    salt = ''.join(secrets.choice(alphabet) for i in range(length))
    return salt


# use password and salt to generate AES KEY
def generate_cipher(password,salt,iv):
    key = hashlib.pbkdf2_hmac('sha512', password.encode(), salt.encode(), 10000, 32)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher


def encrypt_content(password,salt,iv,content):
    cipher = generate_cipher(password,salt,iv)
    content_bin = content.encode()
    while len(content_bin) % 16 != 0:
        content_bin += b'0'
    return cipher.encrypt(content_bin)


def decrypt_content(password,salt,iv,enc_content):
    cipher = generate_cipher(password,salt,iv)
    return cipher.decrypt(enc_content)