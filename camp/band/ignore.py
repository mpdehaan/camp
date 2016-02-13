
from . member import Member

class Filter(Member):

    def __init__(self, filter=None):
        assert type(filter) == list
        super().__init__()
