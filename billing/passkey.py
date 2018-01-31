import os

from django.conf import settings

from keyczar import keyczar

KEY_PATH = os.path.join(settings.BASE_DIR, 'keys')


def encrypt(plaintext):
    crypter = _get_crypter()
    return crypter.Encrypt(plaintext)


def decrypt(ciphertext):
    crypter = _get_crypter()
    return crypter.Decrypt(ciphertext)


def _get_crypter():
    return keyczar.Crypter.Read(KEY_PATH)
