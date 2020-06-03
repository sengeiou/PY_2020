#!/usr/bin/python
#_*_ coding:utf-8 _*_
#此脚本用来拉取open状态的提交

import subprocess
import os
import sys
import json
import re

reload(sys)
sys.setdefaultencoding('utf8')

root_dir=os.getcwd()
list1=[]	
list2=[]
list3=[]
#存放所有提交的列表
t_list=[]
#存放以change_number为key,提交信息为value的字典列表
dict1={}

def pull_code():
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
def do_progress():
	#pull_code()	

	#1:查询所有open的提交形成list1
	sshcmd1="ssh -p "+str(PORT)+" "+HOST+" "+" gerrit query "+"branch:"+BRANCH+" project:"+PROJECT+" status:open --format JSON --current-patch-set --files | grep -E 'project|number|url'"
	child1 = subprocess.Popen(sshcmd1,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	child1.wait()
	list1=child1.stdout.readlines()


	#2：查询所有topic存放进list2
	for p in list1:
		change_number=json.loads(p).get("number")
		topic=json.loads(p).get("topic")
		if not topic is None:
			list2.append(topic)
		else:
			list3.append([change_number])
		dict1[change_number]=json.loads(p)

	#3：遍历topic列表，将相同topic的提交number存放同一个list,形成list3
	for topic in list2:
		list_temp= get_same_topic_change(topic)
		list3.append(list_temp)
		

	#去除重复,形成最终t_list
	for i in list3:
		if i not in t_list:
			t_list.append(i)
	


#查询相同topic的提交函数
def get_same_topic_change(topic):
	sshcmd2="ssh -p "+str(PORT)+" "+HOST+" "+" gerrit query "+"branch:"+BRANCH+" project:"+PROJECT+" topic:"+topic+" status:open --format JSON --current-patch-set --files | grep -E 'project|number|url'"
	child2=subprocess.Popen(sshcmd2,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	child2.wait()
	ret1=child2.stdout.readlines()
	list_temp=[]
	for i in ret1:
		change_number=json.loads(i).get("number")
		list_temp.append(change_number)
	return list_temp
			
#遍历t_list,进行拖提交
def get_info():
	for subnumber in t_list:
		count=1
		for number in subnumber:
			do_cherry_pick(number,count)
		
#拖提交函数
def do_cherry_pick(number,count):
	os.chdir(root_dir+"/4250_code")
	NAME=dict1[number].get("project")
	CHANGE_URL=dict1[number1].get("currentPatchSet").get("ref")
	s1="repo list "+NAME+" -p"
	c1=subprocess.Popen(s1,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	c1.wait()
	PATH_DIR=c1.stdout.readline().replace("\n","")
	
	#进入本地path目录，进行cherry-pick
	os.chdir(root_dir+"/4250_code/"+PATH_DIR)
	s2="git checkout -b "+branch+str(count)
	c2=subprocess.Popen(s2,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	c2.wait()
	s3="git fetch ssh://"+USER+"@"+HOST+":"+PORT+"/"+NAME+" "+CHANGE_URL+" "+"&&"+" git cherry-pick FETCH_HEAD"
	c3=subprocess.Popen(s3,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	c3.wait()

	returncode=c3.wait()
	if returncode == 0:
		count+=1
		print(NAME+":cherry-pick成功！")
	else:
		print(NAME+":cherry-pick失败！")
		s4="git  cherry-pick --abort"
		c4=subprocess.Popen(s4,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		c4.wait()
		#s5="git checout "+"branch"+str(count-1)
		#c5=subprocess.Popen(s4,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		#c5.wait()

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

	do_progress()
	get_info()
