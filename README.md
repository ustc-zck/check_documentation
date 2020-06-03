**环境一致性验证**
==========================

**运行环境**
-------------------

支持的操作系统  ubuntu16.04, ubuntu18.04, ubuntu20.04, centos7.X, centos8.X

python版本 python3.5以上

**配置文件**
----------

程序文件进行打包，压缩成tar文件，例如AIGES-v2.4.3.tar.gz

配置文件config.toml需要提供压缩包文件路径，主程序工作目录，资源目录，镜像版本，环境变量和申请的显存存量，以AIGES-v2.4.3为例
    
    压缩包AIGES-v2.4.3.tar.gz路径， FILE_PATH="/root/CHECK/AIGES-v2.4.3.tar.gz" 
    
    主程序AIService在此目录下， WORKDIR = "/root/CHECK/AIGES-v2.4.3/output" 
    
    资源目录，存在多个资源目录的话，以数组成员形式加入， RESOURCE_DIRs = ["/data1"] 
    
    线上环境的镜像版本，可选择的版本有ubuntu14.04_nvi418.87和centos7.5_nvi418.87， IMAGE_VERSION = "ubuntu14.04_nvi418.87" 
    
    环境变量，多个环境变量以数组成员的形式加入，ENVs = ["LD_LIBRARY_PATH=/root/CHECK/AIGES-v2.4.3/output"] 
    
    申请的显存大小，单位是G， MEMORY = 4 

**运行步骤**
----------------------

安装必要的库

    pip3 install -r requirements.txt

监控使用的内存，如果使用的显存大于申请的显存大小，终端会显示 "显存消耗大于申请量"

    python3 memeory_monitor.py

再开一个终端， 运行程序

    python3 main.py

**查看日志**
----------------------
如果运行异常，进入容器查看日志

    


    
