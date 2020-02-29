# Intro
Ambari 集成 Azkaban

# Major Project Structure
- configuration : azkaban 配置文件
- bin : Azkaban脚本修改（单机部署web、exec需要更换） 
- package : 
  - scripts :  ambari 管理逻辑脚本
    - azkaban_executor.py  
    - azkaban_web.py
    - common.py
    - download.ini
    - params.py

# Deploy

- 1台服务器同时安装web、executor（需要修改azkaban的脚本，同时启动有冲突）
- web、executor分别部署在多台服务器（无需关心脚本）

# Usage

https://cwiki.apache.org/confluence/display/AMBARI/Overview
