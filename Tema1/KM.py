import socket
import random
import string

from Crypto.Cipher import AES

def generator_discussion():
    s = socket.socket()
    host = socket.gethostname()
    port = 111

    s.connect((host, port))
    k_prim = s.recv(1024)
    vi = s.recv(1024)
    s.close()

    return k_prim, vi

def encrypt_key_ecb(k):
    key_encrypt = AES.new(k_prim, AES.MODE_ECB)
    ciphertext = key_encrypt.encrypt(k)
    return ciphertext


def encrypt_key_cfb(k):
    vi_encrypt = AES.new(k_prim, AES.MODE_ECB)
    cipher = vi_encrypt.encrypt(vi)
    ciphertext = bytes([_a ^ _b for _a, _b in zip(cipher, k)])
    return ciphertext

def A_B_discussion():
    s = socket.socket()
    host = socket.gethostname()
    port = 112

    s.bind((host, port))

    s.listen()
    if True:
        c, adr = s.accept()
        print("Got conection with node A")
        mesaj = c.recv(1024)
        if mesaj == b"ecb":
            ciphertext_k = encrypt_key_ecb(k)
            print("\nTrimitem cheia criptata k lui A:  ", ciphertext_k)
            c.send(ciphertext_k)
        else:
            ciphertext_k = encrypt_key_cfb(k)
            print("\nTrimitem cheia criptata k lui A:  ", ciphertext_k)
            c.send(ciphertext_k)
        c.close()

    if True:
        c, adr = s.accept()
        print("Got conection with node B")
        mesaj = c.recv(1024)
        if mesaj == b"ecb":
            ciphertext_k = encrypt_key_ecb(k)
            print("Catalin:", k)
            print("\nTrimitem cheia criptata k lui B:  ", ciphertext_k)
            c.send(ciphertext_k)
        else:
            ciphertext_k = encrypt_key_cfb(k)
            print("\nTrimitem cheia criptata k lui B:  ", ciphertext_k)
            c.send(ciphertext_k)
        c.close()

    s.close()

key_length = 128

k_prim, vi = generator_discussion()
print("Am preluat valorile generate:  ", k_prim, vi)

k = str.encode(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=key_length // 8))) #random key
print("\nGeneram cheia:  ", k)

A_B_discussion()
