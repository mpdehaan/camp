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

class Duration(Member):

    def __init__(self, lengths=None, channel=None, when=True):

        """
        Constructor.  Read class docs.
        """

        super().__init__(channel=channel, when=when)
        self._lengths = lengths
        self.reset()

    def copy(self):
        return Duration(lengths=self._lengths, channel=self.channel, when=self._when)
        # BOOKMARK: I AM ADDING COPY CONSTRUCTORS NOW

    def reset(self):

        # question: not sure if this should respond to reset due to scale change
        # leaving it for now,  YAGNI?

        self._which_length = self.draw_from(self._lengths)

    def on_signal(self, event, start_time, end_time):

        length = next(self._which_length)
        event.duration = length

        for send in self.sends:
            send.signal(event, start_time, end_time)

        return [ event ]
