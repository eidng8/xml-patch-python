from lxml import etree
from patch import Patch

patch = Patch('tests/data/1A.diff.xml', 'tests/data/1A.xml')
print(etree.tostring(patch.apply()))
