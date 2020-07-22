import unittest
from os import path
from lxml import etree
from xml_patch.patch import Patch


class TestPatch(unittest.TestCase):
    def setUp(self):
        self.base = path.abspath(path.join(path.dirname(__file__), 'data'))
        self.diff = path.join(self.base, '1A.diff.xml')
        self.src = path.join(self.base, '1A.xml')
        self.patch = Patch(self.diff, self.src)

    def test_init(self):
        actual = etree.tostring(self.patch.source)
        self.assertEqual(actual, b'<a>x<b>y</b>z</a>')
        actual = etree.tostring(self.patch.patched)
        self.assertEqual(actual, b'<a>x<b>y</b>z</a>')
        actual = etree.tostring(self.patch.diff)
        root = self.patch.diff.getroot()
        self.assertEqual(root.tag, 'diff')
        self.assertEqual(root.getchildren()[0].tag, 'replace')

    def test_apply(self):
        patched = self.patch.apply()
        actual = etree.tostring(patched)
        self.assertEqual(actual, b'<a>x<c>y</c>z</a>')


if __name__ == '__main__':
    unittest.main()
