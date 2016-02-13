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

class Context(object):

    """
    A giant pointer keeping track of what we are doing, able to ask
    questions like "what's the note length" when it might be set on
    the note, or defaulted on the bar, pattern, or scene instead.
    """

    def __init__(self, song=None, play_speed=None):
        self.song = song
        self._play_speed = play_speed
        self._play_head = 0
        self._still_running = True
        self._scene_index = 0
        self._pattern_play_heads = dict()
        self._bar_index_for_scene = dict()

    def advance_play_head(self):
        self._play_head += self._play_speed
        # DO WE NEED TO ADVANCE THE PATTERN PLAY HEADS?  YES, IF CURRENT
        for pattern in self.active_patterns():
            self._pattern_play_heads[pattern] += self._play_speed

    def play_head(self):
        return self._play_head

    def current_patterns(self):
        return self.current_scene.patterns()

    def current_bars(self):
        # return the current bars in all patterns
        

    def restart():
        self._scene_index = 0
        self._play_head = 0

    def still_running(self):
        if not self._still_running:
            return False
        scene = self.current_scene()

        # if we're not at the last scene we are not done
        if scene != self.song.scenes[-1]:
            return True
        else:
            # if we are at the last scene, see if we've played beyond the end length
            for pattern in scene.patterns():
                ph_pat  = self._pattern_play_heads[pattern]
                pat_len = self.pattern_length_in_seconds(pattern=pattern)
                if (ph_pat > pat_len):
                    return False
            return True

    def pattern_length_in_seconds(self, pattern=None):
        raise Exception("WRONG")


    def stop(self):
        self._still_running = False

    def current_scene(self):
        return self.song.scenes[self._scene_index]

    def current_bar(self, pattern=None):
        assert pattern is not None
        bars = pattern.bars
        #scene = self.current_scene()
        #scene.bar[0]
        return bars[0]

    def cell_events(self, bar=None, pattern=None):
        return []


        # self.scene = None
        # self.pattern = None
        # self.bar = None
        # self.track = None
        # self.play_head = 0
