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
from camp.band.members.roman import Roman
from camp.band.members.literal import Literal
from camp.band.members.transpose import Transpose
from camp.band.members.scale_follower import ScaleFollower
from camp.band.selectors.endlessly import Endlessly
from camp.band.members.subdivide import Subdivide
from camp.band.selectors.randomly import Randomly
from camp.band.selectors.repeatedly import Repeatedly
from camp.band.members.ordered import Ordered

def play():

    # in example 15 we show how to drift between different patterns.

    # so far, we've mostly been showing patterns inside a scale, because
    # that sounds good for melodic instruments.  Not everything lives
    # inside a scale though - accidentals etc.  Transpose and the arp
    # can move by semitones to overcome that.

    # however, when dealing with drum kits, the scale is pretty much never
    # relevant

    # Usually these things trigger with something like C3 for a kick drum, D4
    # for a Tom, and so on -- but it varies by drumkit.

    # Having a transpose or scale change in there would
    # mess it all up.

    # Here's an example of switching through some drum patterns, and it also
    # fires multiple types of drum hits on a single channel.

    # when setting this example up, put any synth you want on MIDI channel 2,
    # but on MIDI channel 1 put some kind of drumkit.  You may need to change
    # the MIDI note names to make it sound right

    K = "F4"
    H = "A4"
    C = "Bb4"

    output = Performance(bpm=120, stop_seconds=15)


    scale_choices = Endlessly([scale("D minor")])
    melody_trigger = ScaleSource(scales=scale_choices)
    melody = Roman(symbols=Endlessly("1 - - - - 2 - - - -".split()), channel=1)

    drum_trigger = Subdivide(splits=Endlessly([4]), channel=2) # gimme 16th notes for the drum tracks

    # kick drum on the quarter notes
    kicks = Literal(symbols=Endlessly([K, None, None, None,
                                       K, None, None, None,
                                       K, None, None, None,
                                       K, None, None, None]))

    # hihat on the 8th notes every other bar
    # but wait one bar before starting that up.
    hihat = Ordered(
        sources = Endlessly([
            Literal(symbols="- - - - - - - - - - - - - - - -".split()),
            Literal(symbols=Endlessly([
                H, None, H, None, H, None, H, None,
                H, None, H, None, H, None, H, None
            ]))
        ])
    )

    # cymbals on the half notes
    cymbals = Literal(symbols=Endlessly([
            C, None, None, None, None, None, None,
            C, None, None, None, None, None, None
        ]))


    melody_trigger.send_to(melody)
    drum_trigger.send_to([kicks, hihat, cymbals])
    output.listens_to([melody, kicks, hihat, cymbals])


    conductor = Conductor(signal=[melody_trigger, drum_trigger], performance=output)
    conductor.start()


if __name__ == "__main__":
    play()
