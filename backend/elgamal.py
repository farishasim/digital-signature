import time, random, os
from math import log2, ceil
from flask import *
from backend import math_tools, prime, sha256

def key_generator():
    prim = prime.Prime()    
    p = prim.generate_prime()
    g = random.randint(2, p-1)
    x = random.randint(1, p-2)
    y = math_tools.mod_power(g, x, p)

#    path = os.path.join(current_app.root_path + "/" + app.config["UPLOAD_FOLDER"])
    
    f = open("dump/public.pub", 'w')
    f.write('y=' + str(y) + '\n' + 'g=' + str(g) + '\n' + 'p=' + str(p))
    f.close()
    
    f = open("dump/private.pri", 'w')
    f.write('x=' + str(x) + '\n' + 'p=' + str(p))
    f.close()


def encrypt_elgamal(plaintext):
    key_generator()
    f = open('dump/public.pub', 'r')
    text = f.read()
    keys = text.split('\n')
    y = int(keys[0][2:])
    g = int(keys[1][2:])
    p = int(keys[2][2:])
    f.close()

    block_length = ceil(log2(p - 1))

    plains = math_tools.split_bit(plaintext, block_length)
    
    cipher = 0
    
    k = random.randint(1, p-2)
    for plain in plains:
        print(plain)
        a = math_tools.mod_power(g, k, p)
        b = (plain * math_tools.mod_power(y, k, p)) % p
        cipher <<= block_length
        cipher += a
        cipher <<= block_length
        cipher += b
    return cipher

def decrypt_elgamal(ciphertext):
    f = open('dump/private.pri', 'r')
    text = f.read()
    keys = text.split('\n')
    x = int(keys[0][2:])
    p = int(keys[1][2:])
    f.close()

    block_length = ceil(log2(p - 1))

    ciphers = math_tools.split_bit_pref(ciphertext, 2*block_length)
    plains = 0
    for cipher in ciphers:
        [a, b] = math_tools.split_bit_pref(cipher, block_length)
        plain = (b * math_tools.mod_power(a, p - 1 - x, p)) % p
        print(plain)
        plains <<= block_length
        plains += plain
    return plains

if __name__=="__main__":
    sha = sha256.sha_256(0b100101010001)
    nha = encrypt_elgamal(sha)
    print(sha)
    print(nha)
    print(decrypt_elgamal(nha))
        