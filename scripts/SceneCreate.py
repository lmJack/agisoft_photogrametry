'''
Script Batch Processes Maya Preview Images . 

requires C:\Program Files\Autodesk\Maya2014\bin\mayapy.exe as python executable 

'''
import maya.standalone
maya.standalone.initialize("Python")

import maya.cmds as cmds
cmds.loadPlugin("Mayatomr")

import os
import getpass
import sys
import subprocess

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class MayaScene():

	def find(self):
		# Find Path
		with open ('Path.txt','rb') as myfile:
			print (myfile)
			self.assetspath = myfile.read().rstrip()
			myfile.close
				
		# User Name
		self.username = getpass.getuser()

		# Maya 
		self.path = 'C:\\Program Files\\Autodesk\\Maya2014\\bin'

	def create(self):
		
		print ("asset path: ", self.assetspath)

		blankdocument = self.assetspath+'/MayaProject.ma'
		
		print ("Document path: ", blankdocument)

		# Open your file
		self.render_file = cmds.file(blankdocument, o=True)

		cmds.file(new=True,f=True)
		cmds.file(rn=blankdocument)
		
		# Open Shot List
		views = []
		newviews = []		

		# Placeholder Object
		cmds.polyCube(n='placeholder')
		cmds.group('placeholder',n='ProductGroup')
		cmds.move(0,1,0)
		cmds.select('placeholder')
		cmds.CenterPivot('placeholder')

		# Import OBJ from Agisoft
		ModelPath = self.assetspath+'/output/model.obj'
		cmds.file(ModelPath, i=True)
		cmds.select('Mesh')
		cmds.CenterPivot('Mesh')
		cmds.select('Mesh','placeholder')
		cmds.align(x='mid',y='mid',z='mid',alignToLead=True)
		cmds.group('Mesh',p='ProductGroup')

		# Delete Placeholder
		cmds.delete('placeholder')
		
		# Key Model Positions
		with open(self.assetspath+'/shotListConfig.txt') as inf:
			  		
			# Identify all elements in view column		
			for line in inf:
				parts = line.split() 
				if len(parts) > 1:   
					s = parts[3]
					views.append(s)
					
			# replace tqt elements with angle 
			for idx, item in enumerate(views):
				if item == 'tqt':
					views[idx] = '0_45_0'
					print (views)  			
					
			# Remove the header line		
			views.pop(0)
			
			# Replace _ with , for each element
			angles = ([view.replace('_', ',') for view in views])
			
			# Remove Duplicates
			for i in angles:
				if i not in newviews:
					newviews.append(i)
							
			# Define Frames
			frame = 0
			view = []
			
			# Assign X, Y & Z values from the first 3 elements 
			for view in newviews:
				viewsplit = view.split(",")
				x = viewsplit[0]
				y = viewsplit[1]
				z = viewsplit[2]
				
				# Move frame forward one
				frame += 1
				# Print New Frame
				print (frame)
				
				# Set Key Frame with new X,Y & Z values on new time frame
				cmds.rotate( x, y, z, 'ProductGroup' )
				cmds.setKeyframe('ProductGroup',time=frame)
				
				# Print X,Y & Z Values
				print ("x= " + x)
				print ("y= " + y)
				print ("z= " + z)		

		# Create Lights
		cmds.directionalLight(n='key',intensity=.2,rs=True)
		cmds.rotate(-45,-45,0)
		cmds.scale(10,10,10)
		cmds.setAttr("keyShape.lightAngle",5)
		cmds.setAttr("keyShape.shadowRays",15)

		# Create Camera 
		cam = cmds.camera(n='maincamera',ff='vertical')
		cmds.move(0,1,12)
		width = 512
		height = 512
		cmds.setAttr( 'defaultResolution.deviceAspectRatio', ( ( width ) / ( height ) ) )
		cmds.setAttr('maincameraShape2.backgroundColor',1,1,1)
		cmds.setAttr('maincameraShape2.focalLength', 85)

		# Group Scene
		cmds.group('maincamera1','key', n='Scene')

		# Group ALL
		cmds.group('Scene','ProductGroup',n='ALL')

		# Save File
		cmds.file(rename=self.render_file)
		cmds.file( save=True, type='mayaAscii' )

	def render(self):

		# Render Project. Use MEL instead of python for these;
		render_project = self.assetspath+'/QA_PNG'
		renderer_folder = self.path.split(sys.executable)[0]
		renderer_exec_name = "Render"
		params = [renderer_exec_name]
		params += ['-fnc','name_#.ext']
		params += ['-s','1']
		params += ['-e','16']
		params += ['-of', 'jpg']
		params += ['-cam', 'maincamera1']
		params += ['-alpha', '0']
		params += ['-y','512']
		params += ['-x','512']
		params += ['-proj', render_project]
		params += ['-r', 'mr']
		params += [self.render_file]
		p = subprocess.Popen(params, cwd=renderer_folder)
		stdout, stderr = p.communicate()

	def email(self):

		# Find Images
		ImageDirectory = self.assetspath+'/QA_PNG/'
		print("Image Directory: ",ImageDirectory)
		ImageFiles = []

		for photo in os.listdir (ImageDirectory):
			if photo.endswith('.jpg'):
				FullImage = ImageDirectory + photo
				ImageFiles.append(FullImage)

		# Email Images
		strFrom = '<youremailaddress>'
		strTo = '<youremailaddress>'
		print("email sent to: ",strTo)

		msgRoot = MIMEMultipart('related')
		msgRoot['Subject'] = 'MODEL COMPLETE'
		msgRoot['From'] = strFrom
		msgRoot['To'] = strTo

		msgAlternative = MIMEMultipart('alternative')
		msgRoot.attach(msgAlternative)

		# Define Images to attach
		c = 0
		for image in ImageFiles:

			# get CID name for each image
			c += 1
			newC = str(c)
			new = "<image%s>" %newC

			# attach the image
			i = open(image,'rb')
			img = MIMEImage(i.read())
			i.close()
			msgRoot.attach(img)
			img.add_header('Content-ID',new)

		# Plain text message
		msgText = MIMEText('Model Complete')
		msgAlternative.attach(msgText)

		# Message to send with image in HTML
		msgText = MIMEText('<b>Model Complete:<b><br><img src="cid:image1"><br><img src="cid:image2"><br><img src="cid:image3"><br><img src="cid:image4"><br><img src="cid:image5"><br><img src="cid:image6"><br><img src="cid:image7"><br><img src="cid:image8"><br><img src="cid:image9"><br><img src="cid:image10"><br><img src="cid:image11"><br><img src="cid:image12"><br><img src="cid:image13"><br><img src="cid:image14"><br><img src="cid:image15"><br><img src="cid:image16"><br>', 'html')
		msgAlternative.attach(msgText)

		# Send
		import smtplib
		smtp = smtplib.SMTP()
		smtp.connect('<yourmailserver>')
		smtp.sendmail(strFrom, strTo, msgRoot.as_string())
		smtp.quit()
		print ('Email Sent')


r = MayaScene()
r.find()
r.create()
r.render()
r.email()