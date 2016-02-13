

class Member(object):

    def __init__(self, channel=None):
        self.sends = []
        self.channel = channel

    def send_to(self, obj):
        self.sends.append(obj)

    def signal(self, event):
        for item in self.sends:
            item.signal(event)
