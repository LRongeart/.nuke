# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

# Not to be confused with __init__.py, this file is sourced by Nuke whenever it
# is run, either interactively or in order to run a script. The main purpose is
# to setup the plugin_path and to set variables used to generate filenames.

# During startup the nuke lib loads this module, and a couple others, in the following order:
#   _pathsetup.py
#   init.py
#   menu.py
# _pathsetup has to be first since it sets up the paths to be able to 'import nuke'.

import sys
import os.path
import nuke_internal as nuke
import threading
import knobdefaults

execdir = os.path.dirname(sys.executable)
sys.path.append(execdir + "/plugins/modules")

# necessary to allow dll imports from plugins. only needed on Windows
if os.name == 'nt':
  os.environ['PATH'] += os.path.pathsep + os.path.join(os.path.dirname(__file__), "..")

#________________________________________________________________________#
#OCIO Overrides at startup
nuke.knobDefault('Root.colorManagement', 'OCIO')
nuke.knobDefault('Root.OCIO_config', 'custom')
defaultConfig = os.environ.get('OCIO', os.environ.get("NUKE_PATH") + '/aces_SHOW/config.ocio')
nuke.knobDefault('Root.customOCIOConfigPath', defaultConfig)
#________________________________________________________________________#


# FIXME: import nuke does not yet support OCIO which is required by the
#        default ViewerProcesses
ocioSupported = not nuke.env["ExternalPython"]
if ocioSupported :
  import nukescripts.ViewerProcess

# always use utf-8 for all strings
if hasattr(sys, "setdefaultencoding"):
  sys.setdefaultencoding("utf_8")

def threadendcallback():
  return nuke.waitForThreadsToFinish()

threading.currentThread().waitForThreadsOnExitFunc = threadendcallback

# NUKE_TEMP_DIR is initialized in _pathsetup.py
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

# Register default ViewerProcess LUTs.
if ocioSupported :
  nukescripts.ViewerProcess.register_default_viewer_processes()

# Here are some more examples of ViewerProcess setup.
#
# nuke.ViewerProcess.register("Cineon", nuke.createNode, ("ViewerProcess_1DLUT", "current Cineon"))
#
# Note that in most cases you will want to create a gizmo with the appropriate
# node inside and only expose parameters that you want the user to be able
# to modify when they open the Viewer Process node's control panel.
#
# The "apply LUT to color channels only" option will only work with ViewerProcess LUTs if they have
# a "rgb_only" knob set to 1.
#
# The VectorField node can be used to apply a 3D LUT.
# VectorField features both software (CPU) and GPU implementations.
#
# nuke.ViewerProcess.register("3D LUT", nuke.createNode, ("Vectorfield", "vfield_file /var/tmp/test.3dl"))
#
# You can also use the Truelight node.
#
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


# Pickle support

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



# Define image formats:
nuke.load("formats.tcl")
# back-compatibility for users setting root format in formats.tcl:
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

# Shuffle Label to display Channel Input name
nuke.knobDefault("Shuffle.label", "[value in1]")

# Write InputColorSpace to custom ColorSpace Input name
nuke.knobDefault("Write.colorspace", "show_acescg_out")

# Read InputColorSpace + RAW Override
nuke.knobDefault("Read.colorspace", "show_acescg_in")
nuke.knobDefault("Read.raw", "1")

# OCIOColorSpace InputColorSpace/OutputColorSpace Overrides
nuke.knobDefault("OCIOColorSpace.in_colorspace", "show_acescg_view")
nuke.knobDefault("OCIOColorSpace.out_colorspace", "show_acescg_in")

# Connect InputHidden set as True
nuke.knobDefault("Connect.hide_input", "true")


nuke.pluginAddPath("//tls-storage02/Install/NUKE/Nuke_PLUG/.nuke/NukeSurvivalToolkit_publicRelease-2.1.1/NukeSurvivalToolkit")

####Tractor
nuke.pluginAddPath("./Tractor")


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


if nuke.NUKE_VERSION_MAJOR == 12:
	import NukeToTractor12
else:
	import NukeToTractor

#eTools MENU
nuke.pluginAddPath('./eTools')
nuke.pluginAddPath('./eTools/Icons')
nuke.pluginAddPath('./eTools/Gizmos')

#X_Tools MENU
nuke.pluginAddPath('./X_Tools')
nuke.pluginAddPath('./X_Tools/Icons')
nuke.pluginAddPath('./X_Tools/Gizmos')



import nuke
import time
import socket


