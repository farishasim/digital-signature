from backend import math_tools

kTable = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
   0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
   0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
   0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
   0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
   0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
   0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
   0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

def ror(bit, rotate, max_bits):
    rotate %= max_bits
    return(
        ((bit & ((1 << max_bits) - 1)) >> rotate) |\
        ((bit << (max_bits - rotate)) & ((1 << max_bits) - 1))
    )

# Message sudah dalam bentuk bit
def sha_256(message):
    h0, h1, h2, h3, h4, h5, h6, h7 = 0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
     
    # Padding
    length = message.bit_length()
    message = (message << 1) + 1
    k = 447 - (length % 512)
    if k < 0: k = k + 512
    message = (message << (64 + k)) + length
    padded_length = message.bit_length()
     
    # Prosesi
    chunks = math_tools.split_bit(message, 512)
    for chunk in chunks:
        words = [0 for _ in range(64)]
        chunk_word = math_tools.split_bit(chunk, 32)
        for i in range(16):
            words[i] = chunk_word[i]
            
        for i in range(16, 64):
            s0 =  (ror(words[i-15], 7, 32)) ^ (ror(words[i-15], 18, 32)) ^ (ror(words[i-15], 3, 32))
            s1 = (ror(words[i-2], 17, 32)) ^ (ror(words[i-2], 19, 32)) ^ (ror(words[i-2], 10, 32))
            words[i] = words[i - 16] + s0 + words[i-7] + s1
            
        a, b, c, d, e, f, g, h  = h0, h1, h2, h3, h4, h5, h6, h7

        for i in range(64):
            c1 = (ror(e, 6, 32)) ^ (ror(e, 11, 32)) ^ (ror(e, 25, 32))
            ch = (e & f) ^ (~e & g)
            temp1 = h + c1 + ch + kTable[i] + words[i]
            c0 = (ror(a, 2, 32))  ^ (ror(a, 13, 32)) ^ (ror(a, 22, 32))
            maj = (a & b) ^ (b & c) ^ (c & a)
            temp2 = c0 + maj
            
            h = g
            g = f
            f = e
            e = d + temp1
            d = c
            c = b
            b = a
            a = temp1 + temp2
        
        h0 += a
        h1 += b
        h2 += c
        h3 += d
        h4 += e
        h5 += f
        h6 += g
        h7 += h
           
    digest = (h0 << 32) + h1
    digest <<= 32
    digest += h2
    digest <<= 32
    digest += h3
    digest <<= 32
    digest += h4
    digest <<= 32
    digest += h5
    digest <<= 32
    digest += h6
    digest <<= 32
    digest += h7 
    return(digest)