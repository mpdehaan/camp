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

from camp.core.scale import Scale
from camp.opus.bar import Bar

# see tests/opus.py for how all this works.
#
# reminder example:
#
# Pattern(name="sheep-theme", notation='roman',
#     bars = [
#       Bar(cells="4 6 4 6 4 4 4 4 6 6 4 1 1 - - - -".split())
#     ]
# )


class Pattern(object):

    def __init__(self, name=None, notation='roman', bars=None, scale=None, ):

        self.name = name
        self.notation = notation
        self.bars = bars
        self.scale = scale

        assert isinstance(self.name, str)

        # later, this might (and probably should be) be pluggable
        assert self.notation in [ 'roman', 'literal']

        # bars should be a list of lists of strings to be interpreted by the notation system, such as roman.py
        # one token at a time
        assert type(self.bars) == list

        if len(self.bars) > 0:
            for bar in self.bars:
                assert type(bar) == Bar


        if self.scale is not None:
            # user wishes to override the scale for this pattern only
            assert type(self.scale) == Scale
