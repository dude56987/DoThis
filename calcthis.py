#! /usr/bin/python
########################################################################
# Launcher calculate currently highlighted text, for use with hotkeys
# Copyright (C) 2013  Carl J Smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
from os import popen
from os import system
import sys
import os
########################################################################
def loadFile(fileName):
	try:
		print "Loading :",fileName
		fileObject=open(fileName,'r');
	except:
		print "Failed to load :",fileName
		return False
	fileText=''
	lineCount = 0
	for line in fileObject:
		fileText += line
		sys.stdout.write('Loading line '+str(lineCount)+'...\r')
		lineCount += 1
	print "Finished Loading :",fileName
	fileObject.close()
	if fileText == None:
		return False
	else:
		return fileText
	#if somehow everything fails return false
	return False
########################################################################
def writeFile(fileName,contentToWrite):
	try:
		fileObject = open(fileName,'w')
		fileObject.write(contentToWrite)
		fileObject.close()
	except:
		return False
########################################################################
def calcText():
	# grab highlighted section
	inputVar = popen('xsel').read()
	# run grabed section through genius to get anwser
	output = popen('genius --exec="'+inputVar+'"').read()
	# print out problem and anwser with zenity using a popup
	system("zenity --info --icon-name='calc' --text='"+inputVar+' = '+output+"'")
########################################################################
def setupShortcuts():
	newSettingsArray = []
	# in this array the 0th value is searched for and if found the 1th 
	# value is used to replace the current line in the file
	newSettingsArray.append(['<property name="&lt;Super&gt;c" type="string" value="calcthis"/>',''])
	newSettingsArray.append(['      <property name="&lt;Alt&gt;F1" type="string" value="xfce4-popup-applicationsmenu"/>','      <property name="&lt;Alt&gt;F1" type="string" value="xfce4-popup-applicationsmenu"/>\n      <property name="&lt;Super&gt;c" type="string" value="calcthis"/>'])
	# sets up shortcuts for all users on the system
	for folder in os.listdir('/home'):
		filePath = os.path.join('/home',folder,'.config','xfce4','xfconf','xfce-perchannel-xml','xfce4-keyboard-shortcuts.xml')
		if os.path.exists(filePath):
			# split the config file by lines into an array to loop though
			tempConfig=loadFile(filePath).split('\n')
			newConfig = '' # stores the new file as a string
			for line in tempConfig:
				foundString = False # this is used to prevent double line writes
				for item in newSettingsArray:
					if line.find(item[0]) != -1:
						# write new setting and remove old one
						newConfig += item[1]+'\n'
						foundString = True
				if foundString == False:
					newConfig += line+'\n'
			# after editing file write the new version of the file
			writeFile(filePath,newConfig.replace('\n\n','\n'))
			# make user the owner of this file once more since root is editing the files
			os.system(('chown '+folder+' '+filePath))
	print 'All users on the system now have it setup so that when you press'
	print '"<super>+c" the program will calculate the highlighted text and '
	print 'popup a window showing the anwser! You must logout and back in'
	print 'before the program is enabled.'
########################################################################
def setupShortcut():
	newSettingsArray = []
	# in this array the 0th value is searched for and if found the 1th 
	# value is used to replace the current line in the file
	newSettingsArray.append(['<property name="&lt;Super&gt;c" type="string" value="calcthis"/>',''])
	newSettingsArray.append(['<property name="&lt;Alt&gt;F2" type="string" value="xfrun4"/>','      <property name="&lt;Alt&gt;F2" type="string" value="xfrun4"/>\n      <property name="&lt;Super&gt;c" type="string" value="calcthis"/>'])
	# sets up shortcut for current user
	filePath = os.path.join(os.getenv('HOME'),'.config','xfce4','xfconf','xfce-perchannel-xml','xfce4-keyboard-shortcuts.xml')
	if os.path.exists(filePath):
		# split the config file by lines into an array to loop though
		tempConfig=loadFile(filePath).split('\n')
		newConfig = '' # stores the new file as a string
		for line in tempConfig:
			foundString = False # this is used to prevent double line writes
			for item in newSettingsArray:
				if line.find(item[0]) != -1:
					# write new setting and remove old one
					newConfig += item[1]+'\n'
					foundString = True
			if foundString == False:
				newConfig += line+'\n'
		# after editing file write the new version of the file
		writeFile(filePath,newConfig.replace('\n\n','\n'))
		print 'The system has successfully been configured to calculate equations'
		print 'when you press "<super>+c", popup a window showing the anwser!'
		print 'You must logout and back in before the program is enabled.'
########################################################################
if (('-S' in sys.argv)==True) or (('--setup-shortcuts' in sys.argv)==True):
	#check for root since shortcuts need to be installed for all users
	if os.geteuid() != 0:
		print 'ERROR: this argument must be ran as root!'
		print 'This parameter will install shortcuts for all users!'
		exit()
	else:
		# setup shortcuts for everyone on the system
		setupShortcuts();
elif (('-s' in sys.argv)==True) or (('--setup-shortcut' in sys.argv)==True):
	setupShortcut()
elif (('-h' in sys.argv)==True) or (('--help' in sys.argv)==True):
	print "CalcThis calculates currently highlighted text and pops a anwser up"
	print "Copyright (C) 2013  Carl J Smith"
	print ""
	print "This program is free software: you can redistribute it and/or modify"
	print "it under the terms of the GNU General Public License as published by"
	print "the Free Software Foundation, either version 3 of the License, or"
	print "(at your option) any later version."
	print ""
	print "This program is distributed in the hope that it will be useful,"
	print "but WITHOUT ANY WARRANTY; without even the implied warranty of"
	print "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
	print "GNU General Public License for more details."
	print ""
	print "You should have received a copy of the GNU General Public License"
	print "along with this program.  If not, see <http://www.gnu.org/licenses/>."
	print "#############################################################"
	print "-h or --help"
	print "    Displays this menu"
	print "-s or --setup-shortcut"
	print "    Installs shortcuts for xfce <super>+c to run the program"
	print "-S or --setup-shortcuts"
	print "    Installs shortcuts for xfce <super>+c to all users on the system"
	print "Running the program without arguments will calculate the highlighted"
	print "    problem and popup the anwser in a zenity info window."
	print '#############################################################'
	print 'Below are some sample equations to test out the program.'
	print '                        2+2'
	print '                        log(128)'
	print '                        2^3'
	print '                        (log(2^3)*100)+2'
	print '                        log(-1)'
	print '                        sqrt(-1)'
else:
	# by default run calcText on program launch with no arguments
	calcText();
