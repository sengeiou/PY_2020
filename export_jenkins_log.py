#!/usr/bin/python
#导出jenkins控制台的log

import jenkins
import requests

jenkins_url="http://jenkins.mot.com"
username="gaoyx9"
password="gyx050400??"
job_name="QZB30.Q4_borneo-retail_userdebug_mq-2020-q4_r-qsm2020_test-keys_continuous"
job_number=742

server=jenkins.Jenkins(jenkins_url, username=username, password=password)
#得到指定job控制台输出的log信息息
jobLog=server.get_build_console_output(job_name,job_number)
#将jenkins log写入文件中
with open("jenkins_lot.txt","w") as f1:
	f1.write(jobLog)

