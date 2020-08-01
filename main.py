#  GPLv3 https://www.gnu.org/licenses/gpl-3.0.en.html
#
#  Author: eidng8

from lxml import etree

from xml_patch.patch import Patch

patch = Patch('tests/data/1A.diff.xml', 'tests/data/1A.xml')
print(etree.tostring(patch.apply()))
