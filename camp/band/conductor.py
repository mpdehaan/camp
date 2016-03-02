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

from camp.playback.realtime import Realtime
from camp.playback.event import Event
from camp.band.members.performance import Performance

class Conductor(object):

    """
    The conductor oversees a performance.

    Don't think of this metaphor too literally.  This isn't a real world model, exactly.

    With each wave of the baton (every quarter note, a beat in "bpm"), the conductor sends a beat event down toward listening band members.
    This is just an event without data in it.  No notes. No velocity.  But it does mark the start of the quarter note with the time field.

    Each member (who in turn can talk to other members) copy the event, and modify it.  They could add or change the notes, set a velocity,
    or set a duration.

    If the conductor is not conducting fast enough, a subdivide plugin can speed it up.

    The performance is, counter-intuitively, also a band-member, taking high level note objects and cleaning them  up, making
    sure time divisions are appropriate, and note events are in the pipeline.  The conductor knows about the performance object
    and asks for it's timeline.

    The timeline object is responsible for the "clock" of the system and is the key to playback.
    """

    def __init__(self, signal=None, performance=None):

        """
        Constructor.

        signal - a list of band members that are keyed into 'beats'.  If not listed here the band
        member needs to be keyed into other band members or they won't play.

        performance - the last note in the event chains that both owns the timeline and makes sure
        band members feeding into the performance impact the timeline.
        """

        assert type(signal) == list
        print("PERF=%s" % performance)

        assert type(performance) == Performance

        self.realtime = Realtime()
        self.signal = signal
        #self.timeline = timeline
        self.performance = performance
        self.timeline = self.performance.timeline
        self.bpm = self.performance.bpm
        self.quarter_note_length = 60 / self.bpm

    def _band_event_to_midi_events(self, event):
        """
        Given a camp.band.playback.event Event, return the list of MIDI events associated with it.
        """
        midi_events = []
        if event.notes is not None:
            if event.channel is None:
                raise Exception("missing channel assignment somewhere in the pipeline")
            for note in event.notes:
                if event.off == True:
                    midi_events.append(self.realtime.note_off(event.channel, note.note_number(), event.velocity))
                else:
                    midi_events.append(self.realtime.note_on(event.channel, note.note_number(), event.velocity))
            return midi_events
        else:
            raise Exception("do not understand non-note events just yet: %s" % event)

    def handle_band_event(self, event):
        """
        Given a camp.band.playback.event Event, play the interpretation of it as MIDI notes.
        """

        midi_events = self._band_event_to_midi_events(event)
        for midi_event in midi_events:
            self.realtime.play_event(midi_event)

    def start(self):

        """
        The start method begins a performance.  The performance will end on it's own
        or when the user Control-C's it.
        """

        running = True
        now_time = 0

        while running:

            print("-- BEAT")
            # we're just going to send a beat signal, the members of the band
            # decide whether to play any notes.  A beat is an inaudible event.
            beat = Event(time=now_time, duration=0.25)

            # if the output ever does not produce events in a time slice, the
            # playback will stop.  We may implement a 'silent' event to keep it
            # going, though this is based on the idea of generators - keep playing
            # until the data runs out
            self.performance.got_events = False

            # the beat happens every quarter note.  Here we calculate the time
            # for the current beat cycle to end
            until_time = now_time + self.quarter_note_length

            # for musicians paying attention to the conductor, tell them the
            # next beat cycle has started now and when it will end
            for item in self.signal:
                item.signal(beat, now_time, until_time)

            # the timeline has recorded any musicians that are being listened
            # to by the RealtimeOutput (aka Audience).  Get all these events
            # off the timeline with appropriate timing delays so they play back
            # exactly when they are supposed to.  Events outside the beat cycle
            # will stay on the timeline for later.  For instance, a whole note may
            # have an 'off' event well in the future.
            for event in self.timeline.process_due_events(now_time, until_time):
                self.handle_band_event(event)

            # if no events were recorded, we're done, so bail out
            if not self.performance.got_events:
                print("OUT OF EVENTS")
                running = False

            # count the beat cycle as concluded
            now_time = until_time

        # the performance is done, make sure we don't leave any notes stuck on
        # FIXME: TODO: hook SIGINT so this also happens on Control-C.
        for event in self.timeline.process_off_events():
            self.handle_band_event(event)
