#!/usr/bin/python
#_*_ coding:utf-8 _*_
#此脚本用来拉取open状态的提交

import subprocess
import os
import sys
import json
import getopt

dir_name="/home/ubuntu/SM4250/SM4250"
#字典1：存放name
dict1={}
#字典2：存放ref
dict2={}
#字典3：存放path
dict3={}
args_list=sys.argv

def do_progress(PORT,HOST,BRANCH_NAME,PROJECT_NAME):
	#进入到代码目录
	os.chdir(dir_name)
	#得到此项目open提交
	sshcmd="ssh -p "+str(PORT)+" "+HOST+" "+" gerrit query "+"branch:"+BRANCH_NAME+" project:"+PROJECT_NAME+" status:open --format JSON --current-patch-set --files | grep -E 'project|number|url'"
	child = subprocess.Popen(sshcmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	child.wait()
	#读取open提交内容
	global context
	context=child.stdout.readlines()
	#遍历读取的内容，并提取有效信息，存入字典
	for p in context:
		project1=json.loads(p).get("project")
		dict1["name"]=project1
		refs=json.loads(p).get("currentPatchSet").get("ref")
		dict2["ref"]=refs

		#根据name得到本地对应的path
		sshcmd2="repo list "+project1+" -p"
		child2=subprocess.Popen(sshcmd2,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		child2.wait()
		path1=child2.stdout.readline().replace("\n","")
		dict3["path"]=path1
		#存放cherry-pick的信息
		list1=[dict1,dict2,dict3]

		#定义全局的path,name,ref
		global path_dir
		global name
		global change_url
		path_dir=list1[2].get("path")
		name=list1[0].get("name")
		change_url=list1[1].get("ref")


		#进行cherry-pick操作
		do_cherry_pick(USER)

def do_cherry_pick(USER):
	#进入本地path目录，进行cherry-pick
	os.chdir(dir_name+"/"+path_dir)
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
	print("参数的使用示例")

def args_parse():
	print("START TO PARSE ARGS")
	args = getopt.getopt(args_list[1:],"h",["port","host","branch_name","project_name","user"])
	print(args)
	for key,value in opts:
		if key == "-h":
			usage()
		elif key == "--port":
			PORT=value
		elif key == "--host":	
			HOST=value
		elif key == "--branch_name":
			BRANCH_NAME=value
		elif key == "--project_name":
			PROJECT_NAME=value
		elif key == "--user":
			USER=value

##############################################3
if __name__=="__main__":
	if len(sys.argv) < 5:
		usage()
	else:
		PORT=sys.argv[1]
		HOST=sys.argv[2]
		PROJECT_NAME=sys.argv[3]
		BRANCH_NAME=sys.argv[4]
		USER=sys.argv[5]
		args_parse()
		#do_progress(PORT,HOST,BRANCH_NAME,PROJECT_NAME)
