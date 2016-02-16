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

class ScaleSource(Member):

    """
    The scale source uses event flags to specify the current scale to be used on each beat.
    Typically, but not always, there will be one scale source at the top of the mesh.

    To play one scale for 7 beats, then another scale for 7:

    source1 = ScaleSource(scales=[ dict(scale=scale1, beats=7), dict(scale=scale2, beats=7) ])

    To keep it simple and just select a permanent scale:

    source1 = ScaleSource(scales=[ dict(scale=scale1) ])
    """

    def __init__(self, scales=None, channel=None):

        if channel is not None:
            self.channel = channel

        super().__init__()

        self.scale_spec_looper = self.draw_from(scales)
        self.scale_gen = self.scale_generator()


    def scale_generator(self):

        for scale_spec in self.scale_spec_looper:

            scale = scale_spec.get('scale', None)
            if scale is None:
                raise Exception("invalid scale spec")
            self.current_scale = scale

            repeat_beats = scale_spec.get('beats', 1)

            for beat in range(0, repeat_beats):
                yield scale


    def on_signal(self, event, start_time, end_time):

        try:
            scale = next(self.scale_gen)
        except StopIteration:
            return

        event.add_flags(scale=scale)

        for send in self.sends:
            send.signal(event, start_time, end_time)
