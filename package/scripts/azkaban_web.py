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
from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script

from common import azkabanHome, azkabanWebTarUrl, azkabanWebTarName, \
    azkabanConfPath, jdk11TarName, jdk11Home, jdk11Url, exportJavaHomeAndPath


class WebServer(Script):
    def install(self, env):
        # download jdk11 and extract jdk11 tarball
        tmpJdk11Path = '/tmp/' + jdk11TarName
        Execute('mkdir -p {0}'.format(jdk11Home))
        Execute('wget --no-check-certificate {0} -O {1}'.format(jdk11Url, tmpJdk11Path))
        Execute('tar -xf {0} -C {1} --strip-components=1'.format(tmpJdk11Path, jdk11Home))

        # Execute('yum install -y python-requests')

        tmpAzkabanWebTarPath = '/tmp/' + azkabanWebTarName
        Execute('mkdir -p {0}'.format(azkabanHome))
        Execute('wget --no-check-certificate {0} -O {1}'.format(azkabanWebTarUrl, tmpAzkabanWebTarPath))
        Execute('tar -xf {0} -C {1} --strip-components=1'.format(tmpAzkabanWebTarPath, azkabanHome))

        Execute('cd ' + azkabanHome + ' && mv bin/shutdown-web.sh bin/stop-web.sh')

        Execute(
            'cd {0} && '
            'chmod +x bin/start-web.sh && '
            'chmod +x bin/stop-web.sh && '
            'chmod +s bin/internal/internal-start-web.sh'.format(azkabanHome)
        )

        self.configure(env)

    def stop(self, env):
        self.configure(env)

        Execute('cd ' + azkabanHome + ' && ' + exportJavaHomeAndPath + ' && ./bin/stop-web.sh')

    def start(self, env):
        self.configure(env)

        Execute('cd ' + azkabanHome + ' && ' + exportJavaHomeAndPath + ' && ./bin/start-web.sh')

        #
        # maxRetryCount = 10
        # retryCount = 0
        #
        # from params import host_info, azkaban_executor_properties
        # executor_port = int(azkaban_executor_properties['executor.port'])
        # execHosts = host_info['azkaban_executor_hosts']
        # urlTmpl = 'http://{0}:{1}/executor?action=getStatus'
        # import requests
        # while True:
        #     for execHost in execHosts:
        #         try:
        #             url = urlTmpl.format(execHost, executor_port)
        #             print(url)
        #             resp = requests.get(url)
        #             print(resp.text)
        #             if json.loads(resp.text)['isActive'] == 'true':
        #                 Execute('cd {0} && ./bin/start-web.sh'.format(azkabanHome))
        #                 return
        #         except:
        #             print('web is not alive')
        #         time.sleep(0.5)
        #     time.sleep(1)
        #     retryCount += 1
        #     if retryCount > maxRetryCount:
        #         raise Exception('web start failed')

    def status(self, env):
        try:
            Execute(
                'export AZ_CNT=`ps -ef |grep -v grep |grep "azkaban.webapp.AzkabanWebServer" | wc -l` && `if [ $AZ_CNT -ne 0 ];then exit 0;else exit 3;fi `'
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
