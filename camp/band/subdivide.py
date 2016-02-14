
from camp.band.member import Member
from camp.utils import loop_around

class Subdivide(Member):

    """
    Repeats a signal a given number of amounts.

    For instance, if we have a quarter note pulse from the conductor:
    Q Q Q Q

    This will produce in each "Q" beat four signals, rather than one.
    SSSS SSSS SSSS SSSS

    If attached to something like ScalePlayer, it would repeat notes.
    """

    def __init__(self, channel=None, amounts=None):
        assert type(amounts) == list
        super().__init__()
        self.channel = channel
        if amounts is None:
            amounts = [2]
        self._subdivide_amounts = loop_around(amounts)

    def signal(self, event, start_time, end_time):

        delta = end_time - start_time
        slices = next(self._subdivide_amounts)

        each_slice_width = delta / slices
        new_start_time = start_time

        event = event.copy()
        event.add_flags(subdivide=slices)


        for send in self.sends:

            for slice_num in range(0,slices):

                new_end_time = new_start_time + each_slice_width

                if event.typ == 'beat':
                    event.time = new_start_time
                    send.signal(event, new_start_time, new_end_time)

                elif event.typ == 'note':
                    raise Exception("using subdivide with note is currently untested!")
                else:
                    raise Exception("AIEEE?")

                new_start_time = new_start_time + each_slice_width
