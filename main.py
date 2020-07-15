import click
import os
import yaml
import yamlOps






"""
path="./docker-compose.yml"
mode=0o666
flags=os.O_RDWR | os.O_CREAT
fd=os.open(path, flags, mode)

str=os.read(fd,os.path.getsize(fd))
print(str.decode())
os.close(fd)
print(fd)
"""
"""
with open(r"./docker-compose.yml") as yFile:
    dcFile=yaml.full_load(yFile) # we read yaml file in dict type

firstItem=list(dcFile["services"])[0] # first services name
dcFile["services"][firstItem]["image"])
"""