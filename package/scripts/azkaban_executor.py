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

import json
import os.path as path
import time
from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script

from common import azkabanHome, azkabanExecTarUrl, azkabanExecTarName, azkabanConfPath, jdk11TarName, jdk11Home, \
    jdk11Url, exportJavaHomeAndPath


class ExecutorServer(Script):
    def install(self, env):
        # download jdk11 and extract jdk11 tarball
        tmpJdk11Path = '/tmp/' + jdk11TarName
        Execute('mkdir -p {0}'.format(jdk11Home))
        Execute('wget --no-check-certificate {0} -O {1}'.format(jdk11Url, tmpJdk11Path))
        Execute('tar -xf {0} -C {1} --strip-components=1'.format(tmpJdk11Path, jdk11Home))

        Execute('yum install -y python-requests')

        tmpAzkabanExecTarPath = '/tmp/' + azkabanExecTarName
        Execute('mkdir -p {0}'.format(azkabanHome))
        Execute('wget --no-check-certificate {0} -O {1}'.format(azkabanExecTarUrl, tmpAzkabanExecTarPath))
        Execute('tar -xf {0} -C {1} --strip-components=1'.format(tmpAzkabanExecTarPath, azkabanHome))

        Execute('cd ' + azkabanHome + ' && mv bin/shutdown-exec.sh bin/stop-exec.sh')

        Execute(
            'cd {0} && '
            'chmod +x bin/start-exec.sh && '
            'chmod +x bin/stop-exec.sh && '
            'chmod +s bin/internal/internal-start-executor.sh'.format(azkabanHome)
        )

        self.configure(env)

    def stop(self, env):
        self.configure(env)

        Execute('cd ' + azkabanHome + ' && ' + exportJavaHomeAndPath + ' && ./bin/stop-exec.sh')

    def start(self, env):
        self.configure(env)

        from params import azkaban_executor_properties

        executorPort = azkaban_executor_properties['executor.port']

        Execute('cd ' + azkabanHome + ' && ' + exportJavaHomeAndPath + ' && ./bin/start-exec.sh')

        url = 'http://localhost:{0}/executor?action=ping'.format(executorPort)
        maxRetryCount = 30
        retryCount = 0
        import requests
        while True:
            try:
                resp = requests.get(url)
                print(resp.text)
                if json.loads(resp.text)['status'] == 'alive':
                    print('executor is alive')
                    Execute('curl -G "localhost:{0}/executor?action=activate" && echo'.format(executorPort))
                    print('after activate')
                    break
            except:
                print('executor is not alive')
            time.sleep(1)
            retryCount += 1
            if retryCount > maxRetryCount:
                raise Exception('Exec start failed')

    def status(self, env):
        # TODO 可优化,和start逻辑一致
        try:
            Execute(
                'export AZ_CNT=`ps -ef |grep -v grep |grep "azkaban.execapp.AzkabanExecutorServer" | wc -l` && `if [ $AZ_CNT -ne 0 ];then exit 0;else exit 3;fi `'
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        from params import azkaban_executor_properties, log4j_properties, azkaban_common, global_properties
        key_val_template = '{0}={1}\n'

        with open(path.join(azkabanConfPath, 'azkaban.properties'), 'w') as f:
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

        with open(path.join(azkabanConfPath, 'global.properties'), 'w') as f:
            if global_properties.has_key('content'):
                f.write(str(global_properties['content']))


if __name__ == '__main__':
    ExecutorServer().execute()
