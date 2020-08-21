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
import socket
import time

from common import azkabanHome, azkabanExecTarUrl, azkabanExecTarName, azkabanConfPath
from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script


class ExecutorServer(Script):
    def install(self, env):
        tmpAzkabanExecTarPath = '/tmp/' + azkabanExecTarName
        Execute('wget --no-check-certificate {0} -O {1}'.format(azkabanExecTarUrl, tmpAzkabanExecTarPath))
        Execute('tar -xf {0} -C {1} --strip-components=1'.format(tmpAzkabanExecTarPath, azkabanHome))

        Execute(
            'cd {0} && '
            'chmod +x bin/start-exec.sh && '
            'chmod +x bin/shutdown-exec.sh && '
            'chmod +s bin/internal/internal-start-executor.sh'.format(azkabanHome)
        )

        self.configure(env)

    def stop(self, env):
        Execute('cd {0} && ./bin/shutdown-exec.sh'.format(azkabanHome))

    def start(self, env):
        self.configure(env)
        Execute('cd {0} && ./bin/start-exec.sh'.format(azkabanHome))
        from params import azkaban_common
        executor_port = int(azkaban_common['jetty.port'])
        while 1:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', executor_port))
            sock.close()
            if result == 0:
                Execute('curl -G "localhost:{0}/executor?action=activate" && echo'.format(executor_port))
                break
            else:
                time.sleep(3)

    def status(self, env):
        try:
            Execute(
                'export AZ_CNT=`ps -ef |grep -v grep |grep azkaban-exec-server | wc -l` && `if [ $AZ_CNT -ne 0 ];then exit 0;else exit 3;fi `'
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        from params import azkaban_executor_properties, log4j_properties, azkaban_common
        key_val_template = '{0}={1}\n'

        with open(path.join(azkabanConfPath + "/conf", 'azkaban.properties'), 'w') as f:
            for key, value in azkaban_common.iteritems():
                f.write(key_val_template.format(key, value))
            for key, value in azkaban_executor_properties.iteritems():
                if key != 'content':
                    f.write(key_val_template.format(key, value))
            if azkaban_executor_properties.has_key('content'):
                f.write(str(azkaban_executor_properties['content']))

        with open(path.join(azkabanConfPath, 'log4j.properties'), 'w') as f:
            if log4j_properties.has_key('content'):
                f.write(str(log4j_properties['content']))


if __name__ == '__main__':
    ExecutorServer().execute()
