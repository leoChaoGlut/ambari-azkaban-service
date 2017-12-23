# Intro
Ambari 集成 presto
官方的项目仅支持 rpm 形式的安装,该项目支持 tar 形式安装.
# Major Project Structure
- configuration : presto 配置文件
- package : 
  - scripts :  ambari 管理逻辑脚本
    - common.py : 
    - download.ini : preseto-tar & presto-cli 的下载信息配置
    - params.py :  ambari 参数和 presto 参数
    - presto_cli.py : cli ambari 管理逻辑
    - presto_client.py : 测试是否安装成功
    - presto_coordinator.py coordinator ambari 管理逻辑
    - presto_worker.py : worker ambari 管理逻辑
