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

from camp.band.selectors.endlessly import Endlessly
from camp.band.selectors.repeatedly import Repeatedly
from camp.band.selectors.randomly import Randomly

class Patterns(object):

    def __init__(self, song, patterns=None):

        assert patterns is not None

        self._factory = song
        self._patterns = dict()
        self._save(patterns)

    def _save(self, patterns):
        for (name, pattern) in patterns.items():
            if isinstance(pattern, str):
                pattern = pattern.replace("|","").split()
                # print("USING PATTERN: %s" % pattern)
            self._patterns[name] = self.create(pattern)

    def create(self, pattern):
        raise NotImplementedError()

    def as_dict(self):
        return self._patterns

class RandomPatterns(Patterns):

    def __init__(self, song, mode=None, patterns=None):
        self.mode = mode
        super().__init__(song, patterns=patterns)

    def create(self, pattern):
        return Randomly(pattern, mode=self.mode)

class EndlessPatterns(Patterns):

    def create(self, pattern):
        return Endlessly(pattern)

class BasicPatterns(Patterns):

    def create(self, pattern):
        return pattern

class RepeatedPatterns(Patterns):

    def __init__(self, song, hold=None, patterns=None):
        self.hold = hold
        self.mode = mode
        super().__init__(song, patterns=patterns)


    def create(self, pattern):
        return Repeatedly(pattern, hold=self.hold)
