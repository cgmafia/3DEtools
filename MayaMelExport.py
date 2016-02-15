"""
3DEqualizer maya mel script exporter
3DE4r5 extended

github/danielforgacs
"""
#
#
# 3DE4.script.name:	mel export...
#
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:	Main Window::ford
#
# 3DE4.script.comment:	Creates a MEL script file that contains all project data, which can be imported into Autodesk Maya.
#
#

#
# import sdv's python vector lib...

import os
import socket
import tde4
from vl_sdv import *
from TDE4Wrapper import TDE4Wrapper


class MayaConnectWrapper(object):
	def __enter__(self):
		self.maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.maya.connect(('localhost', 6005))
		except:
			print('--> Maya is not running. Can\'t open exported mel')

		return self.maya

	def __exit__(self, type, value, traceback):
		self.maya.close()


def get_mel_filename():
	projectpath = os.path.abspath(tde4.getProjectPath())
	folder = os.path.dirname(projectpath)
	projectname = os.path.basename(projectpath)
	mel_name = projectname.replace('3de', 'mel')
	path = os.path.join(folder, 'exports', mel_name)

	if not os.path.exists(os.path.join(folder, 'exports')):
		os.mkdir(os.path.join(folder, 'exports'))

	# print('path: {0}'.format(path))

	return {'path': path, 'filename': projectname}


def get_frame_range():
	project = TDE4Wrapper()
	fstart, fend, step = project.frange

	return {'first': fstart, 'last': fend}


def get_cam_parms():
	project = TDE4Wrapper()
	focal = tde4.getCameraFocalLength(project.cam_id, 1)
	resx = tde4.getCameraImageWidth(project.cam_id)
	resy = tde4.getCameraImageHeight(project.cam_id)

	return {'focal': focal, 'id': project.cam_id, 'resx': resx, 'resy': resy}


def get_filmback():
	cam_id = tde4.getCurrentCamera()
	lens_id = tde4.getCameraLens(cam_id)
	filmback_w = tde4.getLensFBackWidth(lens_id)
	filmback_h = tde4.getLensFBackHeight(lens_id)

	return {'w': filmback_w, 'h': filmback_h}



def add_pipeline_attribs():
	mel = """
// add pipeline attribs
addAttr -longName "source" -dataType "string" $cameraShape;
addAttr -longName "footage" -dataType "string" $cameraShape;
addAttr -longName "res_x" -attributeType "short" $cameraShape;
addAttr -longName "res_y" -attributeType "short" $cameraShape;
addAttr -longName "focal" -attributeType "float" $cameraShape;
addAttr -longName "filmback_w" -attributeType "float" $cameraShape;
addAttr -longName "filmback_h" -attributeType "float" $cameraShape;
addAttr -longName "fstart" -attributeType short $cameraShape;
addAttr -longName "fend" -attributeType short $cameraShape;

setAttr ($cameraShape + ".source") -type "string" "{source}";
setAttr ($cameraShape + ".footage") -type "string" "{footage}";
setAttr ($cameraShape + ".res_x") {res_x};
setAttr ($cameraShape + ".res_y") {res_y};
setAttr ($cameraShape + ".focal") {focal};
setAttr ($cameraShape + ".filmback_w") {filmback_w};
setAttr ($cameraShape + ".filmback_h") {filmback_h};
setAttr ($cameraShape + ".fstart") {fstart};
setAttr ($cameraShape + ".fend") {fend};

setAttr -lock on ($cameraShape + ".source");
setAttr -lock on ($cameraShape + ".footage");
setAttr -lock on ($cameraShape + ".res_x");
setAttr -lock on ($cameraShape + ".res_y");
setAttr -lock on ($cameraShape + ".fstart");
setAttr -lock on ($cameraShape + ".fend");
setAttr -lock on ($cameraShape + ".focal");
setAttr -lock on ($cameraShape + ".filmback_w");
setAttr -lock on ($cameraShape + ".filmback_h");

setAttr -lock on ($cameraShape + ".focalLength");
setAttr -lock on ($cameraShape + ".horizontalFilmAperture");
setAttr -lock on ($cameraShape + ".verticalFilmAperture");

setAttr -lock on ($cameraTransform + ".translateX");
setAttr -lock on ($cameraTransform + ".translateY");
setAttr -lock on ($cameraTransform + ".translateZ");
setAttr -lock on ($cameraTransform + ".rotateX");
setAttr -lock on ($cameraTransform + ".rotateY");
setAttr -lock on ($cameraTransform + ".rotateZ");
setAttr -lock on ($cameraTransform + ".scaleX");
setAttr -lock on ($cameraTransform + ".scaleY");
setAttr -lock on ($cameraTransform + ".scaleZ");
"""

	mel = mel.format(source=tde4.getProjectPath(),
					footage=tde4.getCameraPath(get_cam_parms()['id']),
					res_x=get_cam_parms()['resx'],
					res_y=get_cam_parms()['resy'],
					focal=get_cam_parms()['focal'],
					filmback_w=get_filmback()['w'],
					filmback_h=get_filmback()['h'],
					fstart=get_frame_range()['first'],
					fend=get_frame_range()['last'],
				)

	return mel


