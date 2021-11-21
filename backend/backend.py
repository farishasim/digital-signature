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

def find_signature(infile):
    hasil = ""
    pattern = re.compile(b"[<ds>]")
    pattern2 = re.compile(b"[<\ds>]")
    copy = False
    for line in infile:
        if line.strip() == bool(pattern.search(line)):
            copy = True
            continue
        elif line.strip() == bool(pattern2.search(line)):
            copy = False
            continue
        elif copy:
            hasil.append(line)
    return hasil
    # if(len(hasil) > 0):
    #     return hasil
    # else:
    #     return -1