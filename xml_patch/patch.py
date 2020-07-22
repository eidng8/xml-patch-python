from copy import deepcopy
from logging import info
from lxml import etree
from os import path

from xml_patch.action_replace import ActionReplace


class Patch:
    """Handles RFC-5261 XML patch operations.
    Properties
    ----------
    source : str
        The input XML document, which will be patched. By default, content
        here will be directly mutated. To keep the source content unchanged,
        set `keep_source` to `True` when initializing.
    diff : str
        The diff (patch) XML document, which will be applied. By default, this
        is the same as `self.source`. To make this a clone of the source, set
        `keep_source` to `True` when initializing.
    patched : str
        The patched (output) XML document.
    """

    def __init__(self, diff_path: str, src_path: str, keep_source: bool = False):
        """
        Parameters
        ----------
        diff_path : str
            Absolute path to the diff (patch) XML file.
        src_path : str
            Absolute path to the source XML file to be patched.
        keep_source: bool = False
            Whether the source XML document should be kept untouched. Setting
            this to be `True` will consume more memory.
        """
        self._source: etree.ElementTree = etree.parse(src_path)
        self._patched: etree.ElementTree = deepcopy(
            self._source) if keep_source else self._source
        xsd = path.join(path.abspath(path.dirname(__file__)), 'diff.xsd')
        parser = etree.XMLParser(schema=etree.XMLSchema(file=xsd))
        self._diff: etree.ElementTree = etree.parse(diff_path, parser=parser)

    @property
    def source(self) -> str:
        return self._source

    @property
    def diff(self) -> str:
        return self._diff

    @property
    def patched(self) -> str:
        return self._patched

    def apply(self) -> etree.ElementTree:
        """Apply all patch operations."""
        for action in self._diff.getroot():
            self._apply_action(action)
        return self.patched

    def _apply_action(self, action: etree.Element):
        """Apply one operation."""
        info(etree.tostring(action))
        sel: str = action.get('sel')
        target: etree.Element = self._patched.xpath(sel)
        self._apply_replace(action, target[0])

    def _apply_replace(self, action: etree.Element, target: etree.Element):
        ActionReplace(action, target).apply()
