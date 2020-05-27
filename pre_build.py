#!/usr/bin/python
#_*_ coding:utf-8 _*_

import subprocess
import os
import sys
import json

dir_name="/home/ubuntu/SM4250/SM4250"
#进入到代码目录
os.chdir(dir_name)

PORT="29418"
HOST="192.168.56.101"
PROJECT_NAME="^alps/.*"
BRANCH_NAME="master"
USER="ubuntu"
#字典1：存放name
dict1={}
#字典2：存放ref
dict2={}
#字典3：存放path
dict3={}
#存放cherry-pick的信息
list1=[]

def do_cherry_pick():
	#得到此项目open提交
	sshcmd="ssh -p "+str(PORT)+" "+HOST+" "+" gerrit query "+"branch:"+BRANCH_NAME+" project:"+PROJECT_NAME+" status:open --format JSON --current-patch-set --files | grep -E 'project|number|url'"
	child = subprocess.Popen(sshcmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	#读取open提交内容
	context=child.stdout.readlines()
	#遍历读取的内容，并提取有效信息，存入字典
	for p in context:
		project1=json.loads(p).get("project")
		dict1["name"]=project1
		refs=json.loads(p).get("currentPatchSet").get("ref")
		dict2["ref"]=refs

		#根据name得到本地对应的path
		sshcmd2="repo list | grep "+project1+" | awk '{print $1}'"
		child2=subprocess.Popen(sshcmd2,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		path1=child2.stdout.readline().replace("\n","")
		dict3["path"]=path1
		list1=[dict1,dict2,dict3]

		#进入本地path目录，进行cherry-pick	
		path_dir=list1[2].get("path")
		os.chdir(dir_name+"/"+path_dir)

		name=list1[0].get("name")
		change_url=list1[1].get("ref")
		sshcmd3="git fetch ssh://"+USER+"@"+HOST+":"+PORT+"/"+name+" "+change_url+" "+"&&"+" git cherry-pick FETCH_HEAD"
		child3 = subprocess.Popen(sshcmd3,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

##############################################3
if __name__=="__main__":
	do_cherry_pick()
