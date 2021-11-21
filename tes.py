# Open file with 'b' to specify binary mode
with open("d:\\public.pub", 'rb') as f:
    print(f.read()[-30:])
    