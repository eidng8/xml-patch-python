#  GPLv3 https://www.gnu.org/licenses/gpl-3.0.en.html
#
#  Author: eidng8

from xml_patch.exceptions.base_error import BaseError


class UnlocatedNode(BaseError):
    """A single unique node (typically an element) could
    not be located with the 'sel' attribute value.  Also, the location
    of multiple nodes can lead to this error.
    """

    def __init__(self, action, message: str = None):
        super().__init__(action, message if message else UnlocatedNode.__doc__)
