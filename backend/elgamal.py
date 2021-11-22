import time, random, os
from math import log2, ceil
from flask import *
import math_tools, prime, sha256

# app.config["UPLOAD_FOLDER"]='dump'

def key_generator():
    prim = prime.Prime()    
    p = 524287
    g = random.randint(2, p-1)
    x = random.randint(1, p-2)
    y = math_tools.mod_power(g, x, p)

#    path = os.path.join(current_app.root_path + "/" + app.config["UPLOAD_FOLDER"])
    
    f = open("public.pub", 'w')
    f.write('y=' + str(y) + '\n' + 'g=' + str(g) + '\n' + 'p=' + str(p))
    f.close()
    
    f = open("private.pri", 'w')
    f.write('x=' + str(x) + '\n' + 'p=' + str(p))
    f.close()


def encrypt_elgamal(plaintext):
    key_generator()
    f = open('public.pub', 'r')
    text = f.read()
    keys = text.split('\n')
    y = int(keys[0][2:])
    g = int(keys[1][2:])
    p = int(keys[2][2:])
    f.close()

    block_length = ceil(log2(p + 1))

    plains = math_tools.split_bit(plaintext, block_length)
    print(plains)
    print(bin(plaintext))
    cipher = 0
    
    k = random.randint(1, p-2)
    for i in range(len(plains[0])):
        a = math_tools.mod_power(g, k, p)
        b = ((plains[0][i] % p) * math_tools.mod_power(y, k, p)) % p
        cipher <<= block_length
        cipher += a
        cipher <<= block_length
        cipher += b
        print([a, b])
    return cipher

def decrypt_elgamal(ciphertext):
    f = open('private.pri', 'r')
    text = f.read()
    keys = text.split('\n')
    x = int(keys[0][2:])
    p = int(keys[1][2:])
    f.close()

    block_length = ceil(log2(p + 1))

    ciphers = math_tools.split_bit_pref(ciphertext, 2*block_length)
    pl = []
    plains = 0
    for i in range(len(ciphers[0])):
        [a, b] = math_tools.split_bit_pref(ciphers[0][i], block_length)[0]
        plain = ((b % p) * math_tools.mod_power(a, p - 1 - x, p)) % p
        print([a, b])
        if(i == (len(ciphers[0]) - 1)):
            plains <<= (plain.bit_length())
        else:
            plains <<= block_length
        plains += plain
        print(bin(plains))
        pl.append(plain)
    print(pl)
    return plains

sha = sha256.sha_256(0b11011)
nha = encrypt_elgamal(sha)
print(sha)
print(nha)
xha = decrypt_elgamal(nha)
print(xha)
print(sha == xha)
      
