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

from common import AZKABAN_DB_URL, AZKABAN_WEB_URL, AZKABAN_NAME, AZKABAN_HOME, AZKABAN_CONF, AZKABAN_SQL
from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script


class WebServer(Script):
    def install(self, env):
        #from params import java_home, azkaban_db
        from params import  azkaban_db
        java_home='/usr/local/jdk1.8.0_171'
        Execute('wget --no-check-certificate {0}  -O /tmp/{1}'.format(AZKABAN_WEB_URL, AZKABAN_NAME))
        Execute('wget --no-check-certificate {0}  -O /tmp/{1}'.format(AZKABAN_DB_URL, AZKABAN_SQL))
        Execute(
            'mysql -h{0} -P{1} -D{2} -u{3} -p{4} < {5}'.format(
                azkaban_db['mysql.host'],
                azkaban_db['mysql.port'],
                azkaban_db['mysql.database'],
                azkaban_db['mysql.user'],
                azkaban_db['mysql.password'],
                '/tmp/{0}'.format(AZKABAN_SQL),
            )
        )
        Execute(
            'mkdir -p {0} {1} {2} || echo "whatever"'.format(
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
        self.configure(env)
    Execute('cd {0} && bin/shutdown-web.sh'.format(AZKABAN_HOME))

    def start(self, env):
        self.configure(env)
        Execute('cd {0} && bin/start-web.sh'.format(AZKABAN_HOME))

    def status(self, env):
        try:
        self.configure(env)
            Execute(
                'export AZ_CNT=`ps -ef |grep -v grep |grep azkaban-web-server | wc -l` && `if [ $AZ_CNT -ne 0 ];then exit 0;else exit 3;fi `'
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        from params import azkaban_db, azkaban_web_properties, azkaban_users, global_properties, log4j_properties
        key_val_template = '{0}={1}\n'

        with open(path.join(AZKABAN_CONF, 'azkaban.properties'), 'w') as f:
            for key, value in azkaban_db.iteritems():
                f.write(key_val_template.format(key, value))
            for key, value in azkaban_web_properties.iteritems():
                if key != 'content':
                    f.write(key_val_template.format(key, value))
            #f.write(azkaban_web_properties['content'])
        if azkaban_web_properties.has_key('content'):
                f.write(str(azkaban_web_properties['content']))

        with open(path.join(AZKABAN_CONF, 'azkaban-users.xml'), 'w') as f:
            if azkaban_users.has_key('content'):
            f.write(str(azkaban_users['content']))

        with open(path.join(AZKABAN_CONF, 'global.properties'), 'w') as f:
            #f.write(global_properties['content'])
            if global_properties.has_key('content'):
                f.write(str(global_properties['content']))

        with open(path.join(AZKABAN_CONF, 'log4j.properties'), 'w') as f:
            #f.write(log4j_properties['content'])
            if log4j_properties.has_key('content'):
                f.write(str(log4j_properties['content']))


if __name__ == '__main__':
    WebServer().execute()
