import unittest
from os import path
from lxml import etree
from xml_patch.action_replace import ActionReplace


class TestActionReplace(unittest.TestCase):
    def test_init(self):
        src = etree.fromstring('<a>x<b>y</b>z</a>')
        patch = etree.fromstring('<replace sel="/a/b"><c>w</c></replace>')
        action = ActionReplace(patch, src)
        actual = etree.tostring(action._target)
        self.assertEqual(actual, b'<a>x<b>y</b>z</a>')
        actual = etree.tostring(action._action)
        self.assertEqual(actual, b'<replace sel="/a/b"><c>w</c></replace>')

    def test_apply(self):
        src = etree.fromstring('<a>x<b>y</b>z</a>')
        patch = etree.fromstring('<replace sel="/a/b"><c>w</c></replace>')
        ActionReplace(patch, src.getchildren()[0]).apply()
        actual = etree.tostring(src)
        self.assertEqual(actual, b'<a>x<c>w</c>z</a>')


if __name__ == '__main__':
    unittest.main()
