from camp.band.member import Member
from camp.playback.event import Event
from camp.utils import loop_around

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

        assert type(scales) == list
        if channel is not None:
            self.channel = channel

        super().__init__()

        self.scale_spec_looper = loop_around(scales)
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

        scale = next(self.scale_gen)
        event.add_flags(scale=scale)

        for send in self.sends:
            send.signal(event, start_time, end_time)
