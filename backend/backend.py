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

def find_signature(filename):
    hasil = ""
    with open(filename, 'rb') as f:
        s = str(f.read()[-30:])
        start = s.find("<ds>") + len("<ds>")
        end = s.find("</ds>")
        hasil = s[start:end]
    if(len(hasil) > 0):
        return hasil
    else:
        return -1