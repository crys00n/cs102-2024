"""
This module allows to encode and decipher strings using Ceaser cipher
"""

def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in range(len(plaintext)):
        if (plaintext[i] not in "xyzXYZ"):
            if plaintext[i].isalpha():
                ciphertext+=chr(ord(plaintext[i])+shift)
            else:
                ciphertext+=plaintext[i]
        elif shift==0:
            ciphertext+=plaintext[i]
        elif plaintext[i]=="x" or plaintext[i]=="X":
            ciphertext+=chr(ord(plaintext[i])-(26-shift))
        elif plaintext[i]=="y" or plaintext[i]=="Y":
            ciphertext+=chr(ord(plaintext[i])-(26-shift))
        elif plaintext[i]=="z" or plaintext[i]=="Z":
            ciphertext+=chr(ord(plaintext[i])-(26-shift))
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    ciphertext.encode(encoding="utf-8")
    plaintext = ""
    for i in range(len(ciphertext)):
        if (ciphertext[i] not in "ABCabc"):
            if ciphertext[i].isalpha():
                plaintext+=chr(ord(ciphertext[i])-shift)
            else:
                plaintext+=ciphertext[i]
        elif shift==0:
            plaintext+=ciphertext[i]
        elif ciphertext[i]=="a" or ciphertext[i]=="A":
            plaintext+=chr(ord(ciphertext[i])+(26-shift))
        elif ciphertext[i]=="b" or ciphertext[i]=="B":
            plaintext+=chr(ord(ciphertext[i])+(26-shift))
        elif ciphertext[i]=="c" or ciphertext[i]=="C":
            plaintext+=chr(ord(ciphertext[i])+(26-shift))
    return plaintext
