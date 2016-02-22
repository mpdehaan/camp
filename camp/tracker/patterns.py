
from camp.band.selectors.endlessly import Endlessly
from camp.band.selectors.repeatedly import Repeatedly
from camp.band.selectors.randomly import Randomly

class Patterns(object):

    def __init__(self):
        pass

    def _produce(self):
        raise Exception("Patterns is not a thing, did you mean BasicPatterns, EndlessPatterns, RandomPatterns, or RepeatedPatterns?")

    def set(self, **kwargs):
        def callback(song):
            for (name, pattern) in kwargs.items():
                if isinstance(pattern, str):
                    pattern = pattern.replace("|","").split()
                song.patterns[name] = self._produce(pattern)
            return self
        return callback

class RandomPatterns(Patterns):

    def __init__(self, mode):
        self.mode = mode

    def _produce(self, pattern):
        return Randomly(pattern, mode=self.mode)

class EndlessPatterns(Patterns):

    def _produce(self, pattern):
        return Endlessly(pattern)

class BasicPatterns(Patterns):

    def _produce(self, pattern):
        return pattern

class RepeatedPatterns(Patterns):

    def __init__(self, hold=None):
        self.hold = hold

    def _produce(self, pattern):
        return Repeatedly(pattern, hold=self.hold)
