from camp.band.member import Member
from camp.playback.event import Event
from camp.utils import loop_around

class ScalePlayer(Member):

    """
    The scale player repeats one or more scales.

    For instance:

    sp = ScalePlayer(scales=["c4 major", "c3 major", lengths=[3,3], note_velocities=[127,64], note_durations=[0.25,0.125,0.125])

    It's not limited to just one scale, and while playing a scale the velocity of notes and durations of notes can be varied

    In the above example, the following notes would play

    c4 - velocity 127, duration=0.25
    d4 - velocity 64, duration=0.125
    e4 - velocity 127, duration=0.125
    c3 - velocity 64, duration=0.25
    d3 - velocity 127, duration=0.125
    e3 - velocity 64, duration=0.125
    f3 - velocity 127, duration=0.125

    A simpler incantation:

    sp = ScalePlayer(scales=["c4 chromatic", lengths=[12], note_velocities=[127], note_durations=[0.25])

    Plays the chromatic scale in equally maximally loud quarter notes.

    After exhausting the cycle, then the cycle would repeat endlessly as specified.
    See more in the constructor documentation.

    If the scale player is NOT connected to an output, it can still be used to send messages about the current
    scale to something like the RomanPlayer, which takes incoming events that have scale data and then applies
    transforms on it.
    """

    def __init__(self, scales=None, lengths=None, note_durations=None, note_velocities=None, channel=None):

        """
        scales - a list of what scales to play
        lengths - how many notes to play in each scale
        note_durations - a list of how long should each note be
        note_velocities - how loud should each note be
        channel - what MIDI channel to send to?
        """


        assert type(scales) == list
        assert type(lengths) == list
        super().__init__()

        # if velocities are not specified, play all notes maximally loud
        if note_velocities is None:
            note_velocities = [ 127 ]
        # if no durations are specified, everything is a quarter note
        if note_durations is None:
            note_durations = [ 0.25 ]
        self.note_durations = note_durations
        self.note_velocities = note_velocities

        # use the loop_around iterator to make sure our cycle of notes
        # never runs out.

        # FIXME: TODO: implement a "direction" array that allows a scale
        # to be played backwards.

        self.length_looper = loop_around(lengths)
        self.scale_looper = loop_around(scales)
        self.duration_looper = loop_around(note_durations)
        self.velocity_looper = loop_around(note_velocities)

        # the note generator is also a generator, but a lot more complicated
        self.note_gen = self.note_generator()

        # be sure we record the output MIDI channel preference
        self.channel = channel

        # keep track of the current scale being iterated over
        self.current_scale = None

    def note_generator(self):

        """"
        The note generator is a generator that tells the consumer of this plugin
        what note to play for each beat.
        """

        # we're given a list of scales that we'll cycle between
        for scale in self.scale_looper:

            self.current_scale = scale

            # each scale goes for a certain specified length
            # specified in a parallel array, same for velocity and
            # note duration per note.
            scale_length = next(self.length_looper)
            note_duration = next(self.duration_looper)
            note_velocity = next(self.velocity_looper)

            # use the scale classes's generate method - also an iterator
            # to get the actual notes, then yield them to the caller.
            for note in scale.generate(length=scale_length):
                note.duration = note_duration
                note.velocity = note_velocity
                yield note

    def on_signal(self, event, start_time, end_time):

        """
        The callback for the ScalePlayer class.
        """

        if event.typ == 'beat':

            # respond to a beat by playing the next specified scale note.

            note = next(self.note_gen)

            # TODO: FIXME: how to make this code so it doesn't have to live in each class that generates
            # note expressions so it can use the subdivider?  Want something like note.apply_event_flags(event) I think.
            if event.flags.get('subdivide', 0) > 1:
                note.duration = note.duration / event.flags.get('subdivide')
            evt = Event(typ='note', velocity=127, channel=event.channel, notes=[note], time=start_time)
            evt.add_flags(scale=self.current_scale)

            # pass along the note down the chain.  Now that the note is passed along we don't have to repeat
            # the 'beat' signal.

            for send in self.sends:
                send.signal(evt, start_time, end_time)
