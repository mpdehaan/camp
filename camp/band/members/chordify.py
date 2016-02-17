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

class Chordify(Member):

    """
    Chordify takes a note producing member and turns it into chords of
    the given type.

    cf = Chordify(types=["major","major","minor"])

    In the above example, if connected to a scale player, or other note
    generating BandMember, we'd turn the input into a major chord for the first two beats
    and every third beat we'd use a minor chord.

    To do things consistently:

    cf = Chordify(types=["major"])

    There you go, all major chords.
    """

    # TODO: allow "None" as a type to just emit the note.

    def __init__(self, types=None, channel=None):

        """
        Constructor.  Read class docs.
        """

        super().__init__(channel=channel)
        self._types = types
        self.reset()

    def reset(self):

        self._which_chord = self.draw_from(self._types)

    def on_signal(self, event, start_time, end_time):

        chord_typ = next(self._which_chord)

        if event.notes and len(event.notes) > 0:
            chord = Chord(root=event.notes[0], typ=chord_typ)
            event.notes = chord.notes

        for send in self.sends:
            send.signal(event, start_time, end_time)

        return [ event ]
