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

# FxBus([
#     dict(module='velocity', levels='velocity_pt1'),
#    dict(module='duration', levels='duration_pt1')
# ]),

class FxBus(object):

    def __init__(self):

        self._nodes = []

    def set(self, param_list):

        def callback(song):

            if type(param_list) != list:
                raise Exception("The constructor to FxBus expects a list of dicts, got: %s" % param_list)

            for params in param_list:

                if type(params) != dict:
                    raise Exception("The constructor to FxBus expects a list of dicts, got element: %s" % params)

                module = params.get('module', None)
                if module is None:
                    raise Exception("'module' required in FxBus")

                    namespace = "camp.band.members.%s" % module

                    params_out = dict()
                    for (k,v) in params.items():
                        if k == 'module':
                            continue
                            if isinstance(v, str):
                                if v not in self._factory.patterns:
                                    raise Exception("referenced pattern is not defined: %s" % v)
                                else:
                                    v = self._factory.patterns[v]
                                    params_out[k] = v

                    instance = instance_produce(namespace, module, [], params_out)
                    self._nodes.append(instance)

            return self

        return callback

    def nodes(self):
        return self._nodes
