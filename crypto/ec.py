class Curve:
    """
    An elliptic curve over Z_p, p > 3 is the set of points (x, y) described by the equation
        y^2 = x^3 + ax + b mod p
    where 4a^3 + 27b^2 != 0 mod p. Geometrically speaking, this means that the curve has no
    self-intersections or vertices, which is achieved if the discriminant of the curve
    is nonzero.
    """

    def __init__(self, a: int, b: int, p: int, q: int = None, generator=None):
        self.p = p
        self.q = q
        self.generator = generator
        self._check_curve_parameters(a, b)
        self.a = a
        self.b = b

    def _check_curve_parameters(self, a: int, b: int):
        if (((4 * a**3) + (27 * b**2)) % self.p) == 0:
            raise ValueError(
                f"Given curve parameters are incorrect: ((4 * {a}**3) + (27 * {b}**2)) mod {self.p} == 0"
            )

    def is_point(self, x: int, y: int) -> bool:
        """
        Return true if and only if the given point (x, y) is on this curve.
        """
        return (((y**2) - (x**3 + self.a * x + self.b)) % self.p) == 0

    def __repr__(self) -> str:
        return f"Curve(a={self.a}, b={self.b})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Curve):
            return False

        return (
            (self.a == other.a)
            and (self.b == other.b)
            and (self.p == other.p)
            and (self.q == other.q)
        )

    def __neq__(self, other) -> bool:
        return not (self == other)


def modinv(a: int, p: int):
    """
    Return the inverse of a modulo p.
    """
    return pow(a, -1, mod=p)


def bits(n: int):
    """
    Generates the bits of n starting from the LSB.
    """
    while n:
        yield n & 1
        n >>= 1


class Point:
    """
    Point represents a point on an elliptic curve.
    """

    def __init__(self, x: int, y: int, curve: Curve):
        """
        Construct a Point object with the given parameters.

        If the point is not on the given curve, a ValueError is raised.
        """
        if not curve.is_point(x, y):
            raise ValueError(f"Given point ({x}, {y}) not on given curve {curve}")
        self.x = x
        self.y = y
        self.curve = curve

    def double(self):
        """
        Double doubles this point and returns a new point representing
        the doubled value.
        This is equivalent to doing P + P for a point P on the curve.
        """
        return self + self

    def __eq__(self, other) -> bool:
        if isinstance(other, Infinity) or (not isinstance(other, Point)):
            return False

        return self.x == other.x and self.y == other.y and self.curve == other.curve

    def __slope(self, p, q) -> int:
        """
        Calculate the slope of the line connecting p and q, or the slope
        of the tangent to the curve if p == q.
        """
        if p == q:
            # Same point on the curve, should use m = (3x^2 + a) / 2y as slope,
            # otherwise the regular equation would divide by zero.
            # (3 * p.x**2 + self.curve.a) * mod_inv(2 * p.y, self.p)
            return (
                (3 * p.x**2 + self.curve.a) * modinv(2 * p.y, self.curve.p)
            ) % self.curve.p
        else:
            # different points on curve, should use m = (y_p - y_q) / (x_p - x_q)
            return ((p.y - q.y) * modinv(p.x - q.x, self.curve.p)) % self.curve.p

    def __add__(self, other):
        """
        Add this point to other, which is also a point on the same elliptic curve,
        returning a new point object.

        If the curves do not match, ValueError is raised.
        """

        # Adding the additive identity is a no-op
        if other == Infinity():
            return self

        if not isinstance(other, Point):
            raise ValueError(f"Can only add Point objects with other Point objects")

        if self.curve != other.curve:
            raise ValueError(f"Curves not equal: {self.curve} != {other.curve}")

        if self.x == other.x and self.y != other.y:
            return Infinity()

        m = self.__slope(self, other)

        # Calculate x_r = m^2 - x_p - x_q
        # Retrieved by solving the cubic equation where the line intersects with
        # the curve, with x_r, x_p, and x_q as the roots and x_r + x_p + x_q = -b/a
        # in the cubic equation.
        x_r = (m**2 - self.x - other.x) % self.curve.p

        # Calculate y_r = y_p + m(x_r - x_q)
        # y_r = -(self.y + m * (x_r - self.x)) % self.p
        y_r = (m * (self.x - x_r) - self.y) % self.curve.p

        # The result point is going to be at (x_r, y_r)
        return Point(x_r, y_r, self.curve)

    def __radd__(self, other):
        return self.__add__(other)

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __rmul__(self, scalar: int):
        if not isinstance(scalar, int):
            raise ValueError("Can only multiply by an integer")

        result = Infinity()
        addend = self

        for bit in bits(scalar):
            if bit == 1:
                result += addend
            addend += addend

        return result

        # Equivalent Implementation from "Understanding Cryptography"
        # by Paar and Pelzl
        # T = self
        # scalar_bits = bin(scalar).replace("0b", "")
        # for bit in scalar_bits[1:]:
        #     T += T
        #     if bit == "1":
        #         T += self
        # return T


class Infinity:
    """
    The infinity point is an imaginary point in the elliptic curve group that
    acts as the additive identity of the group, i.e
        Inf + P = P + Inf = P
    For all P in the elliptic curve group.
    """

    def __eq__(self, o):
        if isinstance(o, Infinity):
            return True
        return False

    def __ne__(self, o):
        return not (self == o)
