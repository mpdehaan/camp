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
from camp.band.members.transpose import Transpose
from camp.band.members.scale_follower import ScaleFollower
from camp.band.selectors.endlessly import Endlessly
from camp.band.selectors.randomly import Randomly
from camp.band.members.ordered import Ordered

def play():

    # so far what we've done has been mostly theoretical.
    # to construct larger songs, obviously, one thing has to occur
    # after another.  To do this, we could just pass in GIGANTIC
    # arrays to everything but that would suck!

    # now, everything in CAMP is built off the idea of generators.
    # this means the system can pretty well know if one thing is done
    # playing and more on to the next.

    # while we could just pass in huge note arrays, that kind of sucks.
    # What if we want a flute to play
    # it's part and then have the trombone come in?  To do that,
    # we need a facility for ordering - to say "this comes next"

    # NOTE: we're setting stop seconds to 100 seconds but this composition
    # will complete due to the sources being exhausted first, which is the point.
    # we're not writing an endlessly generative piece here, but moving towards
    # more explicit songwriting tools.  The point of this example is to show
    # we are writing a finite song in PIECES.

    output = Performance(bpm=240, stop_seconds=100)
    scale_choices = Endlessly([scale("a3 major")])

    source = ScaleSource(scales=scale_choices)

    pattern1 = Roman(symbols="1 2 3 4".split())
    pattern2 = Roman(symbols="I I I I".split())
    pattern2_transpose = Transpose(octaves=Endlessly([2]))
    pattern2.send_to(pattern2_transpose)

    # in this example, we're going to play pattern1 until it is exhausted
    # then pattern2, and when that's done, we're done.

    ordered = Ordered(sources=[pattern1, pattern2], channel=1)

    # HOMEWORK ASSIGNMENT:
    # uncomment this line to randomly pick a pattern and play it until
    # it is exhausted, but keep doing that endlessly.  Patterns might
    # repeat, see notes about advanced usages of Randomly in examples/11_randomness.py
    #
    # ordered = Ordered(sources=Randomly([pattern1,pattern2]), channel=1)

    # HOMEWORK ASSIGNMENT:
    #
    # uncomment this next line to play pattern1, pattern2 in an endless sequence
    # ordered = Ordered(Endlessly([pattern1,pattern2]))

    # TODO: IDEA: it might be nice to have a "beats" flag on ordered where it can stop
    # producing after a certain number of beats
    # ordered = Ordered(Randomly([pattern1,pattern2,pattern3]), beats=24)
    # this would allow for patterns of patterns, and better nesting.

    # TODO: IDEA: anything that can take a "beats" should really take a bars=, it's just easier
    # to think about

    # HOMEWORK: using a pattern in Ordered that uses Endlessly will cause the pattern to NOT switch.
    # Try this out and understand why pattern 2 will never play.
    # pattern1 = Roman(symbols=Endlessly("3 6 3 6 5 1 2".split()))
    # ordered = Ordered([pattern1,pattern2,pattern3])

    # TODO: IDEA, make the above homework example actually work, with something like:
    # pattern1 = Roman(symbols=Endlessly("3 6 3 6 5 1 2".split()))
    # ordered = Ordered([ dict(pattern=pattern1, beats=8), dict(pattern=pattern2, beats=8) ])

    # NOTE: in simple cases we could connect ordered to the output, but we'd miss the transposition,
    # and I wanted to show off a more complete example.  This also underscores the idea that source.chain
    # is just syntactic sugar and you don't have to use it.

    source.send_to(ordered)
    pattern1.send_to(output)
    pattern2_transpose.send_to(output)

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()

if __name__ == "__main__":
    play()