def convertToAngles(r3d):
	rot	= rot3d(mat3d(r3d)).angles(VL_APPLY_ZXY)
	rx	= (rot[0]*180.0)/3.141592654
	ry	= (rot[1]*180.0)/3.141592654
	rz	= (rot[2]*180.0)/3.141592654
	return(rx,ry,rz)


def convertZup(p3d,yup):
	if yup==1:
		return(p3d)
	else:
		return([p3d[0],-p3d[2],p3d[1]])


def angleMod360(d0,d):
	dd	= d-d0
	if dd>180.0:
		d	= angleMod360(d0,d-360.0)
	else:
		if dd<-180.0:
			d	= angleMod360(d0,d+360.0)
	return d


def validName(name):
	name	= name.replace(" ","_")
	name	= name.replace("\n","")
	name	= name.replace("\r","")
	return name

def prepareImagePath(path,startframe):
	path	= path.replace("\\","/")
	i	= 0
	n	= 0
	i0	= -1
	while(i<len(path)):
		if path[i]=='#': n += 1
		if n==1: i0 = i
		i	+= 1
	if i0!=-1:
		fstring		= "%%s%%0%dd%%s"%(n)
		path2		= fstring%(path[0:i0],startframe,path[i0+n:len(path)])
		path		= path2
	return path


#
# main script...


