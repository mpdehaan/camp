from camp.band.member import Member
from camp.playback.event import Event
from camp.utils import loop_around
from camp.notation.roman import Roman

class RomanPlayer(Member):

    """
    The roman player listens to an incoming note signal and then only really pays attention to the velocity, duration, and scale data.
    The actual note played depends on a symbol off the scale, whether a note or a chord.

    As such, a ScalePlayer makes the most sense to have higher up in the chain.

    For instance:

    r = RomanPlayer(symbols=["I 2 3 4 IV 2 3 4 iii"])
    """

    def __init__(self, symbols=None, channel=None):

        """
        scales - a list of what scales to play
        lengths - how many notes to play in each scale
        note_durations - a list of how long should each note be
        note_velocities - how loud should each note be
        channel - what MIDI channel to send to?
        """


        assert type(symbols) == list
        super().__init__()

        self.symbol_looper = loop_around(symbols)
        self.channel = channel

    def on_signal(self, event, start_time, end_time):

        """
        The callback for the ScalePlayer class.
        """

        if event.typ == 'note':

            # respond to a beat by playing the next specified scale note.

            scale = event.flags.get('scale',None)
            if scale is None:
                raise Exception("missing scale data from note signal, something wrong here")

            symbol = next(self.symbol_looper)
            r = Roman(scale=scale)
            notes = r.do_notes(symbol)

            # TODO: FIXME: velocity information is part of the note and probably needs to be copied, make this cleaner
            velocity = event.notes[0].velocity

            # TODO: FIXME: how to make this code so it doesn't have to live in each class that generates
            # note expressions so it can use the subdivider?  Want something like note.apply_event_flags(event) I think.
            if event.flags.get('subdivide', 0) > 1:
                for note in notes:
                    note.duration = note.duration / event.flags.get('subdivide')
            # this indicates a problem.  Event should not have velocity.  NOTES have velocity.  FIXME.
            #for note in notes:
            #    note.velocity = velocity


            evt = Event(typ='note', channel=event.channel, notes=notes, time=start_time, flags=event.flags, velocity=127)

            # pass along the note down the chain.  Now that the note is passed along we don't have to repeat
            # the 'beat' signal.
            for send in self.sends:
                send.signal(evt, start_time, end_time)

        else:

            raise Exception("the roman player doesn't work with beat signals and requires a note, connect to a BandMember, not the Conductor")
