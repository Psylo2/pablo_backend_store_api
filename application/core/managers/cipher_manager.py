import os

from application.interfaces.core.managers.cipher_interface import CaesarCipherInterface

class CaesarCipher(CaesarCipherInterface):

    def encrypt(self, text: str) -> str:
        step = int(os.environ.get('CAESAR_SHIFT'))
        return self.__base_caesar_cipher(text=text, step=step)

    def decrypt(self, text: str) -> str:
        step = -1 * int(os.environ.get('CAESAR_SHIFT'))
        return self.__base_caesar_cipher(text=text, step=step)

    @staticmethod
    def __base_caesar_cipher(text: str, step: int) -> str:
        enc = ""
        for char in text:
            val = ord(char) + step
            enc += chr(val % 128)
        return enc
