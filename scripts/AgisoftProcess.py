import PhotoScan
import os
import sys

from PySide.QtGui import QPixmap, QApplication
import time

import getpass
import subprocess

from datetime import datetime
startTime = datetime.now()


# Get User
username = getpass.getuser()

def Scan():	

	# Define: Home Directory
	path = os.getcwd()
	print ("Home Directory: ", path)

	ImageDirectory = path
	os.chdir(ImageDirectory)
	print ("Image Directory: ", ImageDirectory)
	
	# Set Application Objects
	doc = PhotoScan.app.document
	print ("Processing Images...")

	# Define Chunk
	chunk = PhotoScan.app.document.addChunk()
	chunk.label = "MainChunk"

	# Find Images
	ImageFiles = []
	for photo in os.listdir (ImageDirectory):
		if photo.endswith('.tif'):
			ImageFiles.append(photo)
			
	if len(ImageFiles)>0:
		print(ImageFiles)
	if len(ImageFiles)==0:
		print('no images found!')
		
	print ("Script Location: C:\Program Files\Agisoft\PhotoScan Pro\scripts")

	# Load Image Files into Chunk Camera
	chunk.addPhotos(ImageFiles)
	chunk.importMasks(path='',method='alpha')
	camera = chunk.cameras[0]

	# match Photos
	chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy,preselection=PhotoScan.GenericPreselection, filter_mask=True)

	# align Photos
	chunk.alignCameras()

	# Build Dense Cloud
	chunk.buildDenseCloud(quality=PhotoScan.HighQuality)

	#Build Model
	chunk.buildModel(surface=PhotoScan.Arbitrary,interpolation=PhotoScan.EnabledInterpolation,face_count=2000000)
	
	# Build UVs
	chunk.buildUV(mapping=PhotoScan.GenericMapping)
	
	# Build Texture
	chunk.buildTexture(blending=PhotoScan.MosaicBlending, size=4096)	

	# Decimate Model
	chunk.decimateModel(2000000)	

	modelname = path+"\\output\\model.obj"
	
	#Export Model & Save Doc
	chunk.exportModel(modelname,texture_format="jpg", texture=True,format="obj")

	time.sleep(5)
	doc.save("AgisoftProject.psz")
	print('time to finish: ',datetime.now()-startTime)
	time.sleep(5)
	sys.exit()
	quit()

	return 1
	
label = "scan/Run"
PhotoScan.app.addMenuItem(label, Scan, "r")

print("scan Menu Added")
print ("press r to run")
