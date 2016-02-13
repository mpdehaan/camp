

class Member(object):

    def __init__(self, channel=None):
        self.sends = []
        self.channel = channel

    def send_to(self, obj):
        self.sends.append(obj)

    def signal(self, event):
        """ Do not reimplement signal in subclasses - only on_signal """

        if event.channel is None:
            print("member :: setting channel to :: %s" % self.channel)
            event.channel = self.channel
        self.on_signal(event)

    def on_signal(self, event):
        for item in self.sends:
            if item.channel is None:
                item.channel = self.channel
            item.signal(event)
