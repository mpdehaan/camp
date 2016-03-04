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
from camp.notation.literal import Literal as LiteralNotation

# FIXME: so much duplication with Roman, really wants for a base class

class Literal(Member):

    """
    Similar to the Roman playback support, this is keyed for literal notes
    and chords, and ignores scales.  Primarily intended for drum kits.
    """

    def __init__(self, symbols=None, channel=None, when=True):

        super().__init__(channel=channel, when=when)
        self._symbols = symbols
        self.reset()

    def copy(self):
        return Literal(symbols=self._symbols, channel=self.channel, when=self._when)

    def reset(self):

        self.symbol_looper = self.draw_from(self._symbols)

    def on_signal(self, event, start_time, end_time):

        try:
            symbol = next(self.symbol_looper)
        except StopIteration:
            return []

        event.notes = LiteralNotation().do_notes(symbol)

        for send in self.sends:
            send.signal(event, start_time, end_time)

        return [ event ]
