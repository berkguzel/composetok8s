This repository's purpose is helping to beginners who want to jump in the Kubernetes from Docker. It will convert your docker-compose.yaml file to a different yaml file form(Pod, Deployment) to use in Kubernetes. It is not proper for either complex files nor big deployments, just for fun :)

# USAGE
1. Run `docker run -it 227500/composetok8s:0.1 --name= --kind=  ` this command will give deployment.yaml file as output on terminal.
1. Run `docker run -it -v "$PWD:/app" 227500/composetok8s:0.1 --name= --kind=  ` this command will create deployment.yaml file in your current directory.

 

# 
1. Run `docker build -t //yourtage .`
1. Run `docker run -it //yourtage --name= --kind`
1. deployment.yaml file will be showed as output in your terminal

#
1. Run `git clone https://github.com/berkguzel/composetok8s.git` in where your docker-compose.yml is.
1. Run `python3 main.py --name= --kind=`
1. deployment.yaml file will be created in your current directory
