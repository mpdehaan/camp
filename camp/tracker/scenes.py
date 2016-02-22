
class Scenes(object):

    __slots__ = [ '_scenes', '_factory' ]

    def __init__(self):
        self._scenes = dict()

    def set(self, **scenes):

        def callback(song):
            for (scene_name, scene) in scenes:
                if not isinstance(bus, Scene):
                    raise Exception("only a Scene is allowed inside of Scenes set method")
                    self._scenes[scene_name] = scene
                    scene.factory = song

        return callback
