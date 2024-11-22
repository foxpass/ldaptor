"""
    Test cases for ldaptor.encoder module
"""

from twisted.trial import unittest


import ldaptor._encoder


class WireableObject:
    """
    Object with bytes representation as a constant toWire value
    """

    def toWire(self):
        return b"wire"


class TextObject(ldaptor._encoder.TextStrAlias):
    """
    Object with human readable representation as a constant getText value
    """

    def getText(self):
        return "text"


class EncoderTests(unittest.TestCase):
    def test_wireable_object(self):
        """
        to_bytes function use object`s toWire method
        to get its bytes representation if it has one
        """
        obj = WireableObject()
        self.assertEqual(ldaptor._encoder.to_bytes(obj), b"wire")

    def test_unicode_object(self):
        """
        unicode string is encoded to utf-8 if passed
        to to_bytes function
        """
        obj = "unicode"
        self.assertEqual(ldaptor._encoder.to_bytes(obj), b"unicode")

    def test_bytes_object(self):
        """
        byte string is returned without changes
        if passed to to_bytes function
        """
        obj = b"bytes"
        self.assertEqual(ldaptor._encoder.to_bytes(obj), b"bytes")

    def test_int_object(self):
        """
        integer is converted to a string representation, then encoded to bytes
        if passed to to_bytes function
        """
        obj = 42
        self.assertEqual(ldaptor._encoder.to_bytes(obj), b"42")

    def test_get_strings(self):
        """
            Get tuple of available string values
            (byte string and unicode string) for
            given value
        """
        tests = {
            b"42": (b"42", "42"),
            "42": ("42", b"42"),
            "test": ("test", b"test"),
            b"test": (b"test", "test"),
            b"C\x88c\xac\x99\xffIE\xabw|\xf0\xb1<\xced": (b"C\x88c\xac\x99\xffIE\xabw|\xf0\xb1<\xced",),
            b"\xff": (b"\xff",),
            b"\x8f": (b"\x8f",),
            b"\x7f": (b"\x7f", "\x7f"), # b"\x7f" is a valid utf-8 byte
        }
        for test, answer in tests.items():
            result = ldaptor._encoder.get_strings(test)
            self.assertEqual(result, answer)

class WireStrAliasTests(unittest.TestCase):
    def test_toWire_not_implemented(self):
        """
        WireStrAlias.toWire is an abstract method and raises NotImplementedError
        """
        obj = ldaptor._encoder.WireStrAlias()
        self.assertRaises(NotImplementedError, obj.toWire)


class TextStrAliasTests(unittest.TestCase):
    def test_deprecation_warning(self):
        str(TextObject())
        msg = (
            "TextObject.__str__ method is deprecated and will not be used "
            "for getting human readable representation in the future "
            "releases, use TextObject.getText instead"
        )
        warnings = self.flushWarnings()
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0]["category"], DeprecationWarning)
        self.assertEqual(warnings[0]["message"], msg)

    def test_getText_not_implemented(self):
        """
        TextStrAlias.getText is an abstract method and raises NotImplementedError
        """
        obj = ldaptor._encoder.TextStrAlias()
        self.assertRaises(NotImplementedError, obj.getText)
