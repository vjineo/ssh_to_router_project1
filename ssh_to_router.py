#SSH to router and execute 'show version'
import paramiko
import re
import operator

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.157.128', username='admin', password='admin')
ssh.exec_command('terminal lenght 0')

def ssh_exec_command(device,cmd):
    stdin, stdout, stderr = device.exec_command(cmd)    
    return stdout.readlines()
    
output = ssh_exec_command(ssh,'show version')
for line in output:
    find_uptime = re.search('Up Time:\s+(\d+):(\d+):(\d+)',line)
    if find_uptime:
	    print 'Device uptime is %s Hours %s Minutes & %s Seconds' % (find_uptime.group(1), find_uptime.group(2), find_uptime.group(3))

top_output = ssh_exec_command(ssh,'show processes node-id 1')
temp_dict = {}
for line in top_output:
    match_mem = re.search('KiB Mem :  (\d+) total,   (\d+) free,  (\d+) used,',line)
    match_cpu = re.search('%Cpu\(s\):  \S+ us,  \S+ sy,  \S+ ni, (\S+) id,',line)
    match_proc = re.search('\d+\s+\S+\s+\d+\s+\d+\s+\d+\s+(\d+)\s+\d+ \S\s+(\S+)\s+(\S+)\s+\S+\s+(\S+)',line)
    if match_mem:
        print 'Current Free Memory is %s' % match_mem.group(2)
    if match_cpu:
        print 'Current CPU usage is %s percent' % (100.0-float(match_cpu.group(1)))
    if match_proc:
        temp_dict[str(match_proc.group(4))] = {'memory' : int(match_proc.group(1)),
                      'cpu_usage' : float(match_proc.group(2)), 'memory_usage' : float(match_proc.group(3))}

temp_list = sorted(temp_dict, key=lambda x: (temp_dict[x]['memory']), reverse=True)
print '%15s %15s %15s %15s' % ('Proccess', 'Memory','CPU usage','Memory usage')
total_memory = 0
for list in temp_list:
    total_memory += int(temp_dict[list]['memory'])
    print '%15s %15s %15s %15s' % (list, temp_dict[list]['memory'], temp_dict[list]['cpu_usage'], temp_dict[list]['memory_usage'])
print 'Total memory used is %s' % total_memory

    