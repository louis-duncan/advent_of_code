from unittest import TestCase
from day_15 import string_hash, Label


class Test(TestCase):
    def test_string_hash(self):
        checks = [
            ["HASH", 52],
            ["rn=1", 30],
            ["cm-", 253],
            ["qp=3", 97],
            ["cm=2", 47],
            ["qp-", 14],
            ["pc=4", 180],
            ["ot=9", 9],
            ["ab=5", 197],
            ["pc-", 48],
            ["pc=6", 214],
            ["ot=7", 231]
        ]
        for string, exp in checks:
            self.assertEqual(exp, string_hash(string), msg=f"String '{string}' did not hash to expected value")


class TestLabel(TestCase):
    def test_hash(self):
        d = {Label("hfc"): 1}
        self.assertEqual(1, d[Label("hfc")])
        d[Label("pel")] = 2
        self.assertEqual(2, d[Label("hfc")])
