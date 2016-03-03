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

class Channel(Member):

    """
    A very lame plugin that only sets the MIDI channel.  You can set this on
    any event at all, so this is basically a no-op.  It is needed by the tracker
    implementation and may not have direct application otherwise, so you can
    pretend it does not exist!
    """

    def __init__(self, channel=None, when=True):
        assert channel is not None
        super().__init__(channel=channel, when=when)
        self.reset()

    def reset(self):
        pass


    def on_signal(self, event, start_time, end_time):

        for send in self.sends:
            send.signal(event, start_time, end_time)

        return [ event ]
