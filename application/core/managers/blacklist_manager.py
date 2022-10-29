"""this file is made for containing:
[*] JWT Tokens of Logged out users
[*] JWT Tokens of blocked users

in this way we can Access Control users by posses all Identities from tokens
"""
class BlackList:
    def __new__(cls, *args, **kwargs):
        return set()