#
# search for camera point group...
def main():
	campg	= None
	pgl	= tde4.getPGroupList()
	for pg in pgl:
		if tde4.getPGroupType(pg)=="CAMERA": campg = pg
	if campg==None:
		tde4.postQuestionRequester("Export Maya...","Error, there is no camera point group.","Ok")


	#
	# open requester...

	try:
		req	= _export_requester_maya
	except (ValueError,NameError,TypeError):
		_export_requester_maya	= tde4.createCustomRequester()
		req			= _export_requester_maya
		tde4.addFileWidget(req,"file_browser","Exportfile...","*.mel")
		tde4.addTextFieldWidget(req, "startframe_field", "Startframe", "1")
		# tde4.addOptionMenuWidget(req,"mode_menu","Orientation","Y-Up", "Z-Up")
		tde4.addToggleWidget(req,"hide_ref_frames","Hide Reference Frames",0)

	cam	= tde4.getCurrentCamera()
	offset	= tde4.getCameraFrameOffset(cam)
	tde4.setWidgetValue(req,"startframe_field",str(offset))

	# ret	= tde4.postCustomRequester(req,"Export Maya (MEL-Script)...",600,0,"Ok","Cancel")
	ret	= 1

	if ret==1:
		# yup	= tde4.getWidgetValue(req,"mode_menu")
		# if yup==2: yup = 0
		yup	= 1
		# path	= tde4.getWidgetValue(req,"file_browser")
		path = get_mel_filename()['path']
		# frame0	= float(tde4.getWidgetValue(req,"startframe_field"))
		# frame0	-= 1
		framerange = get_frame_range()
		playbackoptions = 'playbackOptions -min {0} -max {1};'
		playbackoptions = playbackoptions.format(framerange['first'], framerange['last'])
		frame0 = framerange['first'] - 1

		hide_ref= tde4.getWidgetValue(req,"hide_ref_frames")
		if path!=None:
			if not path.endswith('.mel'): path = path+'.mel'
			f	= open(path,"w")
			if not f.closed:

				#
				# write some comments...

				f.write("//\n")
				f.write("// Maya/MEL export data written by %s\n"%tde4.get3DEVersion())
				f.write("//\n")
				f.write("// All lengths are in centimeter, all angles are in degree.\n")
				f.write("//\n\n")

				#
				# write scene group...
				groupname = """// create scene group...
string $sceneGroupName = `group -em -name "mm_{name}"`;
"""

				# f.write("// create scene group...\n")
				# f.write("string $sceneGroupName = `group -em -name \"Scene\"`;\n")
				groupname = groupname.format(name=get_mel_filename()['filename'][:-4])
				f.write(groupname)

				#
				# write cameras...

				cl	= tde4.getCameraList()
				index	= 1
				for cam in cl:
					camType		= tde4.getCameraType(cam)
					noframes	= tde4.getCameraNoFrames(cam)
					lens		= tde4.getCameraLens(cam)
					if lens!=None:
						name		= validName(tde4.getCameraName(cam))
						cam_name = 'cam_mm_' + name
						# name		= "%s_%s_1"%(name,index)
						# name		= "%s_%s"%(name,index)
						name = cam_name
						index		+= 1
						fback_w		= tde4.getLensFBackWidth(lens)
						fback_h		= tde4.getLensFBackHeight(lens)
						p_aspect	= tde4.getLensPixelAspect(lens)
						focal		= tde4.getCameraFocalLength(cam,1)
						lco_x		= tde4.getLensLensCenterX(lens)
						lco_y		= tde4.getLensLensCenterY(lens)

						# convert filmback to inch...
						fback_w		= fback_w/2.54
						fback_h		= fback_h/2.54
						lco_x		= -lco_x/2.54
						lco_y		= -lco_y/2.54

						# convert focal length to mm...
						focal		= focal*10.0

						# create camera...
						f.write("\n")
						f.write("// create camera %s...\n"%name)
						f.write("string $cameraNodes[] = `camera -name \"%s\" -hfa %.15f  -vfa %.15f -fl %.15f -ncp 0.01 -fcp 10000 -shutterAngle 180 -ff \"overscan\"`;\n"%(name,fback_w,fback_h,focal))
						f.write("string $cameraTransform = $cameraNodes[0];\n")
						f.write("string $cameraShape = $cameraNodes[1];\n")
						f.write("xform -zeroTransformPivots -rotateOrder zxy $cameraTransform;\n")
						f.write("setAttr ($cameraShape+\".horizontalFilmOffset\") %.15f;\n"%lco_x);
						f.write("setAttr ($cameraShape+\".verticalFilmOffset\") %.15f;\n"%lco_y);
						p3d	= tde4.getPGroupPosition3D(campg,cam,1)
						p3d	= convertZup(p3d,yup)
						f.write("xform -translation %.15f %.15f %.15f $cameraTransform;\n"%(p3d[0],p3d[1],p3d[2]))
						r3d	= tde4.getPGroupRotation3D(campg,cam,1)
						rot	= convertToAngles(r3d)
						f.write("xform -rotation %.15f %.15f %.15f $cameraTransform;\n"%rot)
						f.write("xform -scale 1 1 1 $cameraTransform;\n")

						"""add pipeline attributes to camerashape"""
						attribs = add_pipeline_attribs()
						f.write(attribs)

						# image plane...
						f.write("\n\n// create image plane...\n")
						f.write("string $imagePlane = `createNode imagePlane`;\n")
						f.write("cameraImagePlaneUpdate ($cameraShape, $imagePlane);\n")
						f.write("setAttr ($imagePlane + \".offsetX\") %.15f;\n"%lco_x)
						f.write("setAttr ($imagePlane + \".offsetY\") %.15f;\n"%lco_y)

						if camType=="SEQUENCE": f.write("setAttr ($imagePlane+\".useFrameExtension\") 1;\n")
						else:			f.write("setAttr ($imagePlane+\".useFrameExtension\") 0;\n")

						f.write("expression -n \"frame_ext_expression\" -s ($imagePlane+\".frameExtension=frame\");\n")
						path	= tde4.getCameraPath(cam)
						sattr	= tde4.getCameraSequenceAttr(cam)
						path	= prepareImagePath(path,sattr[0])
						f.write("setAttr ($imagePlane + \".imageName\") -type \"string\" \"%s\";\n"%(path))
						f.write("setAttr ($imagePlane + \".fit\") 4;\n")
						f.write("setAttr ($imagePlane + \".displayOnlyIfCurrent\") 1;\n")
						f.write("setAttr ($imagePlane  + \".depth\") (9000/2);\n")

						# parent camera to scene group...
						f.write("\n")
						f.write("// parent camera to scene group...\n")
						f.write("parent $cameraTransform $sceneGroupName;\n")

						if camType=="REF_FRAME" and hide_ref:
							f.write("setAttr ($cameraTransform +\".visibility\") 0;\n")

						# animate camera...
						if camType!="REF_FRAME":
							f.write("\n")
							f.write("// animating camera %s...\n"%name)
							f.write(playbackoptions)
							# f.write("playbackOptions -min %d -max %d;\n"%(1+frame0,noframes+frame0))
							f.write("\n\n")

						frame	= 1
						while frame<=noframes:
							# rot/pos...
							p3d	= tde4.getPGroupPosition3D(campg,cam,frame)
							p3d	= convertZup(p3d,yup)
							r3d	= tde4.getPGroupRotation3D(campg,cam,frame)
							rot	= convertToAngles(r3d)
							if frame>1:
								rot	= [ angleMod360(rot0[0],rot[0]), angleMod360(rot0[1],rot[1]), angleMod360(rot0[2],rot[2]) ]
							rot0	= rot
							f.write("setKeyframe -at translateX -t %d -v %.15f $cameraTransform; "%(frame+frame0,p3d[0]))
							f.write("setKeyframe -at translateY -t %d -v %.15f $cameraTransform; "%(frame+frame0,p3d[1]))
							f.write("setKeyframe -at translateZ -t %d -v %.15f $cameraTransform; "%(frame+frame0,p3d[2]))
							f.write("setKeyframe -at rotateX -t %d -v %.15f $cameraTransform; "%(frame+frame0,rot[0]))
							f.write("setKeyframe -at rotateY -t %d -v %.15f $cameraTransform; "%(frame+frame0,rot[1]))
							f.write("setKeyframe -at rotateZ -t %d -v %.15f $cameraTransform; "%(frame+frame0,rot[2]))

							# focal length...
							focal	= tde4.getCameraFocalLength(cam,frame)
							focal	= focal*10.0
							f.write("setKeyframe -at focalLength -t %d -v %.15f $cameraShape;\n"%(frame+frame0,focal))

							frame	+= 1

				#
				# write camera point group...

				f.write("\n")
				f.write("// create camera point group...\n")
				name	= "cameraPGroup_%s_1"%validName(tde4.getPGroupName(campg))
				f.write("string $pointGroupName = `group -em -name  \"%s\" -parent $sceneGroupName`;\n"%name)
				f.write("$pointGroupName = ($sceneGroupName + \"|\" + $pointGroupName);\n")
				f.write("\n")

				# write points...
				l	= tde4.getPointList(campg)
				for p in l:
					if tde4.isPointCalculated3D(campg,p):
						name	= tde4.getPointName(campg,p)
						name	= "p%s"%validName(name)
						p3d	= tde4.getPointCalcPosition3D(campg,p)
						p3d	= convertZup(p3d,yup)
						f.write("\n")
						f.write("// create point %s...\n"%name)
						f.write("string $locator = stringArrayToString(`spaceLocator -name %s`, \"\");\n"%name)
						f.write("$locator = (\"|\" + $locator);\n")
						f.write("xform -t %.15f %.15f %.15f $locator;\n"%(p3d[0],p3d[1],p3d[2]))
						f.write("parent $locator $pointGroupName;\n")

				f.write("\n")
				f.write("xform -zeroTransformPivots -rotateOrder zxy -scale 1.000000 1.000000 1.000000 $pointGroupName;\n")
				f.write("\n")


				#
				# write object/mocap point groups...

				camera		= tde4.getCurrentCamera()
				noframes	= tde4.getCameraNoFrames(camera)
				pgl		= tde4.getPGroupList()
				index		= 1
				for pg in pgl:
					if tde4.getPGroupType(pg)=="OBJECT" and camera!=None:
						f.write("\n")
						f.write("// create object point group...\n")
						pgname	= "objectPGroup_%s_%d_1"%(validName(tde4.getPGroupName(pg)),index)
						index	+= 1
						f.write("string $pointGroupName = `group -em -name  \"%s\" -parent $sceneGroupName`;\n"%pgname)
						f.write("$pointGroupName = ($sceneGroupName + \"|\" + $pointGroupName);\n")

						# write points...
						l	= tde4.getPointList(pg)
						for p in l:
							if tde4.isPointCalculated3D(pg,p):
								name	= tde4.getPointName(pg,p)
								name	= "p%s"%validName(name)
								p3d	= tde4.getPointCalcPosition3D(pg,p)
								p3d	= convertZup(p3d,yup)
								f.write("\n")
								f.write("// create point %s...\n"%name)
								f.write("string $locator = stringArrayToString(`spaceLocator -name %s`, \"\");\n"%name)
								f.write("$locator = (\"|\" + $locator);\n")
								f.write("xform -t %.15f %.15f %.15f $locator;\n"%(p3d[0],p3d[1],p3d[2]))
								f.write("parent $locator $pointGroupName;\n")

						f.write("\n")
						scale	= tde4.getPGroupScale3D(pg)
						f.write("xform -zeroTransformPivots -rotateOrder zxy -scale %.15f %.15f %.15f $pointGroupName;\n"%(scale,scale,scale))

						# animate object point group...
						f.write("\n")
						f.write("// animating point group %s...\n"%pgname)
						frame	= 1
						while frame<=noframes:
							# rot/pos...
							p3d	= tde4.getPGroupPosition3D(pg,camera,frame)
							p3d	= convertZup(p3d,yup)
							r3d	= tde4.getPGroupRotation3D(pg,camera,frame)
							rot	= convertToAngles(r3d)
							if frame>1:
								rot	= [ angleMod360(rot0[0],rot[0]), angleMod360(rot0[1],rot[1]), angleMod360(rot0[2],rot[2]) ]
							rot0	= rot
							f.write("setKeyframe -at translateX -t %d -v %.15f $pointGroupName; "%(frame+frame0,p3d[0]))
							f.write("setKeyframe -at translateY -t %d -v %.15f $pointGroupName; "%(frame+frame0,p3d[1]))
							f.write("setKeyframe -at translateZ -t %d -v %.15f $pointGroupName; "%(frame+frame0,p3d[2]))
							f.write("setKeyframe -at rotateX -t %d -v %.15f $pointGroupName; "%(frame+frame0,rot[0]))
							f.write("setKeyframe -at rotateY -t %d -v %.15f $pointGroupName; "%(frame+frame0,rot[1]))
							f.write("setKeyframe -at rotateZ -t %d -v %.15f $pointGroupName;\n"%(frame+frame0,rot[2]))

							frame	+= 1

					# mocap point groups...
					if tde4.getPGroupType(pg)=="MOCAP" and camera!=None:
						f.write("\n")
						f.write("// create mocap point group...\n")
						pgname	= "objectPGroup_%s_%d_1"%(validName(tde4.getPGroupName(pg)),index)
						index	+= 1
						f.write("string $pointGroupName = `group -em -name  \"%s\" -parent $sceneGroupName`;\n"%pgname)
						f.write("$pointGroupName = ($sceneGroupName + \"|\" + $pointGroupName);\n")

						# write points...
						l	= tde4.getPointList(pg)
						for p in l:
							if tde4.isPointCalculated3D(pg,p):
								name	= tde4.getPointName(pg,p)
								name	= "p%s"%validName(name)
								p3d	= tde4.getPointMoCapCalcPosition3D(pg,p,camera,1)
								p3d	= convertZup(p3d,yup)
								f.write("\n")
								f.write("// create point %s...\n"%name)
								f.write("string $locator = stringArrayToString(`spaceLocator -name %s`, \"\");\n"%name)
								f.write("$locator = (\"|\" + $locator);\n")
								f.write("xform -t %.15f %.15f %.15f $locator;\n"%(p3d[0],p3d[1],p3d[2]))
								for frame in range(1,noframes+1):
									p3d	= tde4.getPointMoCapCalcPosition3D(pg,p,camera,frame)
									p3d	= convertZup(p3d,yup)
									f.write("setKeyframe -at translateX -t %d -v %.15f $locator; "%(frame+frame0,p3d[0]))
									f.write("setKeyframe -at translateY -t %d -v %.15f $locator; "%(frame+frame0,p3d[1]))
									f.write("setKeyframe -at translateZ -t %d -v %.15f $locator; "%(frame+frame0,p3d[2]))
								f.write("parent $locator $pointGroupName;\n")

						f.write("\n")
						scale	= tde4.getPGroupScale3D(pg)
						f.write("xform -zeroTransformPivots -rotateOrder zxy -scale %.15f %.15f %.15f $pointGroupName;\n"%(scale,scale,scale))

						# animate mocap point group...
						f.write("\n")
						f.write("// animating point group %s...\n"%pgname)
						frame	= 1
						while frame<=noframes:
							# rot/pos...
							p3d	= tde4.getPGroupPosition3D(pg,camera,frame)
							p3d	= convertZup(p3d,yup)
							r3d	= tde4.getPGroupRotation3D(pg,camera,frame)
							rot	= convertToAngles(r3d)
							if frame>1:
								rot	= [ angleMod360(rot0[0],rot[0]), angleMod360(rot0[1],rot[1]), angleMod360(rot0[2],rot[2]) ]
							rot0	= rot
							f.write("setKeyframe -at translateX -t %d -v %.15f $pointGroupName; "%(frame+frame0,p3d[0]))
							f.write("setKeyframe -at translateY -t %d -v %.15f $pointGroupName; "%(frame+frame0,p3d[1]))
							f.write("setKeyframe -at translateZ -t %d -v %.15f $pointGroupName; "%(frame+frame0,p3d[2]))
							f.write("setKeyframe -at rotateX -t %d -v %.15f $pointGroupName; "%(frame+frame0,rot[0]))
							f.write("setKeyframe -at rotateY -t %d -v %.15f $pointGroupName; "%(frame+frame0,rot[1]))
							f.write("setKeyframe -at rotateZ -t %d -v %.15f $pointGroupName;\n"%(frame+frame0,rot[2]))

							frame	+= 1


				#
				# global (scene node) transformation...

				p3d	= tde4.getScenePosition3D()
				p3d	= convertZup(p3d,yup)
				r3d	= tde4.getSceneRotation3D()
				rot	= convertToAngles(r3d)
				s	= tde4.getSceneScale3D()
				f.write("xform -zeroTransformPivots -rotateOrder zxy -translation %.15f %.15f %.15f -scale %.15f %.15f %.15f -rotation %.15f %.15f %.15f $sceneGroupName;\n\n"%(p3d[0],p3d[1],p3d[2],s,s,s,rot[0],rot[1],rot[2]))

				f.write("\n")
				f.close()
				# tde4.postQuestionRequester("Export Maya...","Project successfully exported.","Ok")
				print '--> successfully exported Maya Mel'
			else:
				tde4.postQuestionRequester("Export Maya...","Error, couldn't open file.","Ok")

	return get_mel_filename()['path']


def do_maya_import(path):
	with MayaConnectWrapper() as maya:
		maya.send('\n\nprint "{path}";'.format(path=path))
		maya.send('source "{path}"'.format(path=path))




if __name__ == '__main__':
	melscript = main()
	# print(melscript)
	try:
		do_maya_import(melscript)
	except:
		pass

	print('--> Done...')
