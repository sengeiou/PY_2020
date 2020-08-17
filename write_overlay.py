#!/usr/bin/python
#_*_ coding:utf-8 _*_
#此脚本用来写入overlay表格
#需要overlay into文件提交准备好

import xlwt

def write_excel():
	#设置单元格背景色
	style = xlwt.easyxf('pattern: pattern solid, fore_colour green;')
	
	workbook=xlwt.Workbook(encoding="utf-8")
	#创建一个表格文件
	sheet1=workbook.add_sheet(u"sheet1",cell_overwrite_ok=True)

	#读取文件的内容写入表格中
	count=0
	with open("overlay_info.txt") as f1:
		for line in f1.readlines():	
			for i in line.split():
				count=count+1
				#如果是标题行，则设置背景颜色为绿色
				if((i=="DEVICE_PACKAGE_OVERLAYS") or (i=="PRODUCT_PACKAGE_OVERLAYS")):
					sheet1.write(count,0,i,style)
					sheet1.write(count,1,"Check owner",style)
					sheet1.write(count,2,"Check result",style)
				else:
					sheet1.write(count,0,i)

	workbook.save("overlay.xls")

if __name__=="__main__":
	write_excel()
