#!/usr/bin/env python

'''

Script to Set up Agisoft Project and Execute Image Processing. See top level README.

'''
import sys
import subprocess
from shutil import copyfile
import os
import getpass

# Hot keys
import time
import win32com
from win32com import client

# First Select Directory
class Start():
	def __init__(self, parent=None):
		# Find the Project Path
		with open ('Path.txt','r',encoding='utf8') as myfile:
			self.assetspath = myfile.read().rstrip()
			myfile.close
			
		Config = os.getcwd()
		self.ConfigPath = (os.path.abspath(os.path.join(Config, os.pardir)))
		print ('Config Path: ',self.ConfigPath)

	def setCopy(self):
		
		print ('Set Up Project...')
		print ('\n')

		# activate hotkeys
		wsh = win32com.client.Dispatch("WScript.Shell")

		# New Project
		ProjectDirectory = str(self.assetspath)
		print ('Assets Path: ', ProjectDirectory)
		print ('\n')

		# Define Project Name 
		AgisoftProjectName = "\\AgisoftProject.psz"
		MayaProjectName = "\\MayaProject.ma"

		# Define full project path
		AgisoftProjectPath = (ProjectDirectory + AgisoftProjectName)

		MayaProjectPath = (ProjectDirectory + MayaProjectName)
		
		# Make Processing Script
		processfile = 'C:\\Program Files\\Agisoft\\PhotoScan Pro\\scripts\\AgisoftProcess.py'

		# Make output directory
		output = (ProjectDirectory+"\\output")
		if not os.path.exists(output): os.makedirs(output)

		# Start Up Configuration Directory DO NOT TOUCH
		print ('Copy Agisoft Config File: ',self.ConfigPath+'\\documents'+ AgisoftProjectName)
		print ('Copied Agisoft Config to: ', AgisoftProjectPath)
		copyfile(self.ConfigPath+'\\documents'+ AgisoftProjectName,AgisoftProjectPath)
		print ('\n')
		
		print ('Copy Maya File: ',self.ConfigPath+'\\documents'+ MayaProjectName)
		print ('Copied Maya to: ', MayaProjectPath)		
		copyfile(self.ConfigPath+'\\documents'+ MayaProjectName,MayaProjectPath)
		print ('\n')
		
		print ('Copy Agisoft Process Script: ', self.ConfigPath+'\\scripts\\AgisoftProcess.py')
		print ('Copied Agisoft Process Script to: ', processfile)
		copyfile(self.ConfigPath+'\\scripts\\AgisoftProcess.py',processfile)
		print ('\n')

		# Open New File
		os.chdir (ProjectDirectory)
		wsh.Run(AgisoftProjectPath)

		# Press Hot Key
		time.sleep(5)
		wsh.AppActivate("photoscan")
		print ("r pressed")
		wsh.SendKeys("r")


r = Start()
r.setCopy()