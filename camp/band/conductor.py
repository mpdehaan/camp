
from camp.playback.realtime import Realtime
from camp.playback.event import Event
from camp.band.member import Member
from camp.band.performance import Performance
import time


class Conductor(object):

    """
    The conductor oversees a performance.

    Don't think of this metaphor too literally.  This isn't a real world model, exactly.

    With each wave of the baton (every quarter note, a beat in "bpm"), the conductor sends beats down toward listening band members.
    Band members are more or less duck-typed plugins.
    These beats are functions in the band members, which may in turn signal other attached band members due to various rules.
    They may also emit notes, but they may also mess with the beat *OTHER* band members here.  Or check the weather.
    The realtime_output chooses to listen to specific band members and record their notes onto the timeline.
    The conductor then periodically reviews this timeline as notes are being entered into it, and converts them to realtime MIDI.
    For an example, see tests/band.py
    """

    def __init__(self, signal=None, performance=None):

        """
        Constructor.

        signal - a list of band members that are keyed into 'beats'.  If not listed here the band
        member needs to be keyed into other band members or they won't play.

        output - an instance of the RealtimeOutput class, this is a specialized band
        member that takes events with durations and adds the approriate note off events onto the timeline

        realtime - this is an instance of camp.playback.realtime and is the interface to sending actual
        realtime MIDI data.  Not part of the theoretical object model.

        timeline - an object that records events and can also consume them with appropriately spaced
        delays.  We are writing the score as it plays, and this is the clock that both records
        the score as it is being written and keeps everyone on time.
        """

        assert type(signal) == list
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

            # we're just going to send a beat signal, the members of the band
            # decide whether to play any notes.  A beat is an inaudible event.
            beat = Event(time=now_time)

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
                running = False

            # count the beat cycle as concluded
            now_time = until_time

        # the performance is done, make sure we don't leave any notes stuck on
        # FIXME: TODO: hook SIGINT so this also happens on Control-C.
        for event in self.timeline.process_off_events():
            self.handle_band_event(event)
