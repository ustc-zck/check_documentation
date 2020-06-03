import subprocess
import toml

#配置文件
config = toml.load('config.toml')

distribution = subprocess.check_output('echo $(. /etc/os-release;echo $ID$VERSION_ID)', shell=True)
d = str(distribution)[2:-3]

#安装docker
if(d[:6] == 'ubuntu'):
    subprocess.call('apt-get remove -y docker docker-engine docker.io containerd runc', shell=True)
    subprocess.call('apt-get update', shell=True)
    subprocess.call('apt-get install -y systemd', shell=True)
    subprocess.call('apt-get -y install \
                    apt-transport-https \
                    ca-certificates \
                    curl \
                    gnupg-agent \
                    software-properties-common', shell=True)
    subprocess.call('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -', shell=True)
    subprocess.call('add-apt-repository \
                    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
                    $(lsb_release -cs) \
                    stable"', shell=True)
    subprocess.call('apt-get update', shell=True)
    subprocess.call('apt-get install -y docker-ce docker-ce-cli containerd.io', shell=True)
    #subprocess.call('apt-get update')
    #subprocess.call('snap install -y docker', shell=True)
    #subprocess.call('apt-get install -y docker.io', shell=True)
    #subprocess.call('systemctl start docker', shell=True)
    #subprocess.call('systemctl daemon-reload', shell=True)
    #安装nvidia docker
    
    #选择版本
    temp = 'distribution=' + d
    subprocess.call(temp, shell=True)
    subprocess.call('curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -', shell=True)
    
    temp = 'curl -s -L https://nvidia.github.io/nvidia-docker/' + str(d) + '/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list'
    subprocess.call(temp, shell=True)
    subprocess.call('apt-get update && apt-get install -y nvidia-container-toolkit', shell=True)
    subprocess.call('systemctl restart docker', shell=True)
else:
    subprocess.call('yum remove -y docker \
                    docker-client \
                    docker-client-latest \
                    docker-common \
                    docker-latest \
                    docker-latest-logrotate \
                    docker-logrotate \
                    docker-engine', shell=True)
    subprocess.call('yum install -y yum-utils', shell=True)
    subprocess.call('yum-config-manager \
                    --add-repo \
                    https://download.docker.com/linux/centos/docker-ce.repo', shell=True)
    subprocess.call('yum-config-manager --enable docker-ce-nightly', shell=True)
    subprocess.call('yum-config-manager --enable docker-ce-test', shell=True)


    subprocess.call('yum install -y docker-ce docker-ce-cli containerd.io', shell=True)
    subprocess.call('systemctl start docker', shell=True)
    subprocess.call('systemctl daemon-reload', shell=True)
    #安装nvidia docker
    distribution = subprocess.check_output('echo $(. /etc/os-release;echo $ID$VERSION_ID)', shell=True)
    d = str(distribution)[2:-3]
    temp = 'distribution=' + str(d)
    subprocess.call(temp, shell=True)
    temp = 'curl -s -L https://nvidia.github.io/nvidia-docker/' + str(d) + '/nvidia-docker.repo | tee /etc/yum.repos.d/nvidia-docker.repo'
    subprocess.call(temp, shell=True)
    subprocess.call('yum install -y nvidia-container-toolkit', shell=True)
    subprocess.call('systemctl restart docker', shell=True)

#选择镜像版本
image_version = config['IMAGE_VERSION']

#建立镜像
if(image_version == 'ubuntu14.04_nvi418.87'):
    subprocess.call('docker image build -t ubuntu14.04_nvi418.87:v01  -f ./Dockerfile_Ubuntu14.04/Dockerfile .', shell=True)
else:
    subprocess.call('docker image build -t centos7.5_nvi418.87:v01  -f ./Dockerfile_Centos7.5/Dockerfile .', shell=True)

#解压缩文件
FILE_PATH = config['FILE_PATH']
temp = 'tar -xvf' + ' ' + FILE_PATH
subprocess.call(temp, shell=True)

temp = 'docker run --gpus all --net=host --privileged=true -it '

#环境变量和动态库
ENVs = config['ENVs']

#设置环境变量
for env in ENVs:
    temp += ' --env '
    temp += env

WORKDIR = config["WORKDIR"]
temp += ' -w ' + str(WORKDIR)

RUN = "/AIservice -m=0 -c=aiges.toml -u=http://10.1.87.70:6868 -p=guiderAllService -g=gas -s=xats"

#文件目录
FILE_DIR = FILE_PATH[:FILE_PATH.rfind('/')]

#资源目录
RESOURCE_DIRs = config['RESOURCE_DIRs']
for RESOURCE_DIR in RESOURCE_DIRs:
    temp += ' -v ' + str(RESOURCE_DIR) + ':' + str(RESOURCE_DIR)

if(image_version == 'ubuntu14.04_nvi418.87'):
    temp += ' -v' + ' ' + str(FILE_DIR) + ':' + str(FILE_DIR) + ' ' + 'ubuntu14.04_nvi418.87:v01' + ' ' + WORKDIR + RUN
else:
    temp += ' -v' + ' ' + str(FILE_DIR) + ':' + str(FILE_DIR) + ' ' + 'centos7.5_nvi418.87:v01' + ' ' + WORKDIR + RUN

subprocess.call(temp, shell=True)


