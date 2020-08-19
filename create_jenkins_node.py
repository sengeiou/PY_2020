#!/usr/bin/python
#_*_ coding:utf-8 _*_

import jenkins

jenkins_url="http://192.168.137.1:8088/"
username="scm"
password="scm"
server=jenkins.Jenkins(jenkins_url,username,password)

#创建节点的参数
params={
	"port":22,
	"username":"gaoyx",
	"credentialsId":"b0066466-73a9-401a-abf7-c16678c4def2",
	"host":"192.168.56.101",
}
#创建节点服务器
server.create_node("slave",nodeDescription='my test slave',remoteFS='/home/gaoyx',labels='precise',exclusive=True,launcher=jenkins.LAUNCHER_SSH,launcher_params=params)

