mkdir -p /data/azkaban/executor
mkdir -p /data/azkaban/web

chmod +x /data/azkaban/web/bin/start-exec.sh
chmod +x /data/azkaban/web/bin/shutdown-exec.sh
chmod +x /data/azkaban/web/bin/internal/internal-start-web.sh


chmod +x /data/azkaban/executor/bin/start-exec.sh
chmod +x /data/azkaban/executor/bin/shutdown-exec.sh
chmod +x /data/azkaban/executor/bin/internal/internal-start-executor.sh








grant all privileges on azkaban.* to 'azkaban'@'dmp-az-executor001' identified by 'azkaban';
grant all privileges on azkaban.* to 'azkaban'@'dmp-az-executor002' identified by 'azkaban';
grant all privileges on azkaban.* to 'azkaban'@'dmp-az-executor003' identified by 'azkaban';
