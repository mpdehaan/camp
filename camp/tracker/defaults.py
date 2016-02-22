
CODED_DEFAULTS = dict(
    bpm = 120,
    scene_bar_count = 1,
)


class Defaults(object):

    __slots__ = [ '_defaults', '_factory']

    def __init__(self, **kwargs):
        self._defaults = CODED_DEFAULTS
        self.set(**kwargs)

    def set(self, **kwargs):

        keys = CODED_DEFAULTS.keys()
        for (k,v) in kwargs.items():
            if k not in keys:
                raise Exception("invalid default setting: %s" % k)
            self._defaults[k] = v
        return self

    def as_dict(self):
        return self._defaults
