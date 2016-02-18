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
from camp.core.chord import Chord

class Permit(Member):

    """
    Permit will only let some notes to pass through

    The following example will not play every 4th note.

    silence = Permit(when=Repeatedly([1,1,1,0]))

    The following example omits about 1/4 of the notes at random

    silence = Permit(when=Randomly([1,1,1,0]))

    The following example says every 4th note has a 50% chance of not playing

    silence = Permit(when=Randomly([1,1,1,0.5], mode='probability'))

    The following example is an absolute mute and may be of limited value.

    silence = Permit(when=0)
    """

    def __init__(self, when=None, channel=None):
        assert when is not None
        # NOTE: looks odd, but important that when is not passed to constructor here!
        super().__init__(channel=channel, when=1)
        self._when = when
        self.reset()

    def reset(self):

        self._should_silence = self.draw_from(self._when)

    def on_signal(self, event, start_time, end_time):

        permitted = next(self._should_silence)

        if not permitted:
            event.notes = []
            event.keep_alive = True

        for send in self.sends:
            send.signal(event, start_time, end_time)

        return [ event ]
