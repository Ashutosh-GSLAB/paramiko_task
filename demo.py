import paramiko
import pytest

host = "192.168.43.136"
port = 22
username = "ashutosh"
password = "123"
command = "free | grep Mem | awk '{print ($2-$7)/$2 * 100}'"            # percentage of memory utilization
command1 = "df -h"                    # display file system disk space in human readable format
command2 = "ls"                       # list of directory content
command3 = "lscpu"                    # display information about the CPU architecture

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())             # connecting to servers without a known host key
ssh.connect(host, port, username, password)                           # automatically adding the hostname
#print("Connection Successful")

def runSsh(cmd):
    userName = "ashutosh"
    password = "123"
    hostname = "192.168.43.136"
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        paramiko.util.log_to_file("filename.log")
        ssh.connect(hostname, username=userName, port=22, password=password)
        print("connected to host", host)
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
        result = stdout.read()
        result1 = result.decode()
        print()
        error = stderr.read().decode('utf-8')

        if not error:
            ssh.close()
        return result1
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials: %s")

def test_memory():
    memoryUtil = float(runSsh(command))
    assert memoryUtil < 90

def test_contentlist():
    fileList = runSsh(command2)
    print("The Files present are : \n", fileList)

def test_cpuinfo():
    cpuinfo = runSsh(command3)
