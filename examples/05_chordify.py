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

def play():

    # playing all the power chords in a chromatic scale.

    output = Performance(bpm=120, stop_seconds=10)

    # play the two scales for 7 beats each, and then keep using those scales
    scale1 = scale("c4 chromatic")
    scale_choices = dict(scale=scale1, beats=12)
    source = ScaleSource(scales=scale_choices)

    follower = ScaleFollower(lengths=12)
    chordify = Chordify(types="power", channel=1)
    source.chain([follower, chordify, output])

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()

    # pop quiz: change the following line:
    # follower = ScaleFollower(lengths=Endlessly([12]), channel=1)
    # to
    # follower = ScaleFollower(lengths=[12], channel=1)
    # what happens and why?

if __name__ == "__main__":
    play()
