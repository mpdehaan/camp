
from camp.band.member import Member
import time

class RealtimeOutput(Member):

    """
    Somewhat of a misnomer, the realtime output doesn't really output anything.
    However, it does throw away events that aren't musically relevant, and records
    whether the performance is done or not by way of the special 'got_events' flag.

    The actual processing of the realtime timeline and actual realtime work is mainly
    in the conductor class.
    """


    def __init__(self, timeline=None):

        assert timeline is not None

        # a flag that says if all musicians put their instruments down, we can stop conducting.
        self.got_events = False

        self.last_timestamp = 0

        assert timeline is not None
        self.timeline = timeline

        super().__init__()

    def signal(self, event):

        print("realtime_output :: signaled :: %s" % event)

        if event.typ == 'beat':
            print("realtime_output :: beat")
            self.last_timestamp = time.time()

        elif event.typ != 'beat':
            print("realtime_output :: non-beat")

            # event types will be things like NOTE, CONTROL_CHANGE, and SILENCE
            # lack of any events will signal performance end.

            self.timeline.add_event(event, now_time=self.last_timestamp)
            self.got_events = True
