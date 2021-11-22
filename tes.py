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

print(find_signature("d:\\public.pub"))