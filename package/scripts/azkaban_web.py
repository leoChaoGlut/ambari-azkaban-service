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

from common import AZKABAN_WEB_URL, AZKABAN_NAME, AZKABAN_HOME, AZKABAN_CONF
from resource_management.core.exceptions import ExecutionFailed
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script


class WebServer(Script):
    def install(self, env):
        from params import java_home
        Execute('wget --no-check-certificate {0}  -O /tmp/{1}'.format(AZKABAN_WEB_URL, AZKABAN_NAME))
        Execute(
            'mkdir -p {0} {1} || echo "whatever"'.format(
                AZKABAN_HOME + '/conf',
                AZKABAN_HOME + '/extlib',
                AZKABAN_HOME + '/plugins/jobtypes',
            )
        )
        Execute('echo execute.as.user=false > {0} '.format(AZKABAN_HOME + '/plugins/jobtypes/commonprivate.properties'))
        Execute(
            'export JAVA_HOME={0} && tar -xf /tmp/{1} -C {2} --strip-components 1'.format(
                java_home,
                AZKABAN_NAME,
                AZKABAN_HOME
            )
        )
        self.configure(env)

    def stop(self, env):
        Execute('cd {0} && bin/azkaban-web-shutdown.sh'.format(AZKABAN_HOME))

    def start(self, env):
        self.configure(env)
        Execute('cd {0} && bin/azkaban-web-start.sh'.format(AZKABAN_HOME))

    def status(self, env):
        try:
            Execute(
                'export AZ_CNT=`ps -ef |grep -v grep |grep azkaban-web-server | wc -l` && `if [ $AZ_CNT -ne 0 ];then exit 0;else exit 1;fi `')
        except ExecutionFailed as ef:
            raise ef

    def configure(self, env):
        from params import azkaban_web_properties, azkaban_users_xml, global_properties, log4j_properties

        with open(path.join(AZKABAN_CONF, 'azkaban.properties'), 'w') as f:
            f.write(azkaban_web_properties['content'])

        with open(path.join(AZKABAN_CONF, 'azkaban-users.xml'), 'w') as f:
            f.write(azkaban_users_xml['content'])

        with open(path.join(AZKABAN_CONF, 'global.properties'), 'w') as f:
            f.write(global_properties['content'])

        with open(path.join(AZKABAN_CONF, 'log4j.properties'), 'w') as f:
            f.write(log4j_properties['content'])


if __name__ == '__main__':
    WebServer().execute()
