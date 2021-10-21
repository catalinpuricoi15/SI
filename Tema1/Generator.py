import random
import string
import socket

key_length = 128

k_prim = str.encode(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=key_length // 8)))
vi = str.encode(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=key_length // 8)))

print("Cheia k_prim generata este :  ", k_prim)
print("Vectorul de initializare este:  ", vi)

s = socket.socket()
host = socket.gethostname()
port = 111

s.bind((host, port))

s.listen()
if True:
    c, adr = s.accept()
    print("Got conection from node KM")
    c.send(k_prim)
    c.send(vi)
    c.close()

if True:
    c, adr = s.accept()
    print("Got conection from node A")
    c.send(k_prim)
    c.send(vi)
    c.close()

if True:
    c, adr = s.accept()
    print("Got conection from node B")
    c.send(k_prim)
    c.send(vi)
    c.close()

s.close()
