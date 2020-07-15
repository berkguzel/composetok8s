import os
import yaml
import ruamel.yaml
import sys



with open(r"./docker-compose.yml") as yFile:
    dcFile=yaml.full_load(yFile) # we read yaml file in dict type


firstItem=list(dcFile["services"])[0] # first services name from docker-compose

titles=list(dcFile["services"][firstItem])#we will hold subtitles below of big title
#these both variables will help us to access data we need rapidly on dcFile 

def creatingTempDict():

    tempDict={}
    for item in titles: # it gets values of titles
        value=str(dcFile["services"][firstItem][item])
        tempDict[item]=value # created tempDict to use data more efficiently
    
    ports=tempDict["ports"].split(":",2) #ports were getten in list form we had to convert it to str
    ports=ports[1].split("']",2)
    #ports=int(ports[0])
    tempDict["ports"]=int(ports[0]) # we need integer to define port number
    tempDict["name"]="ops"

    # collected all data are in a place(dictionary type) which calls with tempDict then we will get them 
    # we collected in dict type because converting dict to yaml is easy

    return tempDict



def creatingYamlDict():
    tempDict=creatingTempDict() # we called tempDict to get data at below
    yamlDict={
        "apiVersiion": "apps/v1",
        "kind":"deployment",
        "metadata":{"name":"%s-deployment"%(tempDict["name"],),"labels":{"app":"%s"%(tempDict["name"],)}},
        "spec":{"selector":{"matchLabels":{"app":"%s"%(tempDict["name"],)}},"template":{"metadata":{"labels":{"app":"%s"%(tempDict["name"],)}},"spec":{"containers":{"- name":tempDict["name"],"image":"%s"%(tempDict["image"],),"ports":{"containerPort":tempDict["ports"]}}}}}
    }

    # we made ready yamlDict thus converting dict to yaml will be easy  

    return yamlDict



def converting():
    yamlDict=creatingYamlDict() # called prepared to converting yamlDict

    

    with open(r"./deployment.yaml","w") as file:
        newYaml=yaml.safe_dump(yamlDict, file) # dict to yaml converting place

    return newYaml



converting()
























#firstItem=list(dcFile["services"])[0] # first services name
#item=dcFile["services"][firstItem]["image"]

#getting all items from yaml
"""
for key, value in dcFile.items():
    print(key, value)
"""
"""
with open(r"./deployment.yaml") as file:
    newyaml=yaml.dump(dcFile, file)
print(newyaml)
"""



