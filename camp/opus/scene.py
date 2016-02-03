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

# see tests/opus.py for how all this works
#
# reminder example:
#
# scene1 = song.add_scene(Scene(name="scene1", track_mapping=dict(
#     track1 = llama_pattern,
#     track2 = sheep_pattern,
#     track3 = kick_pattern
# ))


class Scene(object):

    def __init__(self, name=None, scale=None, bpm=None, bars=None, track_mapping=None):

        self.name = name
        self.scale = None  # if not set, use Song value
        self.bpm = None    # if not set, use Song value
        self.bars = None   # if not set, use Song value
        self.track_mapping = track_mapping

        assert isinstance(self.name, str)
        assert type(self.track_mapping) == dict

        if self.scale is not None:
            assert type(self.scale) == scale
        if self.bpm is not None:
            assert type(self.bpm) in [int, float]
        if self.bars is not None:
            assert type(self.bars) == int
