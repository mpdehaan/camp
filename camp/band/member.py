

class Member(object):

    """
    camp.band.member Member is the base class for all band member plugins.
    Each implements on_signal below.
    """

    def __init__(self, channel=None):
        """
        Not every band member must specify a MIDI channel, but along each
        line in the chain it should be specified somewhere.
        """
        self.sends = []
        self.channel = channel

    def send_to(self, obj):
        """
        Indicates what band members this band member informs.
        This can be thought as the opposite of listens_to.
        """
        self.sends.append(obj)

    def listens_to(self, obj):
        """
        An alternate way of recording a communication arrangement
        that is a bit more natural.
        """
        obj.sends.append(self)

    def signal(self, event, start_time, end_time):
        """
        Fires the beat or note events down through the chain.
        Do not reimplement signal in subclasses - only on_signal
        """

        if event.channel is None:
            event.channel = self.channel
        self.on_signal(event, start_time, end_time)

    def on_signal(self, event, start_time, end_time):
        """
        Override this pattern in each plugin, with variations.
        """

        # for each musician that is listening to us
        for item in self.sends:

            # FIXME - needed?
            # if item.channel is None:
            #    item.channel = self.channel

            # tell the musician what events we have seen, and what the length
            # of the current beat cycle is
            item.signal(event, start_time, end_time)
