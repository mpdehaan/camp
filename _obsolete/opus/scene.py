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

    def __init__(self, song=None, name=None, scale=None, bpm=None, bars=None, track_mapping=None):

        self.name = name
        self.scale = None  # if not set, use Song value
        self.bpm = None    # if not set, use Song value
        self.bars = None   # if not set, use Song value
        self.track_mapping = track_mapping
        self.song = None

        assert isinstance(self.name, str)
        assert type(self.track_mapping) == dict

        if self.scale is not None:
            assert type(self.scale) == scale
        if self.bpm is not None:
            assert type(self.bpm) in [int, float]
        if self.bars is not None:
            assert type(self.bars) == int
        if self.song is not None:
            assert str(type(self.song)) == 'Song'

    def track_names(self):
        return self.track_mapping.keys()

    def patterns(self):
        return self.track_mapping.values()

    def compute_quarter_note_length(self):
        bpm = self.song.bpm
        if self.bpm is not None:
            bpm = self.bpm
        return 60 / bpm

    def compute_scene_time(self):
        """
        How long will this scene play in seconds?
        It's a function of the bar count, length, and quarter note length, as
        well as note type on the song AND the scene.
        """
        raise NotImplementedError()
