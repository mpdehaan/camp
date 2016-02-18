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

from camp.band.conductor import Conductor

from camp.band.members.performance import Performance
from camp.band.members.scale_source import ScaleSource
from camp.band.members.scale_follower import ScaleFollower

from camp.playback.realtime import get_ports, get_bus

INSTRUCTIONS = """

To get MIDI realtime output in CAMP to work, you must select an appropriate MIDI bus.
This will be the bus that will drive instruments in your DAW, VST host, or externally.
Currently, only one bus can be used at a time with CAMP.

In the list below, the LAST bus will be selected unless the environment variable
CAMP_MIDI_BUS is set to a different number. For instance, at a bash prompt:

    # export CAMP_MIDI_BUS=1

OR:

    # CAMP_MIDI_BUS=1 PYTHONPATH=. python3 examples/01_minimal.py

In the future the bus choice may also be selectable using the Conductor() object.

If you happen to be using OS X, you probably want to create, and then select, an IAC bus.
Consult README.md in the source distribution for tips.

Available MIDI buses are:

"""

def play():

    print(INSTRUCTIONS)

    ports = get_ports()
    for (i,x) in enumerate(ports):
        print("    - %s: %s" % (i,x))

    print("")
    print("The currently selected bus is #%s" % get_bus())

if __name__ == "__main__":

    play()
