from unittest import TestCase

from crypto import Curve, Point


# TODO: add more tests
class TestCurve(TestCase):
    def setUp(self):
        self.curve = Curve(2, 2, 17)

    def test_is_point(self):
        test_cases = [
            Point(x=6, y=3, curve=self.curve),
            Point(x=10, y=6, curve=self.curve),
            Point(x=3, y=1, curve=self.curve),
            Point(x=9, y=16, curve=self.curve),
            Point(x=16, y=13, curve=self.curve),
            Point(x=0, y=6, curve=self.curve),
            Point(x=13, y=7, curve=self.curve),
            Point(x=7, y=6, curve=self.curve),
            Point(x=7, y=11, curve=self.curve),
            Point(x=13, y=10, curve=self.curve),
            Point(x=0, y=11, curve=self.curve),
            Point(x=16, y=4, curve=self.curve),
            Point(x=9, y=1, curve=self.curve),
            Point(x=3, y=16, curve=self.curve),
            Point(x=10, y=11, curve=self.curve),
            Point(x=6, y=14, curve=self.curve),
            Point(x=5, y=16, curve=self.curve),
        ]
        for point in test_cases:
            self.assertTrue(self.curve.is_point(point.x, point.y))
