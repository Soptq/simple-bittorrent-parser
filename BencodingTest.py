import unittest
from Bencoding import *


class BencodingTest(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(bdecode("i3e"), 3)
        self.assertEqual(bdecode("i-3e"), -3)
        self.assertEqual(bdecode("i0e"), 0)
        self.assertEqual(bdecode("i3221e"), 3221)
        with self.assertRaises(Exception):
            bdecode("i-0e")
        with self.assertRaises(Exception):
            bdecode("i-03e")
        with self.assertRaises(Exception):
            bdecode("i012e")

    def test_string(self):
        self.assertEqual(bdecode("4:span"), "span")
        self.assertEqual(bdecode("0:"), "")

    def test_list(self):
        self.assertEqual(bdecode("le"), [])
        self.assertEqual(bdecode("l4:spam4:eggsi3eli3eee"),
                         ["spam", "eggs", 3, [3]])
        self.assertEqual(bdecode("li3eli3e4:spamli3e4:eggseee"),
                         [3, [3, "spam", [3, "eggs"]]])

    def test_dict(self):
        self.assertEqual(bdecode("de"), {})
        self.assertEqual(bdecode("d3:cow3:moo4:spam4:eggse"),
                         {"cow": "moo", "spam": "eggs"})
        self.assertEqual(bdecode("d4:spaml1:a1:bee"),
                         {"spam": ["a", "b"]})
        self.assertEqual(bdecode("d9:publisher3:bob17:publisher-webpage15:www.example.com18:publisher.location4:homee"),
                         {'publisher': 'bob', 'publisher-webpage': 'www.example.com', 'publisher.location': 'home'})


if __name__ == '__main__':
    unittest.main()