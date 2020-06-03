#!/usr/bin/python
#选择排序

a=[1,2,3,9,8,7,4,5,6]
b=[]

for indexj,j in enumerate(range(len(a))):
	big=a[0]
	print(a)
	for indexi,i in enumerate(a):
		if indexi>len(a)-2:
			break

		if big >a[indexi+1]:
			pass
		else:
			big=a[indexi+1]
	b.append(big)
	a.remove(big)
print(b)
