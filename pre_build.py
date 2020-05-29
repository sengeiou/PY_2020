#!/usr/bin/python
#_*_ coding:utf-8 _*_
#此脚本用来拉取open状态的提交

import subprocess
import os
import sys
import json
import re

root_dir=os.getcwd()
dict1={}
list1=[]	
list2=[]
list3=[]
#存放topic提交的列表
t_list=[]

def pull_code(PROT,HOST,BRANCH):
	if os.path.isdir("4250_code"):
		print("代码目录存在")
		os.system("rm -rf 4250_code")
		os.mkdir("4250_code")
		os.chdir(root_dir+"/4250_code")
		cmd1="repo init -u ssh://"+HOST+":"+PORT+"/manifest -m manifest.xml -b"+BRANCH
		ret1=subprocess.Popen(cmd1,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		ret1.wait()
		cmd2="repo sync"
		ret2=subprocess.Popen(cmd2,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		ret2.wait()
		cmd3="repo start base --all"
		ret3=subprocess.Popen(cmd3,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		ret3.wait()


#cherry-pick前进行信息提取操作
def do_progress(PORT,HOST,BRANCH,PROJECT):
	pull_code(PORT,HOST,BRANCH)	

	#1:查询所有open的提交形成list1
	sshcmd1="ssh -p "+str(PORT)+" "+HOST+" "+" gerrit query "+"branch:"+BRANCH+" project:"+PROJECT+" status:open --format JSON --current-patch-set --files | grep -E 'project|number|url'"
	child1 = subprocess.Popen(sshcmd1,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	child1.wait()
	list1=child1.stdout.readlines()

	#2：查询所有topic存放进list2
	for p in list1:
		topic=json.loads(p).get("topic")
		if not topic is None:
			list2.append(topic)
		else:
			list3.append(p)

	#3：遍历topic列表，将相同topic的提交存放同一个list
	for topic in list2:
		list_temp= get_same_topic_change(topic)
		list3.append(list_temp)

	#去除重复
	for i in list3:
		if i not in t_list:
			t_list.append(i)

#查询相同topic的提交函数
def get_same_topic_change(topic):
	sshcmd2="ssh -p "+str(PORT)+" "+HOST+" "+" gerrit query "+"branch:"+BRANCH+" project:"+PROJECT+" topic:"+topic+" status:open --format JSON --current-patch-set --files | grep -E 'project|number|url'"
	child2=subprocess.Popen(sshcmd2,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	child2.wait()
	list_temp=child2.stdout.readlines()
	return list_temp
			

def do_cherry_pick(USER):
	#path_dir=
	#进入本地path目录，进行cherry-pick
	os.chdir(root_dir+"/4250_code/"+path_dir)
	sshcmd3="git fetch ssh://"+USER+"@"+HOST+":"+PORT+"/"+name+" "+change_url+" "+"&&"+" git cherry-pick FETCH_HEAD"
	child3 = subprocess.Popen(sshcmd3,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	child3.wait()
	print(child3.stdout.read())

	returncode=child3.returncode
	if returncode == 0:
		return True
		print("cherry-pick成功！")
	else:
		return False
		print("cherry-pick失败！")

def usage():
	print("="*120)
	print('argv[1]:gerrit port')
	print('argv[2]:gerrit ip')
	print('argv[3]:branch name')
	print('argv[4]:project name,for example:^alps/.*')
	print('argv[5]:gerrit user')
	print('='*120)

##############################################3
if __name__=="__main__":
	PORT=sys.argv[1]
	HOST=sys.argv[2]
	BRANCH=sys.argv[3]
	PROJECT=sys.argv[4]
	USER=sys.argv[5]

	pull_code(PORT,HOST,BRANCH)
	do_progress(PORT,HOST,BRANCH,PROJECT)
	#do_cherry_pick(USER)	
