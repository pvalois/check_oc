#!/usr/bin/env python3 

import os,sys
import subprocess
import json
import shlex
import requests 

mmwebhooks="{{mattermost_webhook}}"

os.chdir (os.path.dirname(sys.argv[0]))

server=os.uname()[1]

##################################################################################################################

def check_co():

    cpt=0

    args=["oc","get","co"]
    output = subprocess.Popen(args, stdout=subprocess.PIPE, universal_newlines=True).communicate()

    for line in output[0].split("\n"):
      if (len(line)==0): continue
      words=shlex.split(line)
      if (words[2]=="False" or words[4]=="True"):
        cpt+=1
    
    return(cpt)

def check_nodes():

    cpt=0

    args=["oc","get","nodes"]
    output = subprocess.Popen(args, stdout=subprocess.PIPE, universal_newlines=True).communicate()

    for line in output[0].split("\n"):
      if (len(line)==0): continue
      if ("NAME" in line): continue
      if ("Ready" not in line):  
        cpt+=1

    return(cpt)

def check_pods():

    cpt=0

    args=["oc","get","pods","-A"]
    output = subprocess.Popen(args, stdout=subprocess.PIPE, universal_newlines=True).communicate()

    for line in output[0].split("\n"):
      if (len(line)==0): continue
      if ("NAME" in line): continue
      words=shlex.split(line)
      if (words[3] not in ["Running","Completed","Terminating","ContainerCreating"]):
        cpt+=1

    return(cpt)

try: 
  coerr=check_co()
except:
  coerr=0

try: 
  nodeerr=check_nodes(server)
except: 
  nodeerr=0

try: 
  #poderr=check_pods(server)
  poderr=0
except:
  poderr=0


if (coerr+nodeerr+poderr==0): exit(0)

rar=[]

if coerr>0: rar.append(str(coerr)+" co")
if nodeerr>0: rar.append(str(nodeerr)+ " nodes")
if poredd>0: rar.append(str(poderr)+" pods")
report="** Cluster "+server+" errors ** ("+", ".join(rar)+")"

if (mmwebhooks!=""):
  headers = {'Content-Type': 'application/json',}
  values = json.dumps({ "text": report})

  response = requests.post(mmwebhooks, headers=headers, data=values) 

