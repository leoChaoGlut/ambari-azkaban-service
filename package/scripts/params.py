#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from resource_management.libraries.script.script import Script

# config object that holds the configurations declared in the config xml file
config = Script.get_config()

azkaban_web_properties = config['configurations']['azkaban-web.properties']
azkaban_executor_properties = config['configurations']['azkaban-executor.properties']
azkaban_users = config['configurations']['azkaban-users']
azkaban_db = config['configurations']['azkaban-db']
global_properties = config['configurations']['global.properties']
log4j_properties = config['configurations']['log4j.properties']

host_info = config['clusterHostInfo']
host_level_params = config['hostLevelParams']
java_home = host_level_params['java_home']
