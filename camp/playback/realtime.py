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

        # for each scene in the song
            # play the scene
        pass

    def play_scene(scene, callback=play_event):

        # determine the lengths of each bar

        # convert each bar to a timeline of event data

        # find the current bar that should be playing for each track

        # combine all the current bars into one line of events

        # while the desired length of the global bar is not expired
            # fire all the events that have elapsed
            # sleep some very small slice of time
        pass
