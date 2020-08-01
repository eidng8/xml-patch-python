#  GPLv3 https://www.gnu.org/licenses/gpl-3.0.en.html
#
#  Author: eidng8

from lxml import etree


def is_attribute_node(target) -> bool:
    """Check whether the given target is an attribute.

    Parameters
    ==========
        target ([any]): Target to be checked.

    Returns
    =======
        bool: Returns `True` if target is an attribute.
    """
    return hasattr(target, 'is_attribute') and target.is_attribute


def is_text_node(target) -> bool:
    """Check whether the given target is a text node.

    Parameters
    ==========
        target ([any]): Target to be checked.

    Returns
    =======
        bool: Returns `True` if target is a text node.
    """
    return hasattr(target, 'is_text') and target.is_text


def has_no_child_element(target) -> bool:
    """Check whether the given target doesn't have any child element.

    Parameters
    ==========
        target ([any]): Target to be checked.

    Returns
    =======
        bool: Returns `True` if target doesn't have any child element.
    """
    return etree.iselement(target) and 0 == len(target)
