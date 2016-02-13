

from . member import Member

class PatternRouter(Member):

    def __init__(self, routing=None, channel=None):
        assert type(routing) == list
        super().__init__()
        self.channel = channel

# FIXME
