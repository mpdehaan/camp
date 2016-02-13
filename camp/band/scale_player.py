from camp.band.member import Member
from camp.playback.event import Event
from camp.utils import loop_around

class ScalePlayer(Member):

    def __init__(self, scales=None, lengths=None, channel=None):
        assert type(scales) == list
        assert type(lengths) == list
        super().__init__()

        self.length_looper = loop_around(lengths)
        self.scale_looper = loop_around(scales)
        self.note_gen = self.note_generator()
        self.channel = channel

    def note_generator(self):
        # we're given a list of scales that we'll cycle between
        for scale in self.scale_looper:
            # each scale goes for a certain specified length
            # specified in a parallel array
            actual_len = next(self.length_looper)
            for note in scale.generate(length=actual_len):
                yield note

    def on_signal(self, event):

        if event.typ == 'beat':

            note = next(self.note_gen)
            evt = Event(typ='note', velocity=127, channel=event.channel, notes=[note])

            for send in self.sends:
                send.signal(evt)
