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
import os

# this has been successfully tested with an Apple IAC Driver
# open Apple Audio MIDI setup if you have a Mac.
# https://pypi.python.org/pypi/rtmidi-python
import rtmidi_python as rtmidi

from camp.playback.constants import *

def get_ports():
    midi_out = rtmidi.MidiOut(b'out')
    available_ports = midi_out.ports
    return available_ports

def get_bus():
    ports = get_ports()
    port_num = os.environ.get("CAMP_MIDI_BUS", len(ports) -1)
    return int(port_num)

class Realtime(object):

    """ currently this mostly just tests rtmidi.  This may change. """

    def __init__(self):

        midi_out = rtmidi.MidiOut(b'out')
        midi_out.open_port(get_bus())
        self.midi_out = midi_out

    #def _volume(self, channel, volume):
    #    cc = CONTROL_CHANGE | channel
    #    return [cc, volume & 0x7F]

    def note_off(self, channel, note_number, velocity):
        result = [NOTE_OFF | channel, note_number, velocity]
        return result


    def note_on(self, channel, note_number, velocity):
        print("CH: %s" % channel)

        result =  [NOTE_ON | channel, note_number, velocity]
        return result

    def play_event(self, event):
        print(event)
        self.midi_out.send_message(event)

    def playback_test(self):

        note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
        note_off = [0x80, 60, 0]
        self.midi_out.send_message(note_on)
        time.sleep(0.5)
        self.midi_out.send_message(note_off)
        print("OK!")
