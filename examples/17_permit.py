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
from camp.band.members.permit import Permit

def play():

    # Let's show how to play a sequence of one length but omit every Nth note

    output = Performance(bpm=120, stop_seconds=15)

    source = ScaleSource(scales=scale("D minor"))

    melody = Roman(symbols=Endlessly("1 2 3 4 5 6 7".split()), channel=1)
    silence = Permit(when=Endlessly([1, 1, 0]))

    # so we're playing a pattern of 1 2 3 4 5 6 7 of scale degree notes in a giant loop
    # the first time through what really happens is:
    #    1 2 <REST> 4 5 <REST> 7
    # and the second time:
    #    1 <REST> 3 4 <REST> 6 7
    # and the third time:
    #    <REST> 2 3 <REST> 5 6 <REST>
    # all of this is because the pattern and the 'silence' pattern are of unequal lengths

    # this is not ALWAYS relevant in a composition, but if you want to do something
    # polyrhytmic and unorthodox (not just with 'Silence') patterns of  unequal length
    # can be interesting.

    # HOMEWORK: experiment with changing the melody patterns and the silence patterns

    # HOMEWORK: change endlessly to randomly, and see what happens

    source.chain([melody, silence, output])
    conductor = Conductor(signal=[source], performance=output)
    conductor.start()


if __name__ == "__main__":
    play()
