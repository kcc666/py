import os,time

def kill_powershell():
    while True:
        os.system('taskkill /IM powershell.exe /F')
        time.sleep(1)

kill_powershell()