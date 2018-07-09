#SSH to router and get CPU & Memory statistics
import paramiko
import re
from datetime import datetime
import pickle

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.174.128', username='admin', password='admin')
ssh.exec_command('terminal length 0')

def ssh_exec_command(device,cmd):
    stdin, stdout, stderr = device.exec_command(cmd)    
    return stdout.readlines()

top_output = ssh_exec_command(ssh,'show processes node-id 1')
current_time = str(datetime.now())

try:
    with open('mem_monitor.txt', 'rb') as handle:
        proc_list = pickle.loads(handle.read())
except:
    proc_list = []

temp_dict = {}

for line in top_output:
    match_mem = re.search('KiB Mem :  (\d+) total,   (\d+) free,  (\d+) used,',line)
    match_cpu = re.search('%Cpu\(s\):  \S+ us,  \S+ sy,  \S+ ni, (\S+) id,',line)
    if match_mem:
        mem_usage = int(match_mem.group(3))
        print mem_usage
    if match_cpu:
        cpu_usage = str(round((100.0-float(match_cpu.group(1))),2))
        print cpu_usage
temp_dict[current_time] = {'memory_usage' : mem_usage, 'cpu_usage' : cpu_usage}
proc_list.append(temp_dict)
print proc_list

with open('mem_monitor.txt','wb') as handle:
    pickle.dump(proc_list,handle)