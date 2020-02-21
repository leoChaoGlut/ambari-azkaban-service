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
import time
import socket
from common import AZKABAN_EXECUTOR_URL, AZKABAN_NAME, AZKABAN_HOME, AZKABAN_CONF
from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script


class ExecutorServer(Script):
    def install(self, env):
        #from params import java_home
        java_home='/usr/local/jdk1.8.0_171'
        Execute('wget --no-check-certificate {0}  -O /tmp/{1}'.format(AZKABAN_EXECUTOR_URL, AZKABAN_NAME))
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
        Execute('cd {0} && bin/shutdown-exec.sh'.format(AZKABAN_HOME))

    def start(self, env):
        from params import azkaban_executor_properties
        self.configure(env)
        executor_port = int(azkaban_executor_properties['executor.port']) 
        Execute('cd {0} && bin/start-exec.sh'.format(AZKABAN_HOME))
        while 1:
           sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           result = sock.connect_ex(('127.0.0.1',executor_port))
           sock.close()
       if result == 0:
          Execute('curl http://localhost:{0}/executor?action=activate'.format(executor_port))
          break
       else:
         time.sleep(5) 

    def status(self, env):
        try:
        self.configure(env)
            Execute(
                'export AZ_CNT=`ps -ef |grep -v grep |grep azkaban-exec-server | wc -l` && `if [ $AZ_CNT -ne 0 ];then exit 0;else exit 3;fi `'
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        from params import azkaban_executor_properties, log4j_properties, azkaban_db
        key_val_template = '{0}={1}\n'

        with open(path.join(AZKABAN_CONF, 'azkaban.properties'), 'w') as f:
            for key, value in azkaban_db.iteritems():
                f.write(key_val_template.format(key, value))
            for key, value in azkaban_executor_properties.iteritems():
                if key != 'content':
                    f.write(key_val_template.format(key, value))
            #f.write(azkaban_executor_properties['content'])
            if azkaban_executor_properties.has_key('content'):
                f.write(str(azkaban_executor_properties['content']))

        with open(path.join(AZKABAN_CONF, 'log4j.properties'), 'w') as f:
            #f.write(log4j_properties['content'])
            if log4j_properties.has_key('content'):
            f.write(str(log4j_properties['content']))


if __name__ == '__main__':
    ExecutorServer().execute()
