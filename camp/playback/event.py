
class Event(object):
    def __init__(self, typ=None, time=None, channel=None, notes=None, velocity=None, off=False, flags=None):

        assert typ in [ 'beat', 'note', 'note', 'silence']
        if channel is not None:
            assert type(channel) == int
        if velocity is not None:
            assert type(velocity) == int

        if flags is not None:
            assert type(flags) == dict
            self.flags = flags
        else:
            self.flags = dict()

        self.typ = typ
        self.time = time
        self.channel = channel
        self.notes = notes
        self.velocity = velocity
        self.off = off

    def add_flags(self, **kwargs):
        for (k,v) in kwargs.items():
            self.flags[k]=v

    def copy(self):
        return Event(typ=self.typ, time=self.time, channel=self.channel, notes=self.notes, velocity=self.velocity, flags=self.flags, off=self.off)

    def __repr__(self):
        return "<Event (typ=%s,time=%s,channel=%s,notes=%s,velocity=%s,off=%s,flags=%s)>" % (self.typ, self.time, self.channel, self.notes, self.velocity, self.off, self.flags)
