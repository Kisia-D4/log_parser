# 침해사고 분석 시 각종 시스템 자원 정보 수집 코드
import os
import subprocess

if not os.path.exists('result'):
    os.makedirs('result')

print('start')
print('=====================')
print('1. system info 수집')
if not os.path.exists('result/system'):
    os.makedirs('result/system')
systeminfo = subprocess.run('systeminfo', shell=True, text=True, capture_output=True)
systeminfo_text = systeminfo.stdout
with open(os.path.join('result/system', 'system_info.txt'), 'w') as file:
    file.write(systeminfo_text)

print('=====================')
print('2. env 수집')
if not os.path.exists('result/env'):
    os.makedirs('result/env')
env = subprocess.run('set', shell=True, text=True, capture_output=True)
env_text = env.stdout
with open(os.path.join('result/env', 'env.txt'), 'w') as file:
    file.write(env_text)

print('=====================')
print('3. process list 수집')
if not os.path.exists('result/process'):
    os.makedirs('result/process')
tasklist = subprocess.run('tasklist', shell=True, text=True, capture_output=True)
tasklist_text = tasklist.stdout
with open(os.path.join('result/process', 'process_list.txt'), 'w') as file:
    file.write(tasklist_text)

print('=====================')
print('4. service list 수집')
if not os.path.exists('result/service'):
    os.makedirs('result/service')
sc_query = subprocess.run('sc query', shell=True, text=True, capture_output=True)
sc_query_text = sc_query.stdout
with open(os.path.join('result/service', 'service_list.txt'), 'w') as file:
    file.write(sc_query_text)

print('=====================')
print('5. network port 수집')
if not os.path.exists('result/network'):
    os.makedirs('result/network')
netstat = subprocess.run('netstat -abno', shell=True, text=True, capture_output=True)
netstat_text = netstat.stdout
with open(os.path.join('result/network', 'network_port.txt'), 'w') as file:
    file.write(netstat_text)

print('=====================')
print('6. ipconfig 수집')
if not os.path.exists('result/ipconfig'):
    os.makedirs('result/ipconfig')
ipconfig = subprocess.run('ipconfig /all', shell=True, text=True, capture_output=True)
ipconfig_text = ipconfig.stdout
with open(os.path.join('result/ipconfig', 'ipconfig.txt'), 'w') as file:
    file.write(ipconfig_text)

print('=====================')
print('end')

