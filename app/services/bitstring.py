import base64
import gzip
from typing import List

"""
Running a simple benchmark gives us the following result on the size of the compressed bitstring:

Revocations:  0  Len:  68
Revocations:  1  Len:  76
Revocations:  5  Len:  100
Revocations:  10  Len:  147
Revocations:  25  Len:  227
Revocations:  50  Len:  358
Revocations:  75  Len:  536
Revocations:  100  Len:  763
Revocations:  1000  Len:  2424
Revocations:  10000  Len:  11082
Revocations:  100000  Len:  21672

All revocations are randomly generated. Because of the way that gzip works, this results in a logarithmic to sub-linear growth.
"""


def generate_compressed_bitstring(revoked_credentials: List[int], bitstring_size_kb: int = 16) -> str:
    bitstring_size = bitstring_size_kb * 1024 * 8
    bitstring = bytearray(bitstring_size // 8)

    for bit_pos in revoked_credentials:
        byte_index = bit_pos // 8
        bit_offset = bit_pos % 8
        bitstring[byte_index] |= 1 << (7 - bit_offset)

    compressed = gzip.compress(bytes(bitstring))
    b64url_encoded = base64.b64encode(compressed).decode("ascii")

    return b64url_encoded
