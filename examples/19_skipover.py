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

    # Previously, in 11_randomness we introduced the default 'choice' random mode, which just endlessly
    # picks something from a list.

    # in 18_randomness2.py we introduced 'probability', which returns True or False depending on the chances
    # given.  It's used with the "when" statement, shown in both 18_randomness2.py and 19_skipover.py for doing
    # some rather fun things.

    # Some more types of randomness are "exhaust" and "human_random".

    # just to prove this performance will terminate by reaching the END of the performance, we're setting the stop
    # seconds to a crazy long amount of time.  This one won't loop endlessly, because of the way 'exhaust' mode works.
    output = Performance(bpm=120, stop_seconds=9999)

    # exhaust takes a list and feeds it in random order.  It would be the same as shuffle sorting the list, basically, and then
    # popping off the first element repeatedly.  The result is all items will be used, in a random order, and then the sequence
    # will stop.
    #
    # We normally write this in a one liner, but we'll break it up in this example to make things a bit more clear

    scale_choices = [scale("Ab blues"), scale("C major"), scale("Eb mixolydian")]
    scale_chooser = Randomly(scale_choices, mode='exhaust')
    source = ScaleSource(scales=Randomly(scale_choices, mode='exhaust'))

    # human_random is inspired by the Apple iTunes problem.  In a party shuffle mode, people may get suprised to learn
    # that the system played three Van Halen songs in a row.  Apple changed the system to switch between artists more frequently.
    # in CAMP, human random will play each item in a list once, before going back and starting over with a new random selection.

    note_choices = "1 2 3 4 5 6 7".split()
    note_chooser = Randomly(note_choices, mode='human_random')
    melody = Roman(symbols=note_chooser, channel=1)

    # combining these two concepts together, we are going to play 3 random scales in sequence, and then FOR EACH SCALE, play
    # the scale notes in random order.

    source.chain([melody, chordify, transpose, output])
    conductor = Conductor(signal=[source], performance=output)
    conductor.start()


if __name__ == "__main__":
    play()
