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

CODED_DEFAULTS = dict(
    bpm = 120,
    scene_bar_count = 1,
)


class Defaults(object):

    __slots__ = [ '_defaults', '_factory']

    def __init__(self, **kwargs):
        self._defaults = CODED_DEFAULTS
        self.set(**kwargs)

    def set(self, **kwargs):

        keys = CODED_DEFAULTS.keys()
        for (k,v) in kwargs.items():
            if k not in keys:
                raise Exception("invalid default setting: %s" % k)
            self._defaults[k] = v
        return self

    def as_dict(self):
        return self._defaults
