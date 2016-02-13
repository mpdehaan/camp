

from . member import Member

class PatternRouter(Member):

    def __init__(self, routing=None):
        assert type(routing) == list
        super().__init__()
