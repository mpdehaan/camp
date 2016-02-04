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

# see tests/opus.py for how all this works.

class Bar(object):

    def __init__(self, cells=None, repeats=1, stop=None):

        self.cells = cells
        self.stop = stop
        self.repeats = repeats
        self.play_count = 0
        self.play_head = 0

        assert type(self.cells) == list
        if self.stop is not None:
            assert type(self.stop) == int
        assert type(self.repeats) == int

        # TODO: upon evaluation, use the notation system from the Pattern
        # to convert each bar into a list of Notes and/or chords, accounting
        # for that some cells may contain ties or rests.  This method likely
        # lives in Pattern, not here, TBD

    def reset_play_head(self, value=0):
        """ Where are we playing inside this bar? """
        self.play_head = 0

    def reset_play_count(self, value=0):
        """ If play count == repeats, we can move to the next bar """
        self.play_count = 0
