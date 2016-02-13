
class Event(object):
    def __init__(self, typ=None, time=None, channel=None, notes=None, velocity=None, off=False):

        assert typ in [ 'beat', 'note', 'note', 'silence']
        if channel is not None:
            assert type(channel) == int
        if velocity is not None:
            assert type(velocity) == int

        self.typ = typ
        self.time = time
        self.channel = channel
        self.notes = notes
        self.velocity = velocity
        self.off = off

    def copy(self):
        return Event(typ=self.typ, time=self.time, channel=self.channel, notes=self.notes, velocity=self.velocity)

    def __repr__(self):
        return "<Event (typ=%s,time=%s,channel=%s,notes=%s,velocity=%s,off=%s)>" % (self.typ, self.time, self.channel, self.notes, self.velocity, self.off)
