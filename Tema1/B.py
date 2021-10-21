import socket

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

def generator_discussion():
    s = socket.socket()
    host = socket.gethostname()
    port = 111

    s.connect((host, port))
    K = s.recv(1024)
    vi = s.recv(1024)
    s.close()

    return K, vi

def KM_discussion(mesaj):
    s = socket.socket() 
    host = socket.gethostname()  
    port = 112  

    s.connect((host, port))
    s.send(mesaj)
    k = s.recv(1024)
    s.close()

    return k

def decrypt_key_ecb(k):
    cipher = AES.new(k_prim, AES.MODE_ECB)
    plaintext = cipher.decrypt(k)
    return plaintext

def decrypt_key_cfb(k):
    vi_cipher = AES.new(k_prim, AES.MODE_ECB)
    vi_plaintext = vi_cipher.encrypt(vi)
    plaintext = bytes([_a ^ _b for _a, _b in zip(vi_plaintext, k)])
    return plaintext

def decrypt_text_ecb(enc_mesaj, k):
    index = 0
    text = b""

    while index <= len(enc_mesaj):
        block_cipher_decrypt = AES.new(k, AES.MODE_ECB)
        block_plaintext = block_cipher_decrypt.decrypt(enc_mesaj[index:(index + 16)])

        if block_plaintext.find(b'\x01') != -1 or block_plaintext.find(b'\x02') != -1 or block_plaintext.find(
                b'\x03') != -1:
            text = text + unpad(block_plaintext, key_length // 8)
        else:
            if block_plaintext.find(b'\x04') != -1 or block_plaintext.find(b'\x05') != -1 or block_plaintext.find(
                    b'\x06') != -1:
                text = text + unpad(block_plaintext, key_length // 8)
            else:
                if block_plaintext.find(b'\x07') != -1 or block_plaintext.find(b'\x08') != -1 or block_plaintext.find(
                        b'\x09') != -1:
                    text = text + unpad(block_plaintext, key_length // 8)
                else:
                    if block_plaintext.find(b'\x10') != -1:
                        text = text + unpad(block_plaintext, key_length // 8)
                    else:
                        text = text + block_plaintext
        index = index + 16

    return text.decode()

def decrypt_text_cfb(enc_mesaj, k, vi):
    index = 0
    text = b""

    while index <= len(enc_mesaj):
        key_encrypt = AES.new(k, AES.MODE_ECB)
        key_encrypt_cfb = key_encrypt.encrypt(pad(vi, key_length // 8))

        block_plaintext = bytes([_a ^ _b for _a, _b in zip(key_encrypt_cfb, enc_mesaj[index:(index + 16)])])
        text = text + block_plaintext
        vi = enc_mesaj[index:(index + 16)]

        index = index + 16

    return text.decode()

def A_discussion(vi):
    s = socket.socket()
    host = socket.gethostname()
    port = 113

    s.connect((host, port))

    inp = s.recv(1024)
    k = KM_discussion(inp)
    print("\nAm preluat cheia criptata k_prim:  ", k)

    s.send(b"Comunicarea poate incepe (mesaj primit de la B)")
    enc_mesaj = s.recv(1024)
    print("\nAm preluat mesajul criptat de A:  ", enc_mesaj)

    s.close()
    if inp == b"ecb":
        k = decrypt_key_ecb(k)
        print("\nAm decriptat cheia k_prim:  ", k)

        file = open("mesaj_decriptat.txt", "w")
        text = decrypt_text_ecb(enc_mesaj, k)
    else:
        k_prim = decrypt_key_cfb(k)
        print("\nAm decriptat cheia k:  ", k)

        file = open("mesaj_decriptat.txt", "w")
        text = decrypt_text_cfb(enc_mesaj, k, vi)

    file.write(text)
    print("\n\nAm decriptat textul primit:\n")
    print(text)

key_length = 128

k_prim, vi = generator_discussion()
print("Am preluat valorile generate:  ", k_prim, vi)

A_discussion(vi)
