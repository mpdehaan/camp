"""
Copyright 2016, Michael DeHaan <michael.dehaan@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from camp.band.members.member import Member
from camp.playback.timeline import Timeline

class Performance(Member):

    """
    Somewhat of a misnomer, the realtime output doesn't really output anything.
    However, it does throw away events that aren't musically relevant, and records
    whether the performance is done or not by way of the special 'got_events' flag.

    The actual processing of the realtime timeline and actual realtime work is mainly
    in the conductor class.  This then, could technically be called "Audience" and may
    be renamed.
    """


    def __init__(self, bpm=None, stop_seconds=60):

        # TODO: stop_seconds is nice, but we don't we really want stop_beats or stop_bars
        # or something?


        assert bpm is not None

        self.timeline = Timeline()

        self.got_events = False # if we don't get any musical events, the performance will stop
        self.stop_seconds = stop_seconds
        self.bpm = bpm

        # FIXME: this needs to be calculated off of tempo, change to BPM shortly.

        self.whole_note_length = ( 60 / 120) * 4

        super().__init__()

    def on_signal(self, event, start_time, end_time):

        print(event)

        if event.duration is None:
            event.duration = 0.25
        if event.velocity is None:
            event.velocity = 127
        if event.notes is None:
            print("NO NOTES?")
            return



        if end_time >= self.stop_seconds:
            self.got_events = False
            return

        event = event.copy()
        self.timeline.add_event(event)
        event_off = event.copy()

        event_off.off = True

        # if we passed through the subdivide middleware shorten the length
        # before we play it.
        subdivide = event_off.flags.get('subdivide', 1)
        event_off.duration = event_off.duration / subdivide

        offset = event.duration * self.whole_note_length
        event_off.time = event.time + offset
        #print("OFF EVENT is %s in the future" % (offset))
        self.timeline.add_event(event_off)
        self.got_events = True
