import toml
from pynvml.smi import nvidia_smi
import psutil

config = toml.load('config.toml')

#申请内存大小
memory = config["MEMORY"]
#申请显存大小
v_memory = config["V_MEMORY"]

while(True):

    used_memory = 0
    used_memory = psutil.virtual_memory().used
    if(used_memory > memory * 1024 * 1024 * 1024):
        print("内存消耗大于申请量")
    nvsmi = nvidia_smi.getInstance()
    results = nvsmi.DeviceQuery('memory.used')
    ##{'gpu': [{'fb_memory_usage': {'used': 0.0625, 'unit': 'MiB'}}, {'fb_memory_usage': {'used': 0.0625, 'unit': 'MiB'}}]}

    used_v_memory = 0
    for item in results['gpu']:
        used = item['fb_memory_usage']['used']
        used_v_memory += used

    if(used_v_memory  > v_memory * 1024):
        print("显存消耗大于申请量")

    
    
