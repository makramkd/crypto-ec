from hashlib import sha256

from crypto.ec import Curve, modinv
from crypto.rand import gen_nonce


class ECDSA:
    """
    ECDSA implements the elliptic curve digital signature
    algorithm.

    The output of the algorithm is an x coordinate, r, and
    a signature, s, which can be verified as having been generated
    by a particular private key p, without actually knowing the private key.

    In particular, the public key pG, where G is the generator of an
    elliptic curve subgroup, alongside r, s and the message that was signed,
    are all that is required to verify the signature.
    """

    def __init__(self, curve: Curve, tries=10):
        self.curve = curve
        self.tries = tries

    def sign(self, m: bytes, private_key: int) -> (int, int):
        """
        sign signs the given message with the private key using the ECDSA
        algorithm.

        The output is the pair (r, s), which together represent the ECDSA
        signature.
        """
        order = self.curve.q
        for i in range(self.tries):
            k = gen_nonce(self.curve)
            R = k * self.curve.generator
            r = R.x
            s = (
                (int(sha256(m).hexdigest(), 16) + private_key * r) * modinv(k, order)
            ) % order
            # In the event that s is zero we have to re-generate a nonce
            if s:
                return r, s
        raise ValueError("Could not generate a signature in {self.tries} tries")

    def verify(self, r: int, s: int, m: bytes):
        pass
