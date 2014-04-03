#! /usr/bin/python
########################################################################
# SpeakThis speaks the currently highlighted text using espeak.
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
	# figure out the file path
	filepath = fileName.split(os.sep)
	filepath.pop()
	filepath = os.sep.join(filepath)
	# check if path exists
	if os.path.exists(filepath):
		try:
			fileObject = open(fileName,'w')
			fileObject.write(contentToWrite)
			fileObject.close()
			print 'Wrote file:',fileName
		except:
			print 'Failed to write file:',fileName
			return False
	else:
		print 'Failed to write file, path:',filepath,'does not exist!'
		return False
########################################################################
def speakText():
	system('killall espeak')
	# grab text with xsel and pipe to espeak
	system('espeak "'+popen('xsel').read().replace('"','').replace("'","").replace('$','')+'"')
########################################################################
def setupShortcuts():
	newSettingsArray = []
	# in this array the 0th value is searched for and if found the 1th 
	# value is used to replace the current line in the file
	newSettingsArray.append(['<property name="&lt;Super&gt;s" type="string" value="speakthis"/>',''])
	newSettingsArray.append(['      <property name="&lt;Alt&gt;F1" type="string" value="xfce4-popup-applicationsmenu"/>','      <property name="&lt;Alt&gt;F1" type="string" value="xfce4-popup-applicationsmenu"/>\n      <property name="&lt;Super&gt;s" type="string" value="speakthis"/>'])
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
			writeFile(filePath,newConfig.replace('\n\n','\n'))
			# make user the owner of this file once more since root is editing the files
			os.system(('chown '+folder+' '+filePath))
	print 'The system has successfully been configured for all users to'
	print 'speak the highlighted text when you press "<super>+s", you'
	print 'must log out and back in before the program can be used!'
########################################################################
def setupShortcut():
	newSettingsArray = []
	# in this array the 0th value is searched for and if found the 1th 
	# value is used to replace the current line in the file
	newSettingsArray.append(['      <property name="&lt;Super&gt;s" type="string" value="speakthis"/>',''])
	newSettingsArray.append(['      <property name="&lt;Alt&gt;F1" type="string" value="xfce4-popup-applicationsmenu"/>','      <property name="&lt;Alt&gt;F1" type="string" value="xfce4-popup-applicationsmenu"/>\n      <property name="&lt;Super&gt;s" type="string" value="speakthis"/>'])
	# store the filepath to the config file in the user running the programs
	# home directory
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
					print 'Wrote line', item[1] #DEBUG
					foundString = True
			if foundString == False:
				newConfig += line+'\n'
				print 'Wrote line', line #DEBUG
		writeFile(filePath,newConfig.replace('\n\n','\n'))
	print 'The system has successfully been configured to speak the'
	print 'highlighted text when you press "<super>+s", you must log out'
	print 'and back in before the program can be used.'
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
	print "SpeakThis speaks the currently highlighted text using espeak."
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
	print "    Installs shortcuts for xfce <super>+s to run the program"
	print "-S or --setup-shortcuts"
	print "    Installs shortcuts for xfce <super>+s to all users on the system"
	print "Running the program without arguments will speak the currently"
	print "    highlighted text."
	print '#############################################################'
	print 'Highlight some of the above text and hit "<super>+s" to test'
	print 'the program.'
else:
	# by default run calcText on program launch with no arguments
	speakText();
