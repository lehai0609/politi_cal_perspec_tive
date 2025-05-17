import hashlib
from typing import List


def simhash(text: str) -> int:
    tokens = [t.strip('.,;:!?"\'"') for t in text.split()]
    v = [0] * 64
    for token in tokens:
        h = int(hashlib.md5(token.encode('utf-8')).hexdigest(), 16)
        for i in range(64):
            bitmask = 1 << i
            if h & bitmask:
                v[i] += 1
            else:
                v[i] -= 1
    fingerprint = 0
    for i in range(64):
        if v[i] > 0:
            fingerprint |= 1 << i
    return fingerprint


def hamming_distance(x: int, y: int) -> int:
    return bin(x ^ y).count('1')
