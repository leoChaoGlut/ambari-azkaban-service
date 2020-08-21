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

import os.path as path

from common import azkabanHome, azkabanWebTarUrl, azkabanWebTarName, \
    azkabanConfPath
from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script


class WebServer(Script):
    def install(self, env):
        tmpAzkabanWebTarPath = '/tmp/' + azkabanWebTarName
        Execute('wget --no-check-certificate {0} -O {1}'.format(azkabanWebTarUrl, tmpAzkabanWebTarPath))
        Execute('tar -xf {0} -C {1} --strip-components=1'.format(tmpAzkabanWebTarPath, azkabanHome))

        Execute(
            'cd {0} && '
            'chmod +x bin/start-web.sh && '
            'chmod +x bin/shutdown-web.sh && '
            'chmod +s bin/internal/internal-start-web.sh'.format(azkabanHome)
        )

        self.configure(env)

    def stop(self, env):
        Execute('cd {0} && ./bin/shutdown-web.sh'.format(azkabanHome))

    def start(self, env):
        self.configure(env)
        Execute('cd {0} && ./bin/start-web.sh'.format(azkabanHome))

    def status(self, env):
        try:
            Execute(
                'export AZ_CNT=`ps -ef |grep -v grep |grep azkaban-web-server | wc -l` && `if [ $AZ_CNT -ne 0 ];then exit 0;else exit 3;fi `'
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef


def configure(self, env):
    from params import azkaban_common, azkaban_web_properties, azkaban_users, global_properties, log4j_properties
    key_val_template = '{0}={1}\n'

    with open(path.join(azkabanConfPath, 'azkaban.properties'), 'w') as f:
        for key, value in azkaban_common.iteritems():
            f.write(key_val_template.format(key, value))
        for key, value in azkaban_web_properties.iteritems():
            if key != 'content':
                f.write(key_val_template.format(key, value))
        if azkaban_web_properties.has_key('content'):
            f.write(str(azkaban_web_properties['content']))

    with open(path.join(azkabanConfPath, 'azkaban-users.xml'), 'w') as f:
        if azkaban_users.has_key('content'):
            f.write(str(azkaban_users['content']))

    with open(path.join(azkabanConfPath, 'global.properties'), 'w') as f:
        if global_properties.has_key('content'):
            f.write(str(global_properties['content']))

    with open(path.join(azkabanConfPath, 'log4j.properties'), 'w') as f:
        if log4j_properties.has_key('content'):
            f.write(str(log4j_properties['content']))


if __name__ == '__main__':
    WebServer().execute()
