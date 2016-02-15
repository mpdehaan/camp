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

from camp.band.members.member import Member
from camp.utils import loop_around

class ScaleFollower(Member):

    """
    Plays along the current scale for a specified length of notes
    before restarting the scale.

    Usage:

    s = ScaleFollower(lengths=[7,14,7])

    This would play the current scale for 7 notes (rolling around if the scale
    was generated too short), then 14 notes, then 7.  If the scale changed
    while playing back it would start over at the beginning of the new scale.
    """

    def __init__(self, lengths=None, channel=None):



        assert type(lengths) == list
        super().__init__()

        self.lengths_looper = loop_around(lengths)
        if channel is not None:
            self.channel = channel

        self.previous_scale = None
        self.current_scale = None
        self.generator = None

    def get_note_generator(self):

        if self.current_scale != self.previous_scale:
            self.generator = self.current_scale.generate(length=next(self.lengths_looper))
        return self.generator

    def on_signal(self, event, start_time, end_time):

        self.current_scale = event.flags.get('scale',None)
        if self.current_scale is None:
            raise Exception("missing scale data from note signal, something wrong here")

        note_gen = self.get_note_generator()
        note = next(note_gen)
        event.notes = [ note ]

        self.previous_scale = self.current_scale

        for send in self.sends:
            send.signal(event, start_time, end_time)
