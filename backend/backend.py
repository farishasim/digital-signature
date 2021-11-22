from backend import sha256, elgamal
import sys
import re

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
    if(end != -1):
        return hasil
    else:
        return -1

def find_content(filename):
    hasil = ""
    with open(filename, 'rb') as f:
        s = "".join([chr(b) for b in f.read()])
        hasil = re.sub('<ds>.*?</ds>', '', s)
    return hasil

if __name__ == "__main__":
    a = find_signature("C:\\Users\\JLGading\\Downloads\\TeksBerita (6).txt")
    print(a)
