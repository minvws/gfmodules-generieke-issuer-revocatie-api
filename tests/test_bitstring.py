import base64
import gzip
import unittest

from app.services.bitstring import generate_compressed_bitstring


class TestCompressedBitstring(unittest.TestCase):
    @staticmethod
    def decode_bitstring(encoded: str) -> bytes:
        padding = "=" * ((4 - len(encoded) % 4) % 4)
        decoded = base64.urlsafe_b64decode(encoded + padding)
        return gzip.decompress(decoded)

    def test_no_revocations(self) -> None:
        encoded = generate_compressed_bitstring([])
        decompressed = self.decode_bitstring(encoded)
        self.assertEqual(decompressed, bytes(16 * 1024))

    def test_single_revocation(self) -> None:
        encoded = generate_compressed_bitstring([42])
        decompressed = self.decode_bitstring(encoded)
        self.assertEqual(0, decompressed[4])
        self.assertEqual(32, decompressed[5])
        self.assertEqual(0, decompressed[6])

    def test_multiple_revocations(self) -> None:
        indices = [0, 100, 1023, 2047 * 8]
        encoded = generate_compressed_bitstring(indices)
        decompressed = self.decode_bitstring(encoded)
        for i in indices:
            byte_index = i // 8
            bit_offset = i % 8
            self.assertTrue(decompressed[byte_index] & (1 << (7 - bit_offset)))

    def test_invalid_revocation_out_of_bounds(self) -> None:
        with self.assertRaises(IndexError):
            generate_compressed_bitstring([1000000000])
