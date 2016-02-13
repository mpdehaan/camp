
from . member import Member

class Filter(Member):

    def __init__(self, filter=None, channel=None):
        assert type(filter) == list
        super().__init__()
        self.channel = channel
