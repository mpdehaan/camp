
class Event(object):
    def __init__(self, time=None, channel=None, notes=None, velocity=None, off=False, duration=None, flags=None):


        if channel is not None:
            assert type(channel) == int

        if velocity is not None:
            assert type(velocity) == int

        if flags is not None:
            assert type(flags) == dict
            self.flags = flags
        else:
            self.flags = dict()

        self.time = time
        self.channel = channel
        self.notes = notes
        self.velocity = velocity
        self.duration = duration
        self.off = off

    def add_flags(self, **kwargs):
        for (k,v) in kwargs.items():
            self.flags[k]=v

    def copy(self):
        return Event(
            time=self.time,
            channel=self.channel,
            notes=self.notes,
            velocity=self.velocity,
            duration=self.duration,
            flags=self.flags,
            off=self.off)

    def __repr__(self):
        return "<Event (time=%s,channel=%s,notes=%s,velocity=%s,off=%s,duration=%s,flags=%s)>" % \
            (self.time, self.channel, self.notes, self.velocity, self.off, self.duration, self.flags)
