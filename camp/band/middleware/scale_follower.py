from camp.band.member import Member
from camp.playback.event import Event
from camp.utils import loop_around

class ScaleFollower(Member):

    """
    Plays along the current scale for a specified length of notes
    before restarting the scale.

    Usage:

    s = ScaleFollower(lengths=[7,14,7])

    This would play the current scale for 7 notes (rolling around if the scale
    was generated too short), then 14 notes, then 7.  If the scale changed
    while playing back it would start over at the beginning of the new scale.
    """

    def __init__(self, lengths=None, channel=None):



        assert type(lengths) == list
        super().__init__()

        self.lengths_looper = loop_around(lengths)
        if channel is not None:
            self.channel = channel

        self.previous_scale = None
        self.current_scale = None
        self.generator = None

    def get_note_generator(self):

        if self.current_scale != self.previous_scale:
            self.generator = self.current_scale.generate(length=next(self.lengths_looper))
        return self.generator

    def on_signal(self, event, start_time, end_time):

        self.current_scale = event.flags.get('scale',None)
        if self.current_scale is None:
            raise Exception("missing scale data from note signal, something wrong here")

        note_gen = self.get_note_generator()
        note = next(note_gen)
        event.notes = [ note ]

        self.previous_scale = self.current_scale

        for send in self.sends:
            send.signal(event, start_time, end_time)
