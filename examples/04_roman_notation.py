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

def play():

    # now modifying our previous example, instead of playing the same two
    # scales in a loop, let's play a given set of notes in each scale.
    # We'll use roman notation to play the 1st, 4th, and 5th note in the scale
    # followed by the 1st, 4th, and 5th major chord
    # finally, we'll play the 2nd, 3rd, and 6th minor chord.


    output = Performance(bpm=120, stop_seconds=10)

    # this is just as before, playing one scale then the other in a loop of 7
    # notes each
    scale1 = scale("c6 major")
    scale2 = scale("c6 minor")
    scale_choices = [ dict(scale=scale1, beats=7), dict(scale=scale2, beats=7) ]
    source = ScaleSource(scales=Endlessly(scale_choices))

    # the scale follower will play the first 7 notes in each scale, whatever the current
    # scale is.  Note that a scale change that doesn't quite line up with the length
    # of the roman pattern rolling over might sound a bit weird.  That's ok.
    roman = Roman(symbols=Endlessly("1 4 5 I IV V ii iii vi".split()), channel=1)
    source.chain([roman, output])

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()

if __name__ == "__main__":
    play()
