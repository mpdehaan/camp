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

from camp.utils import instance_produce, exclude_dict
from camp.band.selectors.endlessly import Endlessly

# FxBus([
#     dict(module='velocity', levels='velocity_pt1'),
#    dict(module='duration', levels='duration_pt1')
# ]),

class FxBus(object):

    def __init__(self):

        self._nodes = []

    def set(self, param_list):

        def callback(song):

            # FIXME: in any function where song is passed in, remove references to _factory in all files
            self._factory = song

            print("-- FORMING MODULES --")

            if type(param_list) != list:
                raise Exception("The constructor to FxBus expects a list of dicts, got: %s" % param_list)

            for params in param_list:

                print("PARAMS: %s" % params)

                if type(params) != dict:
                    raise Exception("The constructor to FxBus expects a list of dicts, got element: %s" % params)

                module = params.get('module', None)
                if module is None:
                    raise Exception("'module' required in FxBus")

                namespace = "camp.band.members.%s" % module

                params_out = dict()

                for (k,v) in params.items():

                    if k == 'module':
                        pass
                    elif isinstance(v, str):
                        # FIXME: DO WE WANT TO HAVE A SPECIFIC SYNTAX TO DENOTE A PATTERN LOOKUP RATHER THAN DOING IT IMPLICITLY?
                        # (yes, shouty, maybe important)
                        if v in song.patterns:
                            v = song.patterns[v]
                        params_out[k] = v
                    elif type(v) == list:
                        params_out[k] = Endlessly(v)
                    else:
                        raise Exception("unknown pattern type: %s" % v)

                instance = instance_produce(namespace, module, [], params_out)
                print("--> INSTANCE: %s" % instance)
                self._nodes.append(instance)

            return self

        return callback

    def nodes(self):
        return [ node.copy() for node in self._nodes ]
