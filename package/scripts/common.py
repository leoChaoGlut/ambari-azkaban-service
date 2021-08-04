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

import ConfigParser
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join(script_dir, 'download.ini')))

azkabanHomePrefix = '/home/service/var/data1'
azkabanHome = azkabanHomePrefix + '/azkaban'
azkabanConfPath = azkabanHome + '/conf'

azkabanWebTarUrl = config.get('download', 'azkaban_web_tar_url')
azkabanExecTarUrl = config.get('download', 'azkaban_executor_tar_url')

azkabanWebTarName = azkabanWebTarUrl.split('/')[-1]
azkabanExecTarName = azkabanExecTarUrl.split('/')[-1]

jdk11Url = config.get('download', 'jdk11_url')
jdk11TarName = jdk11Url.split('/')[-1]
jdk11Home = azkabanHomePrefix + '/jdk11/'

exportJavaHomeAndPath = ' export JAVA_HOME=' + jdk11Home + ' && export PATH=${JAVA_HOME}/bin:$PATH '
