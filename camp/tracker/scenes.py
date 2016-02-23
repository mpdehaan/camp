"""
Copyright 2016, Michael DeHaan <michael.dehaan@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from camp.tracker.scene import Scene

class Scenes(object):

    __slots__ = [ '_scenes', '_factory' ]

    def __init__(self):
        self._scenes = dict()

    def set(self, **scenes):

        def callback(song):

            for (scene_name, scene) in scenes.items():

                if getattr(scene, '__call__', None) is not None:
                    scene = scene(song)
                if not isinstance(scene, Scene):
                    raise Exception("only a Scene is allowed inside of Scenes set method, got %s" % scene)
                    
                self._scenes[scene_name] = scene
                scene._factory = song
                scene.build()
            return self

        return callback

    def as_dict(self):
        return self._scenes
