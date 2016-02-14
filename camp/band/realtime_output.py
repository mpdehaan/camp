
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


    def __init__(self, timeline=None, bpm=None, time_boredom_seconds=60):

        assert timeline is not None
        assert bpm is not None

        self.absolute_start_time = time.time()

        # a flag that says if all musicians put their instruments down, we can stop conducting.
        self.got_events = False
        self.time_boredom_seconds = time_boredom_seconds

        self.last_timestamp = time.time()

        assert timeline is not None
        self.timeline = timeline
        self.bpm = bpm

        # FIXME: this needs to be calculated off of tempo to be more
        # intuitive, change to BPM shortly.

        self.whole_note_length = ( 60 / 120) * 4

        super().__init__()

    def on_signal(self, event, start_time, end_time):

        now = time.time()

        if now - self.time_boredom_seconds > self.absolute_start_time:
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
            self.timeline.add_event(event)

            # buglet - technically we don't need to cause a note off if it's going to be legato
            # triggered later, this may introduce some minor indiosyncracies but is not a large
            # enough concern to deal with now

            # buglet, this technically requires block chords when sending events with a notes array
            # if this is a problem we can change the code to always send one note per event later.
            # easy enough.

            # the main code doesn't have to think in terms of note off events because they
            # have durations, but because the code interpreting the MIDI timeline does, we create
            # those events here, at the last possible point in the chain, to avoid most of the
            # code needing to think about them.
            event_off = event.copy()
            event_off.off = True
            offset = event.notes[0].duration * self.whole_note_length
            event_off.time = event.time + offset
            #print("OFF EVENT is %s in the future" % (offset))
            self.timeline.add_event(event_off)

            self.got_events = True

        else:
            raise Exception("uncoded event type - FIXME? - %s" % event.typ)
