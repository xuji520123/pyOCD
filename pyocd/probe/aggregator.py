# pyOCD debugger
# Copyright (c) 2018-2020 Arm Limited
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pkg_resources

from ..core import exceptions
from ..core.plugin import load_plugin_classes_of_type
from .debug_probe import DebugProbe

## @brief Dictionary of loaded probe plugins indexed by name.
PROBE_CLASSES = {}

class DebugProbeAggregator(object):
    """! @brief Simple class to enable collecting probes of all supported probe types."""

    @staticmethod
    def get_all_connected_probes(unique_id=None):
        probes = []
        for cls in PROBE_CLASSES.values():
            probes += cls.get_all_connected_probes()
        
        # Filter by unique ID.
        if unique_id is not None:
            unique_id = unique_id.lower()
            probes = [probe for probe in probes if (unique_id in probe.unique_id.lower())]
        
        return probes
    
    @classmethod
    def get_probe_with_id(cls, unique_id):
        for cls in PROBE_CLASSES.values():
            probe = cls.get_probe_with_id(unique_id)
            if probe is not None:
                return probe
        else:
            return None

# Load plugins when this module is loaded.
load_plugin_classes_of_type('pyocd.probe', PROBE_CLASSES, DebugProbe)
