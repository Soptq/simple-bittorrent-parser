import unittest
from bencoding import *


class BencodingTest(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(bdecode(b"i3e"), 3)
        self.assertEqual(bdecode(b"i-3e"), -3)
        self.assertEqual(bdecode(b"i0e"), 0)
        self.assertEqual(bdecode(b"i3221e"), 3221)
        self.assertEqual(bdecode(b"i123e"), 123)
        with self.assertRaises(Exception):
            bdecode(b"i-0e")
        with self.assertRaises(Exception):
            bdecode(b"i-03e")
        with self.assertRaises(Exception):
            bdecode(b"i012e")

        self.assertEqual(bencode(0), b"i0e")
        self.assertEqual(bencode(-0), b"i0e")
        self.assertEqual(bencode(3), b"i3e")
        self.assertEqual(bencode(-3), b"i-3e")
        self.assertEqual(bencode(3221), b"i3221e")
        self.assertEqual(bencode(123), b"i123e")

    def test_string(self):
        self.assertEqual(bdecode(b"4:span"), b"span")
        self.assertEqual(bdecode(b"0:"), b"")
        self.assertEqual(bdecode(b"12:Middle Earth"), b"Middle Earth")

        self.assertEqual(bencode(b"span"), b"4:span")
        self.assertEqual(bencode(b""), b"0:")
        self.assertEqual(bencode(b"Middle Earth"), b"12:Middle Earth")

    def test_list(self):
        self.assertEqual(bdecode(b"le"), [])
        self.assertEqual(bdecode(b"l4:spam4:eggsi3eli3eee"),
                         [b"spam", b"eggs", 3, [3]])
        self.assertEqual(bdecode(b"li3eli3e4:spamli3e4:eggseee"),
                         [3, [3, b"spam", [3, b"eggs"]]])

        self.assertEqual(bencode([]), b"le")
        self.assertEqual(bencode([b"spam", b"eggs", 3, [3]]),
                         b"l4:spam4:eggsi3eli3eee")
        self.assertEqual(bencode([3, [3, b"spam", [3, b"eggs"]]]),
                         b"li3eli3e4:spamli3e4:eggseee")

    def test_dict(self):
        self.assertEqual(bdecode(b"de"), {})
        self.assertEqual(bdecode(b"d3:cow3:moo4:spam4:eggse"),
                         {b"cow": b"moo", b"spam": b"eggs"})
        self.assertEqual(bdecode(b"d4:spaml1:a1:bee"),
                         {b"spam": [b"a", b"b"]})
        self.assertEqual(bdecode(b"d9:publisher3:bob17:publisher-webpage15:www.example.com18:publisher.location4:homee"),
                         {b'publisher': b'bob', b'publisher-webpage': b'www.example.com', b'publisher.location': b'home'})

        self.assertEqual(bencode({}), b"de")
        self.assertEqual(bencode({b"cow": b"moo", b"spam": b"eggs"}),
                         b"d3:cow3:moo4:spam4:eggse")
        self.assertEqual(bencode({b"spam": [b"a", b"b"]}),
                         b"d4:spaml1:a1:bee")
        self.assertEqual(bencode({b'publisher': b'bob', b'publisher-webpage': b'www.example.com', b'publisher.location': b'home'}),
                         b"d9:publisher3:bob17:publisher-webpage15:www.example.com18:publisher.location4:homee")

if __name__ == '__main__':
    unittest.main()