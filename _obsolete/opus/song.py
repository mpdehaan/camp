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
from camp.opus.track import Track
from camp.opus.scene import Scene

# see tests/opus.py for how all this works.

class Song(object):

    def __init__(self, name=None, scale=None, pattern_length=16, bars=1, bpm=120):

        assert isinstance(name, str)
        assert type(scale) == Scale
        assert type(pattern_length) == int
        assert type(bars) == int
        assert type(bpm) == int

        self.name = name
        self.scale = scale
        self.pattern_length = pattern_length
        self.bars = bars
        self.bpm = bpm

        self.tracks = []
        self.scenes = []

    def add_track(self, track):
        assert type(track) == Track
        track.song = self
        self.tracks.append(track)
        return track

    def add_scene(self, scene):
        assert type(scene) == Scene
        scene.song = self
        self.scenes.append(scene)
        return scene
