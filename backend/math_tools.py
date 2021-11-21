# Menghitung nilai dari x^m mod n dengan kompleksitas O(log m)
def mod_power(x, m, n):
    if m == 0: return 1
    elif m == 1: return (x % n)
    else:
        y = mod_power(x, m >> 1, n)
        return((y * y * mod_power(x, m%2, n)) % n)

# Asumsi x = 1 (mod n). Gunakan extended euclid untuk dapatkan a, b sehingga 
# ax + bn = 1
def inverse_modulo(x, n):
    old_r, r = x, n
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        quo = old_r // r
        old_r, r = r, old_r - quo * r
        old_s, s = s, old_s - quo * s
        old_t, t = t, old_t - quo * t
    
    if old_s < 0:
        return old_s + n
    else: return old_s

def fpb(a, b):
    if(b==0): return a
    else: return fpb(b, a % b)
    
def split_bit(n, length):
    chunks = []
    if n.bit_length() % length != 0:
        n <<= (length - (n.bit_length() % length))
    
    num_chunk = n.bit_length() // length
    for i in range(num_chunk):
        mask = (1 << length) - 1
        chunks.append((n & (mask << ((num_chunk - i - 1) * length))) >> ((num_chunk - i - 1) * length))
    return chunks

def split_bit_pref(n, length):
    chunks = []
    num_chunk = n.bit_length() // length
    if n.bit_length() % length != 0:
        num_chunk += 1
    
    for i in range(num_chunk):
        mask = (1 << length) - 1
        chunks.append((n & (mask << ((num_chunk - i - 1) * length))) >> ((num_chunk - i - 1) * length))
    return chunks 