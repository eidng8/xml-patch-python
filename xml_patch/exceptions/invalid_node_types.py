from xml_patch.exceptions.base_error import BaseError


class InvalidNodeTypes(BaseError):
    """The node types of a <replace> operation did
    not match, i.e., for example, the 'sel' selector locates an
    element but the replaceable content is of text type.  Also, a
    <replace> operation may locate a unique element, but replaceable
    content had multiple nodes.
    """

    def __init__(self, action, message: str = None):
        super().__init__(action,
                         message if message else InvalidNodeTypes.__doc__)
