
from camp.playback.realtime import Realtime
from camp.playback.event import Event
from camp.band.member import Member
import time


class Conductor(object):

    def __init__(self, signal=None, output=None, realtime=None, timeline=None, output_modes=None, debug=True):

        assert type(signal) == list
        assert timeline is not None
        assert output is not None

        self.output_modes = output_modes
        if output_modes is None:
            self.output_modes = [ 'print_events', 'play_events']
        for item in output_modes:
            assert item in [ 'save_events', 'print_events', 'play_events']

        self.realtime = realtime
        self.signal = signal
        self.timeline = timeline
        self.output = output
        self.debug = debug
        self.bpm = self.output.bpm
        self.quarter_note_length = 60 / self.bpm

        # these are used ONLY when saving events in the debug output_mode called 'save_events'
        self.midi_event_buffer = []
        self.band_event_buffer = []


    def _band_event_to_midi_events(self, event):

        midi_events = []

        if event.typ == 'note':
            if event.off == True:
                for note in event.notes:
                    assert event.channel is not None
                    midi_events.append(self.realtime.note_off(event.channel, note.note_number(), note.velocity))
            else:
                for note in event.notes:
                    assert event.channel is not None
                    midi_events.append(self.realtime.note_on(event.channel, note.note_number(), note.velocity))

        else:
            raise Exception("do not know how to convert event: %s" % event)

        return midi_events


    def handle_band_event(self, event):
        if 'save_events' in self.output_modes:
            self.band_event_buffer.append(event)
        midi_events = self._band_event_to_midi_events(event)
        for midi_event in midi_events:
            if 'play_events' in self.output_modes:
                self.realtime.play_event(midi_event)
            elif 'save_events' in self.output_modes:
                self.midi_event_buffer.append(midi_event)
            elif 'print_events' in self.output_modes:
                print(event)
            else:
                raise Exception("unknown conductor output mode")

    def start(self):
        beat = Event(typ='beat')
        running = True

        while running:
            #print("waves baton")

            self.output.got_events = False

            now_time = time.time()
            until_time = now_time + self.quarter_note_length

            print("NOW TIME = %s" % now_time)
            print("QNL = %s" % self.quarter_note_length)
            print("UNTIL = %s" % until_time)
            # raise Exception("OK!")



            #print("NOW TIME = %s" % now_time)
            #print("UNTIL TIME = %s" % until_time)


            for item in self.signal:
                item.signal(beat, now_time, until_time)


            for event in self.timeline.process_due_events(until_time):
                self.handle_band_event(event)

            # DEBUG only
            if len(self.timeline.events) > 100:
                raise Exception("EVENT QUEUEING PROBLEM")

            if not self.output.got_events:
                running = False



        # make sure we don't leave any notes stuck on
        # TODO: hook SIGINT and make sure these get cancelled on Control-C

        # FIXME: sometimes this last note gets cut off early

        #print("FLUSHING")
        print(self.timeline.events)
        for event in self.timeline.process_off_events():
            self.handle_band_event(event)
