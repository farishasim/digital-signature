from backend import sha256
import sys
import re

def get_public_key_file(filename):
    #open text file
    text_file = open(filename, "w")
    #write public key
    text_file.write('Hello World!')
    #close file
    text_file.close()

def get_private_key_file(filename):
    #open text file
    text_file = open(filename, "w")
    #write private key
    text_file.write('Hello World!')
    #close file
    text_file.close()

def get_hash_file(filename):
    with open(filename, 'rb') as f:
        temp_s = int(bin(int.from_bytes(f.read(), byteorder=sys.byteorder)),2)
        #print("temp_s", temp_s)
        s = sha256.sha_256(temp_s)
        #print(type(s))
    return s

def get_hash_content(string_hex):
    temp_s = int(bin(int.from_bytes(string_hex, byteorder=sys.byteorder)),2)
    #print("temp_s", temp_s)
    s = sha256.sha_256(temp_s)
    #print(type(s))
    return s

def find_signature(filename):
    hasil = ""
    with open(filename, 'rb') as f:
        s = str(f.read()[-10000:])
        start = s.find("<ds>") + len("<ds>")
        end = s.find("</ds>")
        hasil = s[start:end]
    if(len(hasil) > 0):
        return hasil
    else:
        return -1

def find_content(filename):
    hasil = ""
    with open(filename, 'rb') as f:
        s = str(f.read())
        hasil = re.sub('<ds>.*?</ds>', '', s)
    return hasil
