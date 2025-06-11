#############################################################
###################HEY TRACTOR v1.0##########################
#################by Andrea Geremia###########################
###############www.andreageremia.it##########################
#############################################################


#*****************************************************************
#*****************************************************************
#******************ADD THIS TO YOUR FILE INIT.PY******************
#*************change 'yourPath' with the right name***************
#Tractor_path = "./Tractor"
#*****************************************************************
#*****************************************************************

import nuke
import sys
import os
import webbrowser
import Tractor
Tractor_path = "./Tractor"


# Add PluginPaths to tools and icons
nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./python')
nuke.pluginAddPath('./icons')
nuke.pluginAddPath('./images')
nuke.pluginAddPath('./nk_files')

# Import some helpful functions for the Tractor modules
import Tractor_helper
import Tractor_hey

# This is the prefix being used to customize the gizmo's in this toolkit
global prefixTractor
prefixTractor = "Tractor_"

# Store the location of this menu.py to help with nuke.nodePaste() which requires a filepath to paste
Tractor_FolderPath = os.path.dirname(__file__)
Tractor_helper.Tractor_FolderPath = Tractor_FolderPath


#import Tractor
try:
	import Tractor_hey
except Exception:
	print("Error importing Tractor_hey script")
#MENU on TOP
menubar = nuke.menu("Nuke")

menubar.addCommand('Tractor/TractorSpool', "Tractor_hey.main()", icon = os.path.join(Tractor_path, "icon/tractor-icon_black.png") )
menubar.addSeparator()
#INFO
menubar.addCommand('Tractor/Infos & Tutorial', "nuke.tcl('start', 'http://www.andreageremia.it/tutorial_tractor.html')", icon = os.path.join(Tractor_path, "icon/question_mark.png"))