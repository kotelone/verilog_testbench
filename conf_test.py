#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os

args = sys.argv

filename, modulename, instance = args[1], args[2], args[3]

f = open(filename, 'r');
fileData = f.read()

oneComment = False
moreComment = False
listOfComments = []
widthSpace = False

fileLiters = list(fileData)

l = 0
for liter in fileLiters:
	
	if liter == '/' and fileLiters[l+1] == '/' and (not oneComment) and (not moreComment):
		oneComment = True

	if liter == '/' and fileLiters[l+1] == '*' and (not oneComment) and (not moreComment):
		moreComment = True

	if oneComment:
		if liter == '\n':
			oneComment = False

		listOfComments.append(l)	

	if moreComment:
		if liter == '*' and fileLiters[l+1] == '/':
			moreComment = False

		listOfComments.append(l)	


	if liter == '[':
		widthSpace = True

	if widthSpace and liter == ']':
		widthSpace = False	

	if widthSpace:
		if liter == ' ':
			listOfComments.append(l)
				

	l += 1

for i in reversed(listOfComments):
	del fileLiters[i]

fileData = ''.join(fileLiters)
fileData = fileData.replace('\n', ' ')
fileData = fileData.replace('\t', ' ')
fileWords = fileData.split(' ')

for i in range(fileWords.count('')):
	fileWords.remove('')



# Main parser

listOfModuleInputs = []

module_det = False
moduleInputs_det = False

connection_det = False

connection_dir = ['input','output','inout']
connection_type = ['reg','wire','']

listOfConnections = []

class Connection():
	cType = ""
	cDir  = ""
	cWidth = ""
	cName = ""
	pass
	
		

i = 0

for word in fileWords:


	if word == 'module' and fileWords[i+1] == modulename:
		module_det = True

	if word == 'endmodule':
		module_det = False
			
	if module_det:

		if word == '(' and fileWords[i-1] != '#':
			moduleInputs_det = True
			continue	

		if moduleInputs_det:

			if word == ')' or word == ');':
				moduleInputs_det = False
				continue

			listOfModuleInputs.append(word)


		if moduleInputs_det:

			if word in connection_dir:
				connection_det = True
				new = Connection()
				listOfConnections.append(new)
				new.cDir = word
				continue			

			if connection_det:
		
				if word in connection_type:
					new.cType = word

				elif word[0] == '[':
					new.cWidth = word

				else:
					new.cName = word.replace(',', '')
					connection_det = False


	i += 1 

ports = ""
i = 0
lengthOfList = len(listOfConnections) - 1
for c in listOfConnections:

	testbType = 'wire'
	if c.cDir == 'input':
		testbType = 'reg'

	print("{}\t{}\t{}_{};".format(testbType, c.cWidth, instance, c.cName))

	if i == 0:
		ports = ports + ".{}\t\t({}_{}),\n".format(c.cName,instance, c.cName)
	elif i == lengthOfList:
		ports = ports + "\t.{}\t\t({}_{})\n".format(c.cName,instance, c.cName)
	else:
		ports = ports + "\t.{}\t\t({}_{}),\n".format(c.cName,instance, c.cName)		

	i += 1

print()
print("{} {} ({});".format(modulename, instance, ports))

