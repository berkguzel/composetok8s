import os
import yaml
import ruamel.yaml



with open(r"./docker-compose.yml") as yFile:
    dcFile=yaml.full_load(yFile) # we read yaml file in dict type


firstItem=list(dcFile["services"])[0] # first services name

titles=list(dcFile["services"][firstItem])#we gonna hold subtitles below of big title

def creatingTempDict():

    tempDict={}
    for item in titles: # it gets values of titles
        value=str(dcFile["services"][firstItem][item])
        tempDict[item]=value # created tempDict to use data more efficiently
    
    ports=tempDict["ports"].split(":",2) #ports were getten in list form we had to convert it to str
    ports=ports[1].split("']",2)
    #ports=int(ports[0])
    tempDict["ports"]=int(ports[0])
    tempDict["name"]="ops"

    return tempDict



def creatingYamlDict():
    tempDict=creatingTempDict()

    yamlDict={
        "apiVersiion": "apps/v1",
        "kind":"deployment",
        "metadata":{"name":"%s-deployment"%(tempDict["name"],),"labels":{"app":"%s"%(tempDict["name"],)}},
        "spec":{"selector":{"matchLabels":{"app":"%s"%(tempDict["name"],)}},"template":{"metadata":{"labels":{"app":"%s"%(tempDict["name"],)}},"spec":{"containers":{"name":tempDict["name"],"image":"%s"%(tempDict["image"],),"ports":{"containerPort":tempDict["ports"]}}}}}
    }
    return yamlDict


def converting():
    yamlDict=creatingYamlDict()

    with open(r"./deployment.yaml","w") as file:
        newYaml=yaml.dump(yamlDict, file, default_flow_style=False)

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



