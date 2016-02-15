from camp.band.members.member import Member
from camp.utils import loop_around
from camp.notation.roman import Roman as RomanNotation

class Roman(Member):

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
        if channel is not None:
            self.channel = channel

    def on_signal(self, event, start_time, end_time):


        print("ROMAN!")

        scale = event.flags.get('scale',None)
        if scale is None:
            raise Exception("missing scale data from note signal, something wrong here")

        symbol = next(self.symbol_looper)
        event.notes = RomanNotation(scale=scale).do_notes(symbol)

        for send in self.sends:
            send.signal(event, start_time, end_time)
