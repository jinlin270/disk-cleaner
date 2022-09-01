import subprocess
import os
print("setting up environment")
print("======================================")
print("installing pip")
try:
    subprocess.run(["python3", "-m", "ensurepip", "--default-pip"], check=True)
    # subprocess.run(["sudo", "apt", "install", "python3-pip"], check=True)
    os.system("python3 -m pip install --upgrade pip")
except subprocess.CalledProcessError as error:
    print(error)

print("======================================")
print("installing Pyaml")
subprocess.run(["pip3", "install", "PyYAML"], check=True)


print("======================================")
print("installing schedule")
subprocess.run(["pip3", "install", "schedule"], check=True)


print("======================================")
print("installing progressbar")
subprocess.run(["pip", "install", "progressbar2"], check=True)

print("======================================")
print("installing requests")
subprocess.run(["pip", "install", "requests"], check=True)

print("======================================")
print("installing tox")
subprocess.run(["pip", "install", "tox"], check=True)

