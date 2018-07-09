import paramiko
import re

output = '''
OS10# show processes node-id 1
top - 11:09:29 up 36 min,  2 users,  load average: 0.10, 0.26, 0.30
Tasks: 224 total,   1 running, 222 sleeping,   0 stopped,   1 zombie
%Cpu(s):  1.8 us,  3.1 sy,  0.0 ni, 94.5 id,  0.5 wa,  0.0 hi,  0.1 si,  0.0 st
KiB Mem :  2040284 total,   389136 free,  1367588 used,   283560 buff/cache
KiB Swap:   204024 total,   204024 free,        0 used.   517412 avail Mem
  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
 9633 admin     20   0   41180   3272   2652 R 12.5  0.2   0:00.03 top
    1 root      20   0  139964   7656   5272 S  0.0  0.4   0:03.38 systemd
    2 root      20   0       0      0      0 S  0.0  0.0   0:00.00 kthreadd
    3 root      20   0       0      0      0 S  0.0  0.0   0:01.99 ksoftirqd/0
    5 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 kworker/0:0H
    6 root      20   0       0      0      0 S  0.0  0.0   0:00.01 kworker/u2:0
'''

for line in output.split('\n'):
    match_mem = re.search('KiB Mem :  (\d+) total,   (\d+) free,  (\d+) used,', line)
    match_cpu = re.search('%Cpu\(s\):  (\S+) us,  (\S+) sy,  (\S+) ni, (\S+) id,',line)
    if match_mem:
        print 'memory match found'
        print 'Total System Memory is %s' % match_mem.group(1)
        print 'Total Used Memory is %s' % match_mem.group(3)
        print 'Total Free Memory is %s' % match_mem.group(2)
    if match_cpu:
        print 'cpu match found'
        print 'Current User CPU usage %s' % match_cpu.group(1)
        print 'Current System CPU usage %s' % match_cpu.group(2)
        print 'Current Idle CPU usage %s' % match_cpu.group(4)
