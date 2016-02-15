
from camp.core.chord import Chord
from camp.utils import loop_around
from camp.band.member import Member
from camp.playback.event import Event

class Chordify(Member):

    """
    Chordify takes a note producing member and turns it into chords of
    the given type.

    cf = Chordify(types=["major","major","minor"])

    In the above example, if connected to a scale player, or other note
    generating BandMember, we'd turn the input into a major chord for the first two beats
    and every third beat we'd use a minor chord.

    To do things consistently:

    cf = Chordify(types=["major"])

    There you go, all major chords.
    """

    # TODO: allow "None" as a type to just emit the note.

    def __init__(self, types=None, channel=None):

        """
        Constructor.  Read class docs.
        """

        super().__init__()

        assert type(types) == list
        self._which_chord = loop_around(types)
        self.channel = channel

    def on_signal(self, event, start_time, end_time):

        chord_typ = next(self._which_chord)
        chord = Chord(root=event.notes[0], typ=chord_typ)

        event.notes = chord.notes

        for send in self.sends:
            send.signal(event, start_time, end_time)
