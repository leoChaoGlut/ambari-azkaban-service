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

import os

import ConfigParser

script_dir = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join(script_dir, 'download.ini')))

AZKABAN_HOME = '/usr/hdp/current/azkaban'
AZKABAN_NAME = 'azkaban'
AZKABAN_SQL = 'azkaban.sql'
AZKABAN_WEB_URL = config.get('download', 'azkaban_web_url')
AZKABAN_EXECUTOR_URL = config.get('download', 'azkaban_executor_url')
AZKABAN_DB_URL = config.get('download', 'azkaban_db_url')
AZKABAN_CONF = AZKABAN_HOME + '/conf'
