from hashlib import sha256

from crypto.ec import Curve, modinv, Point, Infinity
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

    def verify(self, r: int, s: int, m: bytes, publicKey: Point) -> bool:
        """
        verify verifies the given signature of the given message
        using the given public key.

        verify returns True if and only if the given signature has been signed
        by the private key corresponding to the given public key.
        """
        self._verify_params(publicKey)
        w = modinv(s, self.curve.q)
        u1 = w * int(sha256(m).hexdigest(), 16) % self.curve.q
        u2 = w * r % self.curve.q
        P = (u1 * self.curve.generator) + (u2 * publicKey)
        if P.x == (r % self.curve.q):
            return True
        return False

    def _verify_params(self, publicKey: Point):
        if publicKey == Infinity():
            raise ValueError("Public key is point at infinity")
        if not self.curve.is_point(publicKey.x, publicKey.y):
            raise ValueError("Public key is not on curve")
