#!/usr/bin/python
#_*_ coding:utf-8 _*_


import json
import xlrd
import xlwt
import re
from HTMLTable import HTMLTable

CR_LIST=[]
CR_COM=[]
CR_DES=[]
CR_ASS=[]
PROJECT_LIST=[]
COMMIT_ID_LIST=[]
GERRIT_ID_LIST=[]

def write_execle():
	workbook=xlwt.Workbook(encoding="utf-8")
	sheet1=workbook.add_sheet('changelist',cell_overwrite_ok=True)
	row0=['CR Number','CR Component/s','CR Description','CR Assignee','Local Repository Path','Commit ID (SHA1)','Gerrit ID']
	for i in range(0,len(row0)):
		sheet1.write(0,i,row0[i])
	
	with open("gerrit_info.txt") as f1:
		for line in f1.readlines():
			msg_list=json.loads(line)
			cr=msg_list.get("subject")
			#CR=cr.split(" ")[0].strip(":")
			CR=re.findall(r"\w+-\d+",cr)
			CR_LIST.append(CR)

			cr_com=msg_list.get("")			
			CR_COM.append(cr_com)

			cr_des=msg_list.get("commitMessage")
			c=cr_des.split("\n")[0]
			CR_DES.append(c)

			cr_ass=msg_list.get("currentPatchSet").get("username")
			CR_ASS.append(cr_ass)

			p_git=msg_list.get("project")
			PROJECT_LIST.append(p_git)

			commit_id=msg_list.get("currentPatchSet").get("revision")
			COMMIT_ID_LIST.append(commit_id[:10])

			gerrit_id=msg_list.get("number")
			GERRIT_ID_LIST.append(gerrit_id)

			for j in range(0,len(PROJECT_LIST)):
				sheet1.write(j+1,0,CR_LIST[j])
				sheet1.write(j+1,1,CR_COM[j])
				sheet1.write(j+1,2,CR_DES[j])
				sheet1.write(j+1,3,CR_ASS[j])			
				sheet1.write(j+1,4,PROJECT_LIST[j])
				sheet1.write(j+1,5,COMMIT_ID_LIST[j])
				sheet1.write(j+1,6,GERRIT_ID_LIST[j])	

	workbook.save("changelist.xls")

def write_html():
	f = open("change_list.html",'w')
	message = """
	<html>
	<head></head>
	<Title>changelist</Title>
	<body>
		<table border="1">
			<tr>
				<td>CR NUMBER</td>
				<td>CR Component/s</td>
				<td>CR Description</td>
				<td>CR Assignee</td>
				<td>Local Repository Path</td>
				<td>Commit ID(SHA1)</td>
				<td>Gerrit ID</td>
			</tr>
			<tr>
				<td>%CR_LIST</td>
				<td>%CR_COM</td>
				<td>%CR_DES</td>
				<td>%CR_ASS</td>
				<td>%PROJECT_LIST</td>
				<td>%COMMIT_ID_LIST</td>
				<td>%GERRIT_ID_LIST</td>
			<tr>
		</table>
	</body>
	</html>""" % (CR_LIST,CR_COM,CR_DES,CR_ASS,PROJECT_LIST,COMMIT_ID_LIST,GERRIT_ID_LIST)
	f.write(message)
	f.close()


if __name__=="__main__":
	write_execle()
	write_html()

