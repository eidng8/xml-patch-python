import unittest
from os import path

from lxml import etree

from xml_patch.action_replace import ActionReplace
from xml_patch.exceptions.unlocated_node import UnlocatedNode


class TestActionReplace(unittest.TestCase):
    def test_init(self):
        src = etree.fromstring('<a>x<b>y</b>z</a>')
        patch = etree.fromstring('<replace sel="/a/b"><c>w</c></replace>')
        action = ActionReplace(patch, src)
        actual = etree.tostring(action._target)
        self.assertEqual(actual, b'<a>x<b>y</b>z</a>')
        actual = etree.tostring(action._action)
        self.assertEqual(actual, b'<replace sel="/a/b"><c>w</c></replace>')

    def test_apply_element(self):
        src = etree.fromstring('<a>x<b>y</b>z</a>')
        patch = etree.fromstring('<replace sel="/a/b"><c>w</c></replace>')
        ActionReplace(patch, src.getchildren()[0]).apply()
        actual = etree.tostring(src)
        self.assertEqual(actual, b'<a>x<c>w</c>z</a>')

    def test_apply_attribute(self):
        src = etree.fromstring('<a><b attr="abc"/></a>')
        patch = etree.fromstring(
            '<replace sel="/a/b/@attr">cba</replace>')
        ActionReplace(patch, src.xpath('/a/b/@attr')).apply()
        actual = etree.tostring(src)
        self.assertEqual(actual, b'<a><b attr="cba"/></a>')

    def test_apply_text(self):
        src = etree.fromstring('<a>abc</a>')
        patch = etree.fromstring('<replace sel="/a/text()">cba</replace>')
        ActionReplace(patch, src.xpath('/a/text()')).apply()
        actual = etree.tostring(src)
        self.assertEqual(actual, b'<a>cba</a>')

    def test_multiple_targets_should_throw_error(self):
        src = etree.fromstring('<a><b/><b/></a>')
        patch = etree.fromstring('<replace sel="/a/b"><c>w</c></replace>')
        action = ActionReplace(patch, src.xpath('/a/b'))
        self.assertRaises(UnlocatedNode, action.apply)


if __name__ == '__main__':
    unittest.main()
