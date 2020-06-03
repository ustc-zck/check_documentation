import toml
from pynvml.smi import nvidia_smi

config = toml.load('config.toml')
#申请内存大小
memory = config["MEMORY"]

while(True):
    nvsmi = nvidia_smi.getInstance()
    results = nvsmi.DeviceQuery('memory.used')
    ##{'gpu': [{'fb_memory_usage': {'used': 0.0625, 'unit': 'MiB'}}, {'fb_memory_usage': {'used': 0.0625, 'unit': 'MiB'}}]}

    total_used = 0
    for item in results['gpu']:
        used = item['fb_memory_usage']['used']
        total_used += used

    if(total_used > memory * 1024):
        print("used memory exceeds the applied memory amount")
        break