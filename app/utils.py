import codecs


def rot13_encrypt(word: str) -> str:
    """Encrypt word into Rot13"""
    return codecs.encode(word, 'rot_13')
