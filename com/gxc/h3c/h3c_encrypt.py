# -*- coding: utf-8 -*-
"""
使用说明

准备工作：
1. 正式使用时，请 EISOO_PRIKEY 的值更新为正式的加密私钥，H3CRYPTO_PUBKEY 的值更新为正式的加密公钥
2. 依赖 PyCrypto 加密库，仅在 2.6.1 版本下测试通过，请尽量保证版本一致

如何使用：
1. 加密明文时调用 eisoo_encrypt(plaintext) 方法即可得到加密后的密文
2. 解密密文时调用 h3c_decrypt(ciphertext) 方法即可得到解密后的明文
"""
import binascii
from Crypto.Util.py3compat import b, tobytes
from Crypto.Util.number import size, ceil_div
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def calc_k(rsakey):
    mod_bits = size(rsakey.n)
    k = ceil_div(mod_bits, 8)
    return k
EISOO_PUBKEY=b("")
eisoo_pub_rsakey =None
eisoo_pub_cipher=None
eisoo_pub_k = None

EISOO_PRIKEY = b('''''')
eisoo_priv_rsakey = None
eisoo_priv_cipher = None
eisoo_priv_k = None
LOAD_KEY = False
H3CRYPTO_PUBKEY = b('''''')
h3c_pub_rsakey = None
h3c_pub_cipher = None
h3c_pub_k = None

h3c_priv_rsa_key = None
h3c_priv_cipher = None
h3c_priv_k = None
    
H3CRYPTO_PRIVKEY = b('''''')
base_path="D:/develop/git/abcloud/program/server/services/anycloudsvc/"
def load_key():
    global LOAD_KEY
    if LOAD_KEY:
        return
    #加载
    print 'load key'
    global eisoo_pub_rsakey,eisoo_pub_cipher,eisoo_pub_k,eisoo_priv_rsakey,eisoo_priv_cipher,eisoo_priv_k
    global h3c_pub_cipher,h3c_pub_rsakey,h3c_pub_k,h3c_priv_cipher,h3c_priv_k,h3c_priv_rsa_key
    EISOO_PUBKEY=b("")
    with open(base_path+'config/eisoo-public.pem') as f:
        EISOO_PUBKEY = f.read()
    eisoo_pub_rsakey = RSA.importKey(EISOO_PUBKEY)
    eisoo_pub_cipher = PKCS1_v1_5.new(eisoo_pub_rsakey)
    eisoo_pub_k = calc_k(eisoo_pub_rsakey)

    with open(base_path+'config/eisoo-private.pem') as f:
        EISOO_PRIKEY = f.read()
        eisoo_priv_rsakey = RSA.importKey(EISOO_PRIKEY)
        eisoo_priv_cipher = PKCS1_v1_5.new(eisoo_priv_rsakey)
        eisoo_priv_k = calc_k(eisoo_priv_rsakey)


    with open(base_path+'config/h3c-public.pem') as f:
        H3CRYPTO_PUBKEY = f.read()
        h3c_pub_rsakey = RSA.importKey(H3CRYPTO_PUBKEY)
        h3c_pub_cipher = PKCS1_v1_5.new(h3c_pub_rsakey)
        h3c_pub_k = calc_k(h3c_pub_rsakey)
        
    with open(base_path+'config/h3c-private.pem') as f:
        H3CRYPTO_PRIVKEY = f.read()
        h3c_priv_rsa_key = RSA.importKey(H3CRYPTO_PRIVKEY)
        h3c_priv_cipher = PKCS1_v1_5.new(h3c_priv_rsa_key)
        h3c_priv_k = calc_k(h3c_priv_rsa_key)
    LOAD_KEY = True
        

def group(text, length):
    """Divide the text into groups by the specific length.

    :param text: The text to be divided.
    :param length: The group length
    :return: a iterable generator
    """
    while text:
        yield text[:length]
        text = text[length:]


def h3c_encrypt(plaintext):
    """Encrypt the plain text into cipher text. This method encrypt the plain
    text using.

    >>> plaintext = 'this is plain text'
    >>> ciphertext = h3c_encrypt(plaintext)
    >>> print(ciphertext)
    b'YR0x4XSXuwlB5dUTGeqmiFup/pvonCuKUrXXpXmPWgPHFjNpNBhdO5RoFjv+sRGSSXVVTi/l8OQvXOe+QAmKXo/rvPAh4Ye7so/3JFUVSB641qGnMjCcZ5nUVR7O/4xfYylKdHcxoIl//TeK6kOunY/tNhU8Lv+BuA5xuyFYEQ9DsPvWK85IgIs9RsPEYK9TEGWqy5q1mQIsUBexLZtrCYa/oLsrVM/c/cIiuYtbyjcf5LI+P7DkK6XrMpcOICg+Mnuvcle9/OT8u63arnx0NDAVYVgABUedu7faT9qjciiDnbtW9zjW1HUNETlrwWpbPG7BDGrDb9kFpD6xVn4LIg=='

    :param plaintext: the plain text to be encrypted.
    :return: the cipher text
    """
    load_key()
    cipher = b('')
    for seg in group(tobytes(plaintext), h3c_pub_k - 11):
        m = h3c_pub_cipher.encrypt(seg)
        cipher += m
    ciphertext = binascii.b2a_base64(cipher)
    return ciphertext[:-1]  # 删除换行符


