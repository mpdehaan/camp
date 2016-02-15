
from camp.band.members.member import Member
from camp.utils import loop_around

class Transpose(Member):


    def __init__(self, channel=None, octaves=None):

        # TODO: later also support step transpositions
        # or even grabbing the next note in the scale

        assert type(octaves) == list

        super().__init__()

        self.octaves_looper = loop_around(octaves)

        if channel is not None:
            self.channel = channel


    def on_signal(self, event, start_time, end_time):

        if event.notes == None:
            raise Exception("transpose requires notes in the pipeline")

        amount = next(self.octaves_looper)
        for (i,note) in enumerate(event.notes):
            event.notes[i] = event.notes[i].transpose(octaves=amount)

        for send in self.sends:
            send.signal(event, start_time, end_time)
