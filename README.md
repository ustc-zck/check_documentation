**<big>环境一致性验证</big>**

**运行环境**

支持的操作系统 

ubuntu16.04, ubuntu18.04, ubuntu20.04, centos7.X, centos8.X

python版本

python3.5以上

**运行步骤**

安装必要的库

    pip3 install -r requirements.txt

安装docker, nvidia-container-toolkit

    python3 main.py
    
监控使用的内存，再开一个窗口, 如果使用的显存大于申请的显存大小，终端会显示 "显存占用大于申请量"

    python3 memeory_monitor.py
