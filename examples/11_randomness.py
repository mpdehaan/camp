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
from camp.band.selectors.randomly import Randomly

def play():

    # in example 10 we showed you how powerful the arpeggiator can get.
    # well, that's great for some degrees of chaos, but what if we want
    # to let the computer make MORE decisions?

    output = Performance(bpm=120, stop_seconds=10)

    # randomness is one way to do that.

    # in example 03 we showed how to use Endlessly to loop over a set of input.
    # that used SELECTORS, but Endlessly is just a LINEAR selector that loops
    # when it gets to the end of the input.

    # randomness can also be accessed, using the Randomly selector, which
    # chooses an item from a list.
    # each choice is then repeated for a given number of times.
    # here lets pick some random scales, but whatever we pick, hold that choice
    # for 7 beats, which we covered in example 01.

    random_scale_choices = Randomly([
        # each of these items are scale specifications.  You've seen these in the very first examples.
        dict(scale=scale("c6 major"), beats=7),
        dict(scale=scale("Db4 minor_pentatonic"), beats=7),
        dict(scale=scale("Eb3 mixolydian"), beats=7)
    ])

    # note that the random selector could repeat a selection as currently
    # implemented and/or specified.  See ideas below.

    # note if we want a random choice to be made EVERY beat we can simplify
    # our usage of randomly like so:

    random_note_choices = Randomly("1 2 3 4 5 6 7".split())

    # what does that do?  It randomly plays one of 7 notes in the current scale.
    # that's syntactically clean, but super basic.  Let's override that with something
    # showing more options available to Randomly.

    # we're playing CHORDS now, and if we choose the "I" chord we are going to play
    # it twice in the current scale (which might change after we play the first, so this is
    # a minor lie). All within the current scale, of course.

    random_note_choices = Randomly([
        dict(value="I", hold=2),
        dict(value="IV", hold=1),
        dict(value="V", hold=1),
        dict(value="i", hold=1),
        dict(value="ii", hold=1),
        dict(value="iv:dim7", hold=1),
    ])

    # HOMEWORK: add some more scales to the random_scale_choices above and take out some
    # notes from random_note_choices.  Mix scales with notes!

    # FUTURE IDEA: also support a notion of frequency controlling what will be drawn.
    # frequencies should add up to 1.  This would still be compatible with "hold" above.

    #random_note_choices = Randomly([
    #    dict(value="I", frequency=0.4),
    #    dict(value="IV", frequency=0.2),
    #    dict(value="V", frequency=0.2),
    #    dict(value="i", frequency=0.1),
    #    dict(value="ii", frequency=0.05),
    #    dict(value="iv:dim7", frequency=0.05),
    #])

    # for more examples, see the demos labelled randomness2.py, randomness3.py, etc.
    # we want to cover some other things first, so I'm not going to go completelyinto
    # randomness now.

    source = ScaleSource(scales=random_scale_choices)
    roman = Roman(symbols=random_note_choices, channel=1)
    source.chain([roman, output])

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()

if __name__ == "__main__":
    play()
