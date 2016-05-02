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

class Subdivide(Member):

    """
    Repeats a signal a given number of amounts.

    For instance, if we have a quarter note pulse from the conductor:
    Q Q Q Q

    This will produce in each "Q" beat four signals, rather than one.
    SSSS SSSS SSSS SSSS

    It does this by slicing up the beat into smaller beats.
    """

    def __init__(self, channel=None, splits=None, when=True):

        """
        Usage:

        sd = Subdivide(amounts=[1,2,3,4])

        Notice the amounts array.

        This means that for the first beat, there is only one subdivision (no subdivision).
        For the next "beat", the notes will be subdivided twice.
        Then three times, then four.

        After that, we'll cycle back and do 1 subdivision again. Ad nauseum.
        """

        super().__init__(channel=channel, when=when)
        self._splits = splits
        self.reset()

    def to_data(self):
        return dict(cls="camp.band.members.subdivide.Subdivide", data=dict(
            splits = self.datafy(self._splits),
            channel = self.datafy(self.channel),
            when = self.datafy(self._when)
        ))

    def copy(self):
        return Subdivide(channel=self.channel, when=self._when, splits=self._splits)

    def reset(self):

        self._subdivide_amounts = self.draw_from(self._splits)

    def on_signal(self, event, start_time, end_time):

        """
        Callback for the plugin.  This one is a bit complicated.
        """

        produced = []

        # calculate the length of the beat cycle
        delta = end_time - start_time
        # find out how many subdivisions there are for this beat
        slices = next(self._subdivide_amounts)
        # how long is each subdivision in seconds?
        each_slice_width = delta / slices
        # when does the first subdivision start?
        new_start_time = start_time

        # here we flag the note. This is because certain plugins like
        # ScalePlayer need to know what to do such that they shorten
        # the durations of the notes coming out, otherwise things won't work right.

        event.add_flags(subdivide=slices)

        # for however many times we are going to subdivide

        for slice_num in range(0,slices):

            event = event.copy()

            # calculate the end time of the new beat we are going to trigger

            new_end_time = new_start_time + each_slice_width

            event.time = new_start_time

            print("SUBDIVIDE SENDS: %s" % self.sends)
            for send in self.sends:
                send.signal(event, new_start_time, new_end_time)

            # move on to the next beat in the subdivision.
            new_start_time = new_start_time + each_slice_width

            produced.append(event)

        return produced
