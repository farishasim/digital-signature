from math import sqrt, floor
from math_tools import mod_power
import random


# Use sieve of erathosthenes
class Prime:
    def __init__(self):
        self.primes = self.sieve()

    def sieve(self):
        MAX = 1000000
        primes = []
        is_prime = [1 for i in range(1, MAX + 1)]
        is_prime[0] = 0
        for k in range(2, floor(sqrt(MAX))+1):
            if is_prime[k - 1]:
                for j in range(k**2, MAX + 1, k):
                    is_prime[j - 1] = 0
        for prime in range(2, MAX + 1):
            if is_prime[prime - 1]:
                primes.append(prime)
        return primes[100:]

    def generate_prime(self):
        z = mod_power(2, random.randint(200, 121021), len(self.primes))
        return self.primes[z]