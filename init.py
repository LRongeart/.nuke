# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

# Not to be confused with __init__.py, this file is sourced by Nuke whenever it
# is run, either interactively or in order to run a script. The main purpose is
# to setup the plugin_path and to set variables used to generate filenames.

# During startup the nuke lib loads this module, and a couple others, in the following order:
#   _pathsetup.py
#   init.py
#   menu.py
# _pathsetup has to be first since it sets up the paths to be able to 'import nuke'.
#___________________________________________________________________________________________________________


#=*=*=*=*=*=*=*=*=*=*
#_[]_INITIALISATION 
#
import sys
import os.path
import nuke_internal as nuke
import nuke
import threading
import knobdefaults
import time
import socket
#___________________________________________________________________________________________________________


#====================  
#_[]_OCIO_OVERRIDES_AT_STARTUP
#
nuke.knobDefault('Root.colorManagement', 'OCIO')
nuke.knobDefault('Root.OCIO_config', 'aces_1.2')
defaultConfig = os.environ.get('OCIO', '')
nuke.knobDefault('Root.customOCIOConfigPath', defaultConfig)
nuke.knobDefault('Root.monitorOutLUT', defaultConfig)

# OCIO fixMe default ViewerProcess
ocioSupported = not nuke.env["ExternalPython"]
if ocioSupported :
  import nukescripts.ViewerProcess
#___________________________________________________________________________________________________________ 


#==================== 
#_[]_MODULES_FOLDER_INTEGRATION 
#
execdir = os.path.dirname(sys.executable)
sys.path.append(execdir + "/plugins/modules")
#___________________________________________________________________________________________________________


#==================== 
#_[]_PLUGIN_DLL_IMPORT - only needed on Windows 
# 
if os.name == 'nt':
  os.environ['PATH'] += os.path.pathsep + os.path.join(os.path.dirname(__file__), "..")
#___________________________________________________________________________________________________________  


#==================== 
#_[]_UTF-8_STRING_OVERRIDE
# always use utf-8 for all strings
if hasattr(sys, "setdefaultencoding"):
  sys.setdefaultencoding("utf_8")
#___________________________________________________________________________________________________________  


#==================== 
#_[]_FINISHED_THREAD_CALLBACK
def threadendcallback():
  return nuke.waitForThreadsToFinish()
threading.current_thread().waitForThreadsOnExitFunc = threadendcallback
#___________________________________________________________________________________________________________


#====================
#_[]_NUKE_TEMP_DIR_OVERRIDE to _pathsetup.py
try:
  nuke_temp_dir = os.environ["NUKE_TEMP_DIR"]
except:
  nuke_temp_dir = ""
  assert False, "$NUKE_TEMP_DIR should have been set in _pathsetup.py nuke package has been successfully imported but it didn't set the variable"

# Stuff the NUKE_TEMP_DIR setting into the tcl environment.
# For some reason this isn't necessary on windows, the tcl environment
# gets it from the same place python has poked it back into, but on
# OSX tcl thinks NUKE_TEMP_DIR hasn't been set.
# But we'll do it all the time for consistency and 'just in case'.
# It certainly shouldn't do any harm or we've got another problem...
nuke.tcl('setenv','NUKE_TEMP_DIR',nuke_temp_dir)

for location in nuke.pluginInstallLocation():
  nuke.pluginAddPath(location, addToSysPath=False)
  for root, dirs, files in os.walk(location):
    if root != location:
      nuke.pluginAddPath(root, addToSysPath=False)

nuke.pluginAddPath("./user", addToSysPath=False)
nuke.pluginAddPath("caravr", addToSysPath=False)
nuke.pluginAddPath("air", addToSysPath=False)
nuke.pluginAddPath(r"Expression", addToSysPath=False)
knobdefaults.initKnobDefaults()
#___________________________________________________________________________________________________________


#==================== 
#_[]_HELLO NUKE
#
import hello
print("""
"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'
------------------------------------------------------------------------------------------------
>>>>>  LOG START --   init.py by Loucas RONGEART
------------------------------------------------------------------------------------------------""")
#___________________________________________________________________________________________________________ 


#==================== 
#_[]_TRACTOR
#
print(">> Importing Tractor")
Tractor_path = "//tls-storage02/Install/NUKE/Nuke_PLUG/.nuke/Tractor"
nuke.pluginAddPath("Tractor")


#_[]_TRACTOR_PLUGIN_FOLDER
#nuke.pluginAddPath("./Tractor")
#if nuke.NUKE_VERSION_MAJOR == 12:
#	import NukeToTractor12
#else:
#	import NukeToTractor
# try:
	# if nuke.NUKE_VERSION_STRING=="12.2v3":
		# Tractor_path = "./Tractor_p2"
		# nuke.pluginAddPath(Tractor_path)
# except:
	# pass

# try:
	# if nuke.NUKE_VERSION_STRING=="13.1v1":
		# Tractor_path = "Tractor_p3"
		# nuke.pluginAddPath(Tractor_path)
		# print (Tractor_path)
# except:
	# pass
#___________________________________________________________________________________________________________


#==================== 
#_[]_STAMPS 
# 
print(">> Importing Stamps")
nuke.pluginAddPath("stamps")

#___________________________________________________________________________________________________________ 


#==================== 
#_[]_eTOOLS_MENU
print(">> Importing eTools")
nuke.pluginAddPath('./eTools')
nuke.pluginAddPath('./eTools/Icons')
nuke.pluginAddPath('./eTools/Gizmos')
#___________________________________________________________________________________________________________ 


#==================== 
#_[]_X_TOOLS_MENU 
print(">> Importing X_Tools")
nuke.pluginAddPath('./X_Tools')
nuke.pluginAddPath('./X_Tools/Icons')
nuke.pluginAddPath('./X_Tools/Gizmos')
#___________________________________________________________________________________________________________ 


#====================
#_[]_NST_PLUGIN_FOLDER_CAMPUS
print(">> Importing NukeSurvivalToolkit")
nuke.pluginAddPath("./NukeSurvivalToolkit_publicRelease-2.1.1/NukeSurvivalToolkit")
#___________________________________________________________________________________________________________



#====================
#_[]_DEFAULT_VIEWERPROCESS LUTs
print(">> Loading DefaultViewerProcessLUTs")
if ocioSupported :
  nukescripts.ViewerProcess.register_default_viewer_processes()

# Here are some more examples of ViewerProcess setup.
# nuke.ViewerProcess.register("Cineon", nuke.createNode, ("ViewerProcess_1DLUT", "current Cineon"))
# Note that in most cases you will want to create a gizmo with the appropriate
# node inside and only expose parameters that you want the user to be able
# to modify when they open the Viewer Process node's control panel.
# The "apply LUT to color channels only" option will only work with ViewerProcess LUTs if they have
# a "rgb_only" knob set to 1.
# The VectorField node can be used to apply a 3D LUT.
# VectorField features both software (CPU) and GPU implementations.
# nuke.ViewerProcess.register("3D LUT", nuke.createNode, ("Vectorfield", "vfield_file /var/tmp/test.3dl"))
# You can also use the Truelight node.
# nuke.ViewerProcess.register("Truelight", nuke.createNode, ("Truelight", "profile /Applications/Nuke5.2v1/Nuke5.2v1.app/Contents/MacOS/plugins/truelight3/profiles/KodakVisionPremier display sRGB enable_display true"))

# register some file extensions to show up in the file browser as sequences
nuke.addSequenceFileExtension("ari");
nuke.addSequenceFileExtension("arri");
nuke.addSequenceFileExtension("bmp");
nuke.addSequenceFileExtension("cin");
nuke.addSequenceFileExtension("crw");
nuke.addSequenceFileExtension("cr2");
nuke.addSequenceFileExtension("dpx");
nuke.addSequenceFileExtension("dng");
nuke.addSequenceFileExtension("deepshad");
nuke.addSequenceFileExtension("dshd");
nuke.addSequenceFileExtension("dtex");
nuke.addSequenceFileExtension("exr");
nuke.addSequenceFileExtension("fpi");
nuke.addSequenceFileExtension("ftif");
nuke.addSequenceFileExtension("ftiff");
nuke.addSequenceFileExtension("gif");
nuke.addSequenceFileExtension("hdr");
nuke.addSequenceFileExtension("hdri");
nuke.addSequenceFileExtension("iff");
nuke.addSequenceFileExtension("iff16");
nuke.addSequenceFileExtension("it8");
nuke.addSequenceFileExtension("jpeg");
nuke.addSequenceFileExtension("jpg");
nuke.addSequenceFileExtension("nkpc"); # Nuke particle cache
nuke.addSequenceFileExtension("obj");
nuke.addSequenceFileExtension("pic");
nuke.addSequenceFileExtension("png");
nuke.addSequenceFileExtension("png16");
nuke.addSequenceFileExtension("psd");
nuke.addSequenceFileExtension("rgb");
nuke.addSequenceFileExtension("rgba");
nuke.addSequenceFileExtension("rgbe");
nuke.addSequenceFileExtension("rgbea");
nuke.addSequenceFileExtension("rla");
nuke.addSequenceFileExtension("sgi");
nuke.addSequenceFileExtension("sgi16");
nuke.addSequenceFileExtension("sxr");
nuke.addSequenceFileExtension("targa");
nuke.addSequenceFileExtension("tga");
nuke.addSequenceFileExtension("tif");
nuke.addSequenceFileExtension("tiff");
nuke.addSequenceFileExtension("tif16");
nuke.addSequenceFileExtension("tiff16");
nuke.addSequenceFileExtension("yuv");
nuke.addSequenceFileExtension("xpm");
nuke.addSequenceFileExtension("");
#___________________________________________________________________________________________________________


#====================
#_[]_PICKLE_SUPPORT
print(">> Loading PickleSupport")
class __node__reduce__():
  def __call__(s, className, script):
    n = nuke.createNode(className, knobs = script, inpanel = False)
    for i in range(n.inputs()): n.setInput(0, None)
    n.autoplace()
__node__reduce = __node__reduce__()

class __group__reduce__():
  def __call__(self, script):
    g = nuke.nodes.Group()
    with g:
      nuke.tcl(script)
    for i in range(g.inputs()): g.setInput(0, None)
    g.autoplace()
__group__reduce = __group__reduce__()
#___________________________________________________________________________________________________________


#====================
#_[]_IMAGE FORMATS
print(">> Loading ImageFormats")
nuke.load("formats.tcl")
#back-compatibility for users setting root format in formats.tcl:
if nuke.knobDefault("Root.format")==None:
  nuke.knobDefault("Root.format", nuke.value("root.format"))
  nuke.knobDefault("Root.proxy_format", nuke.value("root.proxy_format"))

def addProfileOutput(filename):
  print(("TIMING ENABLED: profile will be saved to ", filename))
  import nukescripts
  nukeProfiler = nukescripts.NukeProfiler()
  nukeProfiler.setPathToFile(filename)
  nuke.addBeforeRender(nukeProfiler.resetTimersAndStartProfile)
  nuke.addAfterFrameRender(nukeProfiler.addFrameProfileAndResetTimers)
  nuke.addOnScriptClose(nukeProfiler.endProfile)

if nuke.usingPerformanceTimers():
  profileFile = nuke.performanceProfileFilename()
  if profileFile != None:
    addProfileOutput(profileFile)
#___________________________________________________________________________________________________________


#====================
#_[]_KNOB_DEFAULT_OVERRIDES
print(">> Loading KnobDefaultOverrides")
# PropertiesMaxPanels at 1 Max
nuke.knobDefault("Properties.maxPanels", "1")
# [Shuffle] Label to display Channel Input name in White
nuke.knobDefault("Shuffle2.label", "[value in1]")
nuke.knobDefault("Shuffle2.note_font_color", "0x3fffff")
# [Copy] Label to display Channel Input name in White
nuke.knobDefault("Copy.note_font_color", "0x3fffff")
# [Switch] Label to display Channel Input name
nuke.knobDefault("Switch.label", "[value which]")
# [Remove] to be as 'keep/rgba'
nuke.knobDefault("Remove.operation", "keep")
nuke.knobDefault("Remove.channels", "rgb")
nuke.knobDefault("Remove.label", "[value channels]")
nuke.knobDefault("Remove.note_font_color", "0x3fffff")
# [Write] InputColorSpace to custom ColorSpace Input name
nuke.knobDefault("Write.colorspace", "color_picking")
nuke.knobDefault("Write.file_type", "exr")
nuke.knobDefault("Write.datatype", "32_bit_float")
# [Read] InputColorSpace + RAW Override
nuke.knobDefault("Read.colorspace", "rendering")
nuke.knobDefault("Read.raw", "1")
# [OCIOColorSpace] InputColorSpace/OutputColorSpace Overrides
nuke.knobDefault("OCIOColorSpace.in_colorspace", "color_picking")
nuke.knobDefault("OCIOColorSpace.out_colorspace", "rendering")
# [Connect] visibleInput set as False
nuke.knobDefault("Connect.visibleInput", "FALSE")
#___________________________________________________________________________________________________________
#=*=*=*=*=*=*=*=*=*=*

print("""------------------------------------------------------------------------------------------------
<<<<<  LOG END
------------------------------------------------------------------------------------------------
"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'
      """)