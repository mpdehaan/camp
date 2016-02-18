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

from camp.core.scale import scale
from camp.band.conductor import Conductor

from camp.band.members.performance import Performance
from camp.band.members.scale_source import ScaleSource
from camp.band.members.scale_follower import ScaleFollower
from camp.band.members.chordify import Chordify
from camp.band.members.subdivide import Subdivide

from camp.band.selectors.endlessly import Endlessly

def play():

    # example 05 was "playing all the power chords in a chromatic scale".
    # let's modify the example very slightly using Subdivide.
    # normally the conductor sends down quarter notes.  Let's alternate
    # playing quarter notes and sixteenth notes.

    output = Performance(bpm=120, stop_seconds=10)

    # play the two scales for 7 beats each, and then keep using those scales
    source = ScaleSource(scales=scale("c4 chromatic"))

    follower = ScaleFollower(lengths=12)

    # pay attention to this part - nothing else has changed
    subdivide = Subdivide(splits=Endlessly([1,4]))

    chordify = Chordify(types="power", channel=1)
    source.chain([follower, subdivide, chordify, output])

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()


if __name__ == "__main__":
    play()
