from unittest import TestCase
from uuid import uuid4

from application.core.managers.cipher_manager import CaesarCipher

class CipherValidation(TestCase):

    def setUp(self) -> None:
        self.caesar_cipher = CaesarCipher()

    def test_encrypt_decrypt(self) -> None:
        test_text = uuid4().hex
        encrypt_text = self.caesar_cipher.encrypt(text=test_text)
        self.assertNotEqual(first=test_text, second=encrypt_text, msg="Encryption failure")

        decrypt_text = self.caesar_cipher.decrypt(text=encrypt_text)
        self.assertNotEqual(first=encrypt_text, second=decrypt_text, msg="Decryption failure")

        self.assertEqual(first=test_text, second=decrypt_text, msg="Cipher failure")
