from camp.band.member import Member
from camp.playback.event import Event
from camp.utils import loop_around

class ScalePlayer(Member):

    def __init__(self, scales=None, lengths=None, note_durations=None, note_velocities=None, channel=None):
        assert type(scales) == list
        assert type(lengths) == list
        super().__init__()

        if note_velocities is None:
            note_velocities = [ 127 ]
        if note_durations is None:
            note_durations = [ 0.25 ]
        self.note_durations = note_durations
        self.note_velocities = note_velocities
        self.length_looper = loop_around(lengths)
        self.scale_looper = loop_around(scales)
        self.duration_looper = loop_around(note_durations)
        self.velocity_looper = loop_around(note_velocities)

        self.note_gen = self.note_generator()
        self.channel = channel

    def note_generator(self):
        # we're given a list of scales that we'll cycle between
        for scale in self.scale_looper:
            # each scale goes for a certain specified length
            # specified in a parallel array
            scale_length = next(self.length_looper)
            note_duration = next(self.duration_looper)
            note_velocity = next(self.velocity_looper)
            for note in scale.generate(length=scale_length):
                note.duration = note_duration
                note.velocity = note_velocity
                yield note

    def on_signal(self, event, start_time, end_time):

        if event.typ == 'beat':

            note = next(self.note_gen)

            # FIXME: how to make this code so it doesn't have to live in each class that generates
            # note expressions so it can use the subdivider?  Want something like note.apply_event_flags(event) I think.
            
            if event.flags.get('subdivide', 0) > 1:
                note.duration = note.duration / event.flags.get('subdivide')

            evt = Event(typ='note', velocity=127, channel=event.channel, notes=[note], time=start_time)

            for send in self.sends:
                send.signal(evt, start_time, end_time)
