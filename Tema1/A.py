import socket

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def generator_discussion():
    s = socket.socket()
    host = socket.gethostname()
    port = 111

    s.connect((host, port))
    k_prim = s.recv(1024)
    vi = s.recv(1024)
    s.close()

    return k_prim, vi

def KM_discussion(mesaj):
    s = socket.socket()
    host = socket.gethostname()
    port = 112

    s.connect((host, port))
    s.send(mesaj)
    k_prim = s.recv(1024)
    s.close()

    return k_prim

def decrypt_key_ecb(k):
    cipher = AES.new(k_prim, AES.MODE_ECB)
    plaintext = cipher.decrypt(k)
    return plaintext

def decrypt_key_cfb(k):
    vi_cipher = AES.new(k_prim, AES.MODE_ECB)
    vi_plaintext = vi_cipher.encrypt(vi)
    plaintext = bytes([_a ^ _b for _a, _b in zip(vi_plaintext, k)])
    return plaintext

def encrypt_text_ecb(k):
    readfile = open('mesaj.txt', 'r')

    text_encrypt = str.encode("")
    while readfile:
        block_cipher = AES.new(k, AES.MODE_ECB)
        block = str.encode(readfile.read(key_length // 8))
        block_ciphertext = block_cipher.encrypt(pad(block, key_length // 8))

        text_encrypt = text_encrypt + block_ciphertext

        if block.decode() == "":
            break
    readfile.close()
    return text_encrypt

def encrypt_text_cfb(k):
    readfile = open('mesaj.txt', 'r')
    text_encrypt = str.encode("")

    key_vector = vi
    while readfile:
        key_encrypt = AES.new(k, AES.MODE_ECB)
        key_encrypt_cfb = key_encrypt.encrypt(pad(key_vector, key_length // 8))
        block = str.encode(readfile.read(key_length // 8))
        block_ciphertext = bytes([_a ^ _b for _a, _b in zip(key_encrypt_cfb, block)])

        text_encrypt = text_encrypt + block_ciphertext
        key_vector = block_ciphertext

        if block.decode() == "":
            break
    readfile.close()
    return text_encrypt

def B_discussion(inp, enc_mesaj):
    s = socket.socket()
    host = socket.gethostname()
    port = 113
    s.bind((host, port))
    s.listen()

    if True:
        c, adr = s.accept()
        print("Got conection with node B")
        c.send(inp.encode())
        print(c.recv(1024).decode())
        print("\nTrimitem mesajul criptat lui B:  ", enc_mesaj)
        c.send(enc_mesaj)
        c.close()
    s.close()

def main():

    print("\nAlegeti modul de operare dorit (ecb/cfb):   ")
    inp = input()
    if inp.lower() == "ecb":
        k = KM_discussion(b"ecb")
        print("\nAm preluat cheia criptata k:  ", k)
        k = decrypt_key_ecb(k)
        print("\nAm decriptat cheia k:  ", k)
        B_discussion(inp.lower(), encrypt_text_ecb(k))
    else:
        k = KM_discussion(b"cfb")
        print("\nAm preluat cheia criptata k:  ", k)
        k = decrypt_key_cfb(k)
        print("\nAm decriptat cheia k:  ", k)
        B_discussion(inp.lower(), encrypt_text_cfb(k))

key_length = 128

k_prim, vi = generator_discussion()
print("Am preluat valorile generate:  ", k_prim, vi)

main()

