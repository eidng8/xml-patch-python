#  GPLv3 https://www.gnu.org/licenses/gpl-3.0.en.html
#
#  Author: eidng8

from xml_patch.exceptions.base_error import BaseError


class InvalidPatchDirective(BaseError):
    """A patch directive could not be fulfilled
    because the given directives were not understood.
    """

    def __init__(self, action, message: str = None):
        super().__init__(action,
                         message if message else InvalidPatchDirective.__doc__)
