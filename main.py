#!/usr/bin/env python3

import argparse
import os
import sys
import yaml

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='name of your app', required=True, type=str)
    parser.add_argument('-k', '--kind', help='kind of your yaml file', required=True, type=str)
    parser.add_argument('-i', '--image', help='image you want to use', type=str)
    parser.add_argument('-s', '--selector', help='name of your selector', type=str)
    parser.add_argument('-p', '--port', help='number of your port', type=str)
    parser.add_argument('-r', '--replicas', help='count of your replicas', type=str)
    args=parser.parse_args()
   
    tempDict=createTempDict()

    if args.kind:    # we controlled kind field is empty or not
        if (list(args.kind)[0]=="p"): # We fixed lower inital letters
            kind=args.kind
            kind=kind.replace("p","P")
            api="v1" #we use v1 for pods
        else:
            kind=args.kind
            api="v1" #we use v1 for pods
    
    
        if (list(args.kind)[0]=="d"):
            kind=args.kind   # We fixed lower inital letters
            kind=kind.replace("d","D")
            api="apps/v1" #we use apps/v1 for deployments
 
        else:
            kind=args.kind
            api="apps/v1" #we use apps/v1 for deployments
 
 
    if args.image:
        tempDict["image"]=args.image
    
    if args.name:
        name=args.name
    
    if args.replicas and kind == "Deployment":
        replicas=int(kwargs["replicas"])
    else:
        replicas= None

    if args.port:
        tempDict["ports"]=int(args.port)
    
    

    try:
        yamlDict={
            "apiVersion":api,
            "kind":kind,     
            "metadata":{"labels":{"app":"%s"%(name,)}},
            "spec":{"selector":{"matchLabels":{"app":"%s"%(name,)}},"replicas":replicas,"template":{"metadata":{"labels":{"app":"%s"%(name,)}},"spec":{"containers":[{"name":name,"image":"%s"%(tempDict["image"],),"ports":[{"containerPort":tempDict["ports"]}],"volumeMounts":[{"name":tempDict["volumeName"],"mountPath":"%s"%(None,)}]}],"volumes":[{"name":tempDict["volumeName"]}]}}},
        }    
    except NameError:
        click.echo("You are missing define name or kind")
        return None
    
      
    try:
        with open(r"./deployment.yaml","w") as file:
            yaml.safe_dump((yamlDict),file)    
        print("{}/{} yaml file created. ".format(kind,name))
        
    except Exception as err:
        print(err)
    
    try:
        file=open("deployment.yaml","r")
        print(file.read())
        
    except Exception as err:
        print(err)



def createTempDict():
    titles=''
    index=0
    with open(r"./docker-compose.yml") as yFile:
        dcFile=yaml.full_load(yFile) # we read yaml file in dict type
    

    if len(list(dcFile["services"]))>1:
        print("services:")

        for item in list(dcFile["services"]):
            print(item )
        image=input("You have {} services in your docker-compose.yaml file, please choose a service: ".format(len(list(dcFile["services"]))))

        try:
            index=list(dcFile["services"]).index(image)
        except Exception:
            image=input("Please enter your service name correctly")
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