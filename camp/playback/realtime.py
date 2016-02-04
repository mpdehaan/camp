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

import time

# this has been successfully tested with an Apple IAC Driver
# open Apple Audio MIDI setup if you have a Mac.
# https://pypi.python.org/pypi/rtmidi-python
import rtmidi_python as rtmidi

def print_event(self, io, event):
    """
    A debug callback used in testing that does not actually send real events.
    """
    pass

def play_event(self, io, event):
    """
    A callback that actually sends MIDI events.
    """
    pass

class Realtime(object):

    def __init__(self, song):
        self.song = song

        midi_out = rtmidi.MidiOut(b'out')
        available_ports = midi_out.ports
        for port in available_ports:
            print(port)

        #if available_ports:
        midi_out.open_port(0)
        #else:
        #    midi_out.open_virtual_port("My virtual output")

        self.midi_out = midi_out


    def playback_test(self):

        note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
        note_off = [0x80, 60, 0]
        self.midi_out.send_message(note_on)
        time.sleep(0.5)
        self.midi_out.send_message(note_off)
        print("OK!")

    def play_song(self, callback=play_event):
        for scene in self.song.scenes:
            self.play_scene(scene, callback=callback)


    def play_scene(self, scene, callback=play_event):

        quarter_note_length = scene.compute_quarter_note_length()

        for pattern in scene.patterns():
            pattern.reset_play_head()
        playhead = 0
        scene_time = scene.compute_scene_time()

        while playhead < scene_time:

            playhead += play_speed

            for pattern in scene.patterns():
                events = pattern.advance_play_head(play_head,
                    quarter_note_length=quarter_note_length)
                timeline.add_events(events)

            events = timeline.pop_due_events(playhead)

            for event in Timeline.on_events(events):
                callback(event)
            for event in Timeline.off_events(events):
                callback(off_events)

            sleep(play_speed)

        # if any off events didn't fire because of timing issues,
        # make sure they do
        for event in Timeline.off_events(timeline.events):
            callback(off_events)

        # TODO: we should probably track all on events to make it
        # easier to clear stuck events on Ctrl-C and add an interrupt
        # handler
