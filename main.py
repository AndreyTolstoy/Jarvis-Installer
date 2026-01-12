import requests
import subprocess
import os
import zipfile
from pathlib import Path
import time
import colorama

URL = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-embed-amd64.zip"
REP = "https://github.com/AndreyTolstoy/Jarvis/archive/refs/heads/main.zip"
PIP = "https://bootstrap.pypa.io/get-pip.py"

start = time.time()
colorama.init()
colorama.just_fix_windows_console()

J = Path(subprocess.run(
   ["powershell", "-NoProfile", "-Command", "Add-Type -AssemblyName System.Windows.Forms;" "$f=New-Object System.Windows.Forms.FolderBrowserDialog;" "if($f.ShowDialog() -eq 'OK'){Write-Output $f.SelectedPath}"], 
   capture_output=True, text=True).stdout.strip()) / "Jarvis"

data = {
   "pth" : "python311.zip\npython311\\site-packages\n.\nimport site\n",
   "bat" : f"@echo off\ncd /d '%~dp0'\n..\..\python\python.exe run.py",
   "task_manager" : rf"""
$a = New-ScheduledTaskAction `
    -Execute '{J}\python\python.exe' `
    -Argument 'run.py' `
    -WorkingDirectory '{J}\Jarvis-main\Jarvis-main'

Register-ScheduledTask `
    -TaskName 'JarvisStarter' `
    -Action $a `
    -Trigger (New-ScheduledTaskTrigger -AtLogOn) `
    -Force
"""
}



def output(text, color="GREEN"):
   print(colorama.Style.BRIGHT + getattr(colorama.Fore, color) + text + colorama.Style.RESET_ALL)


def install_py(): 
    output("Requesting python.org...", color="BLUE")
    get = requests.get(URL) 
    get.raise_for_status()
    write_installed_file(f"{J}\\python.zip", get.content)

def install_Jarvis():
    output("Requesting github.com...", color="BLUE")
    get = requests.get(REP) 
    get.raise_for_status()
    write_installed_file(f"{J}\\Jarvis-main.zip", get.content)

def write_installed_file(path, content):
   with open(path, "wb") as f:
      f.write(content)
   
   unzip(path)
   output(path[:-4] + " status: Downloaded and unziped")


def unzip(path):
   with zipfile.ZipFile(path, "r") as f:
      f.extractall(path[:-4])

   os.remove(path)
         

def rewrite_python311_pth():
    with open(f"{J}\\python\\python311._pth", "w") as f:
        f.write(data["pth"])

def get_pip():
    get = requests.get(PIP)
    get.raise_for_status()
    with open(f"{J}\\get-pip.py", "wb") as f: 
        f.write(get.content) 
    
    subprocess.run([f"{J}\\python\\python.exe", f"{J}\\get-pip.py"], shell=False)
    os.remove(f"{J}\\get-pip.py")


def download_lib():
    subprocess.run([f"{J}\\python\\python.exe", "-m", "pip", "install", "-r",  f"{J}\\Jarvis-main\\Jarvis-main\\requirements.txt"], shell=False)
    starter_bat()


def starter_bat():
    with open(f"{J}\\Jarvis-main\\Jarvis-main\\start.bat", "w") as f:
        f.write(data["bat"])
    
    output("Runner .bat: Done")


def auto_starter_status():
    while True:
     keyboard = input("Do u want add 'Jarvis' to task manager (Start with system)? (Y/N) ").upper().strip()
     if keyboard == "Y":
      task_manager()
      return
     
     elif keyboard == "N":
      return
     
     else:
        pass

def task_manager():
   subprocess.run(
       ["powershell.exe", "-NoProfile", "-Command", data["task_manager"]],
       check=True
   )

   output("Task manager: Done")


    

print(colorama.Style.BRIGHT + "===Jarvis Installer v0.0.2===" + colorama.Style.RESET_ALL)
if not Path(J).exists():
 os.makedirs(J)
 install_py()
 install_Jarvis()
 rewrite_python311_pth()

 output("Rewrite ._pth: Done")
 get_pip()

 output("PIP: Downloaded")
 download_lib() 

 output("Libs: Downloaded")
 auto_starter_status()

 output("Download completed in " + str(round(time.time() - start)) + "seconds")

else:
   output("Jarvis already install or u already have a folder named 'Jarvis' in this folder (please rename it)")

input("Press Enter to exit...")