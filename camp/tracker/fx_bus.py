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

    def __init__(self, param_list):

        self._nodes = []

        if type(param_list) != list:
            raise Exception("The constructor to FxBus expects a list of dicts, got: %s" % param_list)

        for params in param_list:

            if type(params) != dict:
                raise Exception("The constructor to FxBus expects a list of dicts, got element: %s" % params)

            module = params.get('module', None)

            if module is None:
                raise Exception("'module' required in FxBus")

            namespace = "camp.band.members.%s" % module
            print("NAMESPACE=%s" % namespace)
            instance = instance_produce(namespace, module, [], exclude_dict(params, 'module'))
            self._nodes.append(instance)
