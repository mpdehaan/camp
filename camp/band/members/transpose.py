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

class Transpose(Member):


    def __init__(self, channel=None, octaves=None, when=True):

        # TODO: later also support step transpositions
        # or even grabbing the next note in the scale

        super().__init__(channel=channel, when=when)
        self._octaves = octaves
        self.reset()

    def copy(self):
        return Transpose(channel=self.channel, octaves=self._octaves, when=self._when)

    def reset(self):
        self.octaves_looper = self.draw_from(self._octaves)


    def on_signal(self, event, start_time, end_time):

        amount = next(self.octaves_looper)

        if event.notes is not None and len(event.notes) > 0:
            notes = [ n.transpose(octaves=amount) for n in event.notes ]
            event.notes = notes

        for send in self.sends:
            send.signal(event, start_time, end_time)

        return [ event ]
