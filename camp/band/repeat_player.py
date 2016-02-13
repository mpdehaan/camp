
from . member import Member

class RepeatPlayer(Member):

    def __init__(self, notes=[]):
        assert type(notes) == list
        super().__init__()
