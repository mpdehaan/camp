
from camp.playback.realtime import Realtime
from camp.playback.event import Event
from camp.band.member import Member
import time


class Conductor(object):

    def __init__(self, signal=None, output=None, timeline=None, output_mode=None, debug=True):

        assert type(signal) == list
        assert timeline is not None
        assert output_mode in [ 'save_events', 'print_events', 'realtime']
        assert output is not None

        self.realtime = None
        self.signal = signal
        self.timeline = timeline
        self.output = output
        self.output_mode = output_mode
        self.debug = debug

        if self.output_mode in [ 'realtime' ]:
            self.realtime = Realtime()

    def _band_event_to_midi_event(self, event):
        raise NotImplementedError()

    def handle_band_event(self, event):
        midi_event = self._band_event_to_midi_event(event)
        if mode == 'realtime':
            realtime.play_event(midi_event)
        elif mode == 'save_events':
            self.midi_event_buffer.append(midi_event)
            self.band_event_buffer.append(event)
        elif mode == 'print_events':
            print(event)
        else:
            raise Exception("unknown conductor output mode")

    def start(self):
        print("conductor :: start")
        beat = Event(typ='beat')
        running = True

        while running:

            print("conductor :: loop")
            self.output.got_events = False

            for item in self.signal:
                print("conductor :: signal :: %s" % item)
                item.signal(beat)

            now_time = time.time()

            events_due = self.timeline.pop_due_events(now_time=now_time)
            print("conductor :: events_due :: %s"  % events_due)
            for event in events_due:
                self.handle_band_event(event)

            if not self.output.got_events:
                print("conductor :: switching off")
                running = False

            # replace with something that better understands BPM.
            if running and self.output_mode in [ 'realtime' ]:
                print("conductor :: sleeping")
                time.sleep(1)


        # make sure we don't leave any notes stuck on
        # TODO: hook SIGINT and make sure these get cancelled on Control-C
        print("conductor :: ensuring all notes are off")
        for event in self.timeline.off_events():
            self.handle_band_event(event)
