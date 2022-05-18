import secrets

from crypto.ec import Curve


def gen_private_key(curve: Curve) -> int:
    """
    Generate a private key that is compatible with the given curve,
    i.e the key lies within 0 < k < q where q is the prime order of the
    subgroup generated by the attached generator.
    """
    return secrets.randbelow(curve.q)


def gen_nonce(curve: Curve) -> int:
    """
    Generate a random nonce (also termed ephemeral key) with
    0 < k < q where q is the prime order of the subgroup generated by
    the attached generator.
    """
    return secrets.randbelow(curve.q)
