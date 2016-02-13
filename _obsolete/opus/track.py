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
#
# reminder example:
#
# track1 = song.add_track(Track(name="melodica", midi_channel=1))

class Track(object):

    def __init__(self, song=None, name=None, midi_channel=None):

        self.name = name
        self.song = song
        self.midi_channel = midi_channel

        assert isinstance(self.name, str)

        # CAMP doesn't *HAVE* to be used for MIDI, but I'd prefer these get
        # checked anyway - if not doing MIDI, just make up a channel number.
        # Channel numbers do *NOT* have to be unique between tracks, but we'll
        # avoid setting a default to avoid surprises.

        assert type(self.midi_channel) == int
