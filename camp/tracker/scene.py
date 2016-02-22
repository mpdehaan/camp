
class Scene(object):

    def __init__(self, scale=None, pre_fx=None, post_fx=None, patterns=None, bar_count=None):

        self.scale = scale
        self.pre_fx = pre_fx
        self.post_fx = post_fx
        self.patterns = patterns
        self.bar_count = bar_count

    def get_signals(self):
        raise NotImplementedError

    def get_output(self):
        raise NotImplementedError
