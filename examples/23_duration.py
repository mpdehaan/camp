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

from camp.band.members.scale_source import ScaleSource
from camp.band.members.performance import Performance
from camp.band.selectors.endlessly import Endlessly
from camp.band.members.duration import Duration
from camp.band.members.roman import Roman
from camp.band.members.ordered import Ordered

def play():

    # examples/06_subdivide showed how to chop up the incoming quarter note signal
    # to create faster signals.  However, sometimes in a given bar we want a mix of note durations.
    # how do we do that?

    # For this example, lets play whole note chords underneath a quarter note melody.

    # implementation caveat:
    # Because the "beat" signal from the conductor comes in every quarter note, we have to take
    # care and rest in the right places of the input signal to avoid funness.  This may get easier
    # later.

    # this is pretty close to what we did in 09_harmony.py


    output = Performance(bpm=120, stop_seconds=15)

    # this performance will actually complete so stop_seconds is mostly ignorable.

    scale_choices = Endlessly([scale("D major")])
    source = ScaleSource(scales=scale_choices)

    # the underlying chords - note the rests
    chords     = Roman(symbols=Endlessly("I - - - I - - - IV - - - V - - - ".split()), channel=1)
    # every beat is a quarter note, but on the first beat in a cycle of 4
    # play a WHOLE note
    chords_len = Duration(lengths=Endlessly([1,0,0,0]))
    source.chain([chords, chords_len, output])

    # the melody
    # TODO: Roman should figure out if input is a string here and auto-split.
    pattern2 = Roman("1 2 3 1 2 2 1 3 3 1 3 2".split(), channel=2)
    pattern3 = Roman("1 3 3 1 4 4 1 3 3 1 5 -".split(), channel=2)
    pattern4 = Roman("1 5 5 1 4 4 1 3 3 1 2 2".split(), channel=2)
    pattern5 = Roman("1 2 4 6 4 2 1 6 4 2 1 -".split(), channel=2)
    melody_sequence = [ pattern2, pattern3, pattern4, pattern5 ]
    melody = Ordered(sources=Endlessly(melody_sequence))
    # we could just do: source.chain(source, ordered) here
    # but it would mean later we would have less flexibility
    # to make the patterns feel different.
    source.chain([melody])
    for pattern in melody_sequence:
        source.chain([ pattern, output])

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()



if __name__ == "__main__":
    play()