def h3c_decrypt(ciphertext):
    """Decrypt the cipher text into plain text. This method decrypt the cipher
    text using.

    >>> ciphertext = 'YR0x4XSXuwlB5dUTGeqmiFup/pvonCuKUrXXpXmPWgPHFjNpNBhdO5RoFjv+sRGSSXVVTi/l8OQvXOe+QAmKXo/rvPAh4Ye7so/3JFUVSB641qGnMjCcZ5nUVR7O/4xfYylKdHcxoIl//TeK6kOunY/tNhU8Lv+BuA5xuyFYEQ9DsPvWK85IgIs9RsPEYK9TEGWqy5q1mQIsUBexLZtrCYa/oLsrVM/c/cIiuYtbyjcf5LI+P7DkK6XrMpcOICg+Mnuvcle9/OT8u63arnx0NDAVYVgABUedu7faT9qjciiDnbtW9zjW1HUNETlrwWpbPG7BDGrDb9kFpD6xVn4LIg=='
    >>> plaintext = h3c_decrypt(ciphertext)
    >>> print(plaintext)
    b'this is plain text'

    :param ciphertext: the cipher text to be decrypted.
    :return: the plain text
    """
    load_key()
    cipher = binascii.a2b_base64(tobytes(ciphertext))
    plain = b('')
    for seg in group(cipher, h3c_priv_k):
        m = h3c_priv_cipher.decrypt(seg, -1)
        plain += m
    return plain


def eisoo_encrypt(plaintext):
    """Encrypt the plain text into cipher text. This method encrypt the plain
    text using.

    >>> plaintext = 'this is plain text'
    >>> ciphertext = eisoo_encrypt(plaintext)
    >>> print(ciphertext)
    b'YR0x4XSXuwlB5dUTGeqmiFup/pvonCuKUrXXpXmPWgPHFjNpNBhdO5RoFjv+sRGSSXVVTi/l8OQvXOe+QAmKXo/rvPAh4Ye7so/3JFUVSB641qGnMjCcZ5nUVR7O/4xfYylKdHcxoIl//TeK6kOunY/tNhU8Lv+BuA5xuyFYEQ9DsPvWK85IgIs9RsPEYK9TEGWqy5q1mQIsUBexLZtrCYa/oLsrVM/c/cIiuYtbyjcf5LI+P7DkK6XrMpcOICg+Mnuvcle9/OT8u63arnx0NDAVYVgABUedu7faT9qjciiDnbtW9zjW1HUNETlrwWpbPG7BDGrDb9kFpD6xVn4LIg=='

    :param plaintext: the plain text to be encrypted.
    :return: the cipher text
    """
    load_key()
    cipher = b('')
    for seg in group(tobytes(plaintext), eisoo_pub_k - 11):
        m = eisoo_pub_cipher.encrypt(seg)
        cipher += m
    ciphertext = binascii.b2a_base64(cipher)
    return ciphertext[:-1]  # 删除换行符


def eisoo_decrypt(ciphertext):
    """Decrypt the cipher text into plain text. This method decrypt the cipher
    text using.

    >>> ciphertext = 'YR0x4XSXuwlB5dUTGeqmiFup/pvonCuKUrXXpXmPWgPHFjNpNBhdO5RoFjv+sRGSSXVVTi/l8OQvXOe+QAmKXo/rvPAh4Ye7so/3JFUVSB641qGnMjCcZ5nUVR7O/4xfYylKdHcxoIl//TeK6kOunY/tNhU8Lv+BuA5xuyFYEQ9DsPvWK85IgIs9RsPEYK9TEGWqy5q1mQIsUBexLZtrCYa/oLsrVM/c/cIiuYtbyjcf5LI+P7DkK6XrMpcOICg+Mnuvcle9/OT8u63arnx0NDAVYVgABUedu7faT9qjciiDnbtW9zjW1HUNETlrwWpbPG7BDGrDb9kFpD6xVn4LIg=='
    >>> plaintext = eisoo_decrypt(ciphertext)
    >>> print(plaintext)
    b'this is plain text'

    :param ciphertext: the cipher text to be decrypted.
    :return: the plain text
    """
    load_key()
    cipher = binascii.a2b_base64(tobytes(ciphertext))
    plain = b('')
    for seg in group(cipher, eisoo_priv_k):
        m = eisoo_priv_cipher.decrypt(seg, -1)
        plain += m
    return plain

if __name__=="__main__":
    plaintext="guanxianchun"
    cipher_text = h3c_encrypt(plaintext)
    print 'h3c-->',cipher_text
    print 'h3c==',h3c_decrypt(cipher_text)
    cipher_text = eisoo_encrypt(plaintext)
    print 'eisoo-->',cipher_text
    print 'eisoo==',eisoo_decrypt(cipher_text)