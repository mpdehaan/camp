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
from camp.band.selectors.endlessly import Endlessly
from camp.band.selectors.randomly import Randomly
from camp.band.members.chordify import Chordify
from camp.band.members.permit import Permit
from camp.band.members.transpose import Transpose

def play():

    # Permit, introduced in the example 18_randomness2.py allows us to
    # silence an entire chain when certain conditions are met.

    # However, sometimes, we may want to decide to apply an affect only
    # when something is true.  Because this could be useful ANYWHERE
    # the same type of "when" logic can actually be attached to ANYTHING.

    # here is a probabilistic way to use random, that combines the concepts.

    output = Performance(bpm=120, stop_seconds=15)

    source = ScaleSource(scales=scale("Ab blues"))

    melody = Roman(symbols=Endlessly("1 2 3 4 5 6 7".split()), channel=1)
    chordify = Chordify(types=Endlessly(['major','minor']), when=Randomly([0,0.45], mode='probability'))
    transpose = Transpose(octaves=Endlessly([2,-2]), when=Randomly([0,0,0.75], mode='probability'))

    # the result is every other note has a 40% chance of becoming a chord,  which is always alternating
    # major and minor when it happens

    # every THIRD note has a 75 percent chance of being transposed, which will be alternating +2/-2 octaves
    # when it happens

    # so now, we have easily inserted CONDITIONAL effects.  The use of when=Randomly wasn't required.
    # we could also have used Endlessly or Repeatedly.  Though keep in mind if using Repeatedly, when
    # the event chain is exhausted, that particular part of the performance will stop.  And when everything stops,
    # the performance is done.  Because this is likely being applied to an effect chain, Repeatedly probably
    # doesn't make the most sense with "when".  But Endlessly?  Sure!

    source.chain([melody, chordify, transpose, output])
    conductor = Conductor(signal=[source], performance=output)
    conductor.start()


if __name__ == "__main__":
    play()
