
from camp.band.member import Member
import time

class RealtimeOutput(Member):

    """
    Somewhat of a misnomer, the realtime output doesn't really output anything.
    However, it does throw away events that aren't musically relevant, and records
    whether the performance is done or not by way of the special 'got_events' flag.

    The actual processing of the realtime timeline and actual realtime work is mainly
    in the conductor class.  This then, could technically be called "Audience" and may
    be renamed.
    """


    def __init__(self, timeline=None, bpm=None, time_boredom_seconds=500):

        assert timeline is not None
        assert bpm is not None

        self.start_time = time.time()

        # a flag that says if all musicians put their instruments down, we can stop conducting.
        self.got_events = False
        self.time_boredom_seconds = time_boredom_seconds

        self.last_timestamp = time.time()

        assert timeline is not None
        self.timeline = timeline
        self.bpm = bpm

        # FIXME: this needs to be calculated off of tempo to be more
        # intuitive, change to BPM shortly.

        self.whole_note_length = (240 / bpm)

        super().__init__()

    def on_signal(self, event):

        now = time.time()

        if now - self.time_boredom_seconds > self.start_time:
            self.got_events = False

        if event.typ == 'beat':
            self.last_timestamp = now

        elif event.typ == 'note':


            # BOOKMARK - STOPPING PLACE
            # FIXME: the event has a NOTES array.  In the event of something that does not
            # match the quarter note BEAT length, we'll want to send notes that already
            # contain an offset and duration. We also need to investigate some bugs in the note off impl.

            # event types will be things like NOTE, CONTROL_CHANGE, and SILENCE
            # lack of any events will signal performance end.
            self.timeline.add_event(event, now_time=self.last_timestamp)

            # buglet - technically we don't need to cause a note off if it's going to be legato
            # triggered later, this may introduce some minor indiosyncracies but is not a large
            # enough concern to deal with now


            # buglet, this technically requires block chords when sending events with a notes array
            # if this is a problem we can change the code to always send one note per event later.
            # easy enough.

            event_off = event.copy()
            event_off.off = True
            offset = event.notes[0].duration * self.whole_note_length

            self.timeline.add_event(event_off, now_time = self.last_timestamp + offset)

            self.got_events = True

        else:
            raise Exception("uncoded event type - FIXME? - %s" % event.typ)
