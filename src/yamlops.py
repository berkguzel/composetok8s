import click
import os
import sys
import yaml
import click
import fire 
from ruamel.yaml import YAML
from collections import OrderedDict


@click.command()
@click.option('--name',type=str,help='name of your app',default="")
@click.option('--kind',type=str,help='Kind or Deployment',default="")
@click.option('--image',type=str,help='title of your image',default="")
@click.option('--selector',type=str,help='name of your selector',default="")
@click.option('--ports',type=str,help='number of your port',default="")
@click.option('--replicas',type=str,help='count of your replicas',default="")
@click.option('--mountPath',type=str,help='mount path of your volume',default="")



def main(**kwargs):

   
    tempDict=createTempDict()

 

    if kwargs["replicas"]!="":
        replicas=int(kwargs["replicas"])
    else:
        replicas=None

    if kwargs["ports"]!="":
        tempDict["ports"]=int(kwargs["ports"])

    """
    if kwargs["mountPath"]!="":
        mountPath=kwargs[mountPath]
    else:
        mountPath=None

    if kwargs["selector"]!="":
        name=kwargs["selector"]
    """

    if kwargs["image"]!="":
        tempDict["image"]=kwargs["image"]


    if kwargs["kind"]!="":    # we controlled kind field is empty or not
        if (list(kwargs["kind"])[0]=="p"): # We fixed lower inital letters
            kind=kwargs["kind"]
            kind=kind.replace("p","P")
        else:
            kind=kwargs["kind"]
    
    
        if (list(kwargs["kind"])[0]=="d"):
            kind=kwargs["kind"]             # We fixed lower inital letters
            kind=kind.replace("d","D")
        else:
            kind=kwargs["kind"]
    
    
        if kwargs["kind"]=="Pod":
            api="v1" #we use v1 for pods
        else:
            api="apps/v1" #we use apps/v1 for deployments
    
    
    if kwargs["name"]!="":
        name=kwargs["name"]

    try:
        yamlDict={
            "apiVersion":api,
            "kind":kind,     
            "metadata":{"name":"%s-%s"%(name,kind,),"labels":{"app":"%s"%(name,)}},
            "spec":{"selector":{"matchLabels":{"app":"%s"%(name,)}},"replicas":replicas,"template":{"metadata":{"labels":{"app":"%s"%(name,)}},"spec":{"containers":[{"name":name,"image":"%s"%(tempDict["image"],),"ports":[{"containerPort":tempDict["ports"]}],"volumeMounts":[{"name":tempDict["volumeName"],"mountPath":"asd"}]}],"volumes":[{"name":tempDict["volumeName"]}]}}},
        }
    
    except NameError:
        click.echo("You are missing define name or kind")
        return None
    

    
    yaml=YAML()    
    yaml.compact(seq_seq=False, seq_map=False)
    with open(r"./deployment.yaml","w") as file:
        yaml.dump(yamlDict,file)
    click.echo("{}/{} ".format(kind,name))


def createTempDict():
    with open(r"./docker-compose.yml") as yFile:
        dcFile=yaml.full_load(yFile) # we read yaml file in dict type
    

    if len(list(dcFile["services"]))>1:
        print("services:")

        for item in list(dcFile["services"]):
            print(item )
        image=click.prompt("You have {} services in your docker-compose.yaml file, please choose a service".format(len(list(dcFile["services"]))))

        try:
            index=list(dcFile["services"]).index(image)
        except ValueError as err:
            image=click.prompt("Please enter your service name correctly")
            index=list(dcFile["services"]).index(image)


    
        

    firstItem=list(dcFile["services"])[int(index)]

    #firstItem1=list(dcFile["services"])[1] # first services name from docker-compose
    titles=list(dcFile["services"][firstItem])#we will hold subtitles below of big title
    #these both variables will help us to access data we need rapidly on dcFile 
 

    tempDict={}
   
    for item in titles: # it gets values of titles
        value=str(dcFile["services"][firstItem][item])
        tempDict[item]=value # created tempDict to use data more efficiently
    
    
    try:
        volumeName=list(dcFile["volumes"])[int(index)] # we took volume name of volume created in compose file
        tempDict["volumeName"]=volumeName
    except IndexError:
        tempDict["volumeName"]=""

                    
    try:
        ports=tempDict["ports"].split(":",2) #ports were getten in list form we had to convert it to str
        ports=ports[1].split("']",2)
        tempDict["ports"]=int(ports[0]) # 
    except KeyError:
        tempDict["ports"]=""

    return tempDict



if __name__ == "__main__":
    main()