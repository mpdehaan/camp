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

from camp.band.members.scale_source import ScaleSource
from camp.core.scale import scale

class Scene(object):

    def __init__(self, scale=None, pre_fx=None, post_fx=None, patterns=None, bar_count=None):

        self.scale = scale
        self.pre_fx = pre_fx
        self.post_fx = post_fx
        self.patterns = patterns
        self.bar_count = bar_count

        self._factory = None # set up by scenes.py
        self._scale_source = ScaleSource(scale=scale(self.scale))
        self._output = None

    def build(self):

        # using self._factory ...
        self._build_output()
        self._build_pre_fx_chains()
        self._build_post_fx_chains()
        self._build_instruments()

    def get_signals(self):
        return [ self._scale_source ]

    def get_output(self):
        return [ self._output ]
