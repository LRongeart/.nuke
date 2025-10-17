#*****************************************************************
#*****************************************************************
#*****************************************************************
#*****************************************************************

import nuke
import sys
import os
import webbrowser
import nukescripts
import perf_time
import perf_time_print
import hello


try:
    import colorama
    colorama.init()
    from colorama import Fore, Style
except ImportError:
    # fallback: define dummy Fore/Style
    class Dummy:
        RESET_ALL = ''
    class DummyFore(Dummy):
        GREEN = YELLOW = RED = CYAN = MAGENTA = GREY = ''
    Fore = DummyFore()
    Style = Dummy()

import re

def cprint(*args, **kwargs):
    text = ' '.join(str(a) for a in args)
    # List of (pattern, color) tuples, multi-character patterns first
    patterns = [
        (r'[><]', Fore.LIGHTYELLOW_EX),
        (r'\+', Fore.YELLOW),
        (r'=', Fore.YELLOW),
        (r'-', Fore.YELLOW),
        (r'!', Fore.RED),
        (r'\|', Fore.YELLOW),
        (r'SUCCESS', Fore.GREEN),
        (r'Importing', Fore.LIGHTRED_EX),
        (r'Loading', Fore.LIGHTRED_EX),
        (r'Adding Path to:', Fore.LIGHTGREEN_EX),
        (r'Adding node:', Fore.LIGHTGREEN_EX),
        (r'Adding menu item:', Fore.LIGHTGREEN_EX),
        (r'menu.py', Fore.RED),
        (r'NUKE', Fore.RED),
    ]
    for pat, color in patterns:
        text = re.sub(pat, lambda m: color + m.group(0) + Style.RESET_ALL, text)
    print(text, **kwargs)

cprint(os.path.basename(__file__))
cprint("""+==============================================================================================+
>>>>>  MENU.PY STARTUP --   menu.py by Loucas RONGEART
+==============================================================================================+""")
#___________________________________________________________________________________________________________ 


cprint("""+-<INITIALIZATION>----------------------------------
| >> Importing nuke
| >> Importing sys
| >> Importing os
| >> Importing webbrowser
| >> Importing nukescripts
| >> Importing perf_time
| >> Importing perf_time_print
| >> Importing hello
+-----------------------------------------------------""")

cprint('+-<MENU.PY_MODULES>------------------------------------')

# Add PluginPaths to tools and icons
cprint("| Loading PluginPaths")

nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./python')
nuke.pluginAddPath('./icons')
nuke.pluginAddPath('./images')
nuke.pluginAddPath('./nk_files')
nuke.pluginAddPath('./performanceTimers')
nuke.pluginAddPath('./tractor')

cprint("| >> -SUCCESS- Loaded: PluginPaths .....100%")
cprint("+-<pluginPaths.printFolders()>------------")
cprint("| >> Adding Path to: ('./gizmos')")
cprint("| >> Adding Path to: ('./python')")
cprint("| >> Adding Path to: ('./icons')")
cprint("| >> Adding Path to: ('./images')")
cprint("| >> Adding Path to: ('./nk_files')")
cprint("| >> Adding Path to: ('./performanceTimers')")
cprint("| >> Adding Path to: ('./tractor')")
cprint("+-----------------------------------------------------")

# Import some helpful functions for the NST
cprint("| Loading NST_helper")
import NST_helper
cprint("| >> -SUCCESS- Loaded: NST_helper .....100%")

# This is the prefix being used to customize the gizmo's in this toolkit
global prefixNST
prefixNST = "NST_"

# Import Reformat Presets
cprint("| Loading reformat_presets")
import reformat_presets
reformat_presets.nodePresetReformat()
cprint("| >> -SUCCESS- Loaded: reformat_presets .....100%")

# Store the location of this menu.py to help with nuke.nodePaste() which requires a filepath to paste
NST_FolderPath = os.path.dirname(__file__)
NST_helper.NST_FolderPath = NST_FolderPath

# give the name of the help doc .pdf in main folder
NST_helpDoc = "NukeSurvivalToolkit_Documentation_Release_v2.1.0.pdf"

# creating full filepath to the help doc
NST_helpDoc_os_path = os.path.join(NST_FolderPath, NST_helpDoc)
NST_helpDocPath = "file:///{}".format(NST_helpDoc_os_path)


############################################################################################################
############################################################################################################
cprint("| Loading PerformanceTimers")

nuke_menu = nuke.menu('Nuke')
split_nuke_menu = nuke_menu.addMenu('PerformanceTimers')
split_nuke_menu.addCommand('Performance Timers', 'perf_time.show_panel()')
split_nuke_menu.addCommand('Performance Timers Print', 'perf_time_print.pf_panel()')
#
pane_menu = nuke.menu('Pane')
pane_menu.addCommand('Performance Timers', perf_time.add_perf_time_panel)
nukescripts.registerPanel('com.splitthediff.perfTime', perf_time.add_perf_time_panel)

cprint("| >> -SUCCESS- Loaded: PerformanceTimers .....100%")
############################################################################################################
############################################################################################################
cprint("| Loading KnobScripter")

# Create KnobScripter Menu
import KnobScripter

cprint("| >> -SUCCESS- Loaded: KnobScripter .....100%")
############################################################################################################
############################################################################################################
cprint("| Loading NukeSurvivalToolkitMenu")

# Create NukeSurivalToolkit Menu
toolbar = nuke.menu('Nodes')
m = toolbar.addMenu('NukeSurvivalToolkit', icon = "SurvivalToolkit.png")

cprint("| >> -SUCCESS- Loaded: NukeSurvivalToolkitMenu .....100%")
############################################################################################################
############################################################################################################
cprint("| Loading X_Tools")

# Create X_Tools Menu
toolbar = nuke.toolbar("Nodes")
m = toolbar.addMenu("X_Tools", icon="X_Tools.png")
m.addCommand("X_Waveform", "nuke.createNode(\"X_Waveform\")", icon="X_Waveform.png")

cprint("| >> -SUCCESS- Loaded: X_Tools .....100%")
############################################################################################################
############################################################################################################
cprint("| Loading NukeSurvivalToolkitDocumentation")

# Create Button to Open NukeSurivalToolkit Documentation
def openNSTDocumentation():
    webbrowser.open(NST_helpDocPath)
m.addCommand("Documentation", "openNSTDocumentation()", icon="info_icon.png", index = 00)

cprint("| >> -SUCCESS- Loaded: NukeSurvivalToolkitDocumentation .....100%")
############################################################################################################
############################################################################################################
cprint("| Loading RotoPaintBrush")

#Create RotoPaintBrush to 'Draw' Menu
nuke.menu('Nodes').addCommand('Draw/RotoPaintBrush', "nuke.createNode('RotoPaintBrush.gizmo')", icon='RotoPaintBrush.png')

cprint("| >> -SUCCESS- Loaded: RotoPaintBrush .....100%")
############################################################################################################
############################################################################################################

# Create Image Menu
imageMenu = m.addMenu('Image', icon = 'ToolbarImage.png', index = 10)
imageMenu.addCommand('LabelFromRead TL', "nuke.createNode('{}LabelFromRead')".format(prefixNST), icon="LabelFromRead.png")

############################################################################################################
############################################################################################################
cprint("| Loading NukeSurvivalToolkitGizmos")

#NUKE_SURVIVAL_TOOLKIT_GIZMOS
drawMenu = m.addMenu('Draw', icon = 'ToolbarDraw.png', index = 20) # Create Draw Menu
expressionMenu = drawMenu.addMenu("Expression Nodes AG", icon = os.path.join(NST_FolderPath, "icons/expr.png"), index=000 )
expressionMenu.addMenu( 'Creations', icon = os.path.join(NST_FolderPath, "icons/expr_01.png") )
expressionMenu.addMenu( 'Alpha', icon = os.path.join(NST_FolderPath, "icons/expr_02.png") )
expressionMenu.addMenu( 'Pixel', icon = os.path.join(NST_FolderPath, "icons/expr_03.png") )
expressionMenu.addMenu( 'Keying and Despill', icon = os.path.join(NST_FolderPath, "icons/expr_04.png") )
expressionMenu.addMenu( 'Transform', icon = os.path.join(NST_FolderPath, "icons/expr_05.png") )
expressionMenu.addMenu( '3D and Deep', icon = os.path.join(NST_FolderPath, "icons/expr_06.png") )
#CREATIONS
expressionMenu.addCommand('Creations/Random/Random Colors', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/Random_colors.nk") + "\")")
expressionMenu.addCommand('Creations/Random/Random every Frame', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/Random_every_frame.nk") + "\")")
expressionMenu.addCommand('Creations/Random/Random every Pixel', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/Random_every_pixel.nk") + "\")")
expressionMenu.addCommand('Creations/Noise/Noise', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/Noise.nk") + "\")")
expressionMenu.addCommand('Creations/Noise/fBm', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/fBm.nk") + "\")")
expressionMenu.addCommand('Creations/Noise/Turbulence', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/turbulence.nk") + "\")")
expressionMenu.addCommand('Creations/lines vertical', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/Lines_Vertical.nk") + "\")")
expressionMenu.addCommand('Creations/lines horizontal', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/Lines_Horizontal.nk") + "\")")
expressionMenu.addCommand('Creations/lines vertical animated', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/Lines_Vertical_Animated.nk") + "\")")
expressionMenu.addCommand('Creations/lines horizontal animated', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/Lines_Horizontal_Animated.nk") + "\")")
expressionMenu.addCommand('Creations/circles', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/circles.nk") + "\")")
expressionMenu.addCommand('Creations/circles user', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/circles_user.nk") + "\")")
expressionMenu.addCommand('Creations/points', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/points.nk") + "\")")
expressionMenu.addCommand('Creations/points advanced', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/points_advanced.nk") + "\")")
expressionMenu.addCommand('Creations/bricks', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/bricks.nk") + "\")")
expressionMenu.addCommand('Creations/gradient horizontal', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/gradient_horizontal.nk") + "\")")
expressionMenu.addCommand('Creations/gradient horizontal invert', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/gradient_horizontal_invert.nk") + "\")")
expressionMenu.addCommand('Creations/gradient vertical', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/gradient_vertical.nk") + "\")")
expressionMenu.addCommand('Creations/gradient vertical invert', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/gradient_vertical_invert.nk") + "\")")
expressionMenu.addCommand('Creations/gradient 4 corners', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/GradientCorner.nk") + "\")")
expressionMenu.addCommand('Creations/radial', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/radial.nk") + "\")")
expressionMenu.addCommand('Creations/radial gradient', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/radial_gradient.nk") + "\")")
expressionMenu.addCommand('Creations/radial rays', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/radial_rays.nk") + "\")")
expressionMenu.addCommand('Creations/Trunc', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/Trunc.nk") + "\")")
#ALPHA
expressionMenu.addCommand('Alpha/alpha binary', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/alpha_binary.nk") + "\")")
expressionMenu.addCommand('Alpha/alpha comparison', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/alpha_comparison.nk") + "\")")
expressionMenu.addCommand('Alpha/alpha exists?', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/alpha_exists.nk") + "\")")
expressionMenu.addCommand('Alpha/alpha sum', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/alpha_sum.nk") + "\")")
#PIXEL
expressionMenu.addCommand('Pixel/absolute value', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/abs.nk") + "\")")
expressionMenu.addCommand('Pixel/check negative', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/check_negative.nk") + "\")")
expressionMenu.addCommand('Pixel/check nan inf pixels', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/check_nan_inf.nk") + "\")")
expressionMenu.addCommand('Pixel/create nan pixel', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/create_nan.nk") + "\")")
expressionMenu.addCommand('Pixel/kill nan pixel', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/kill_nan.nk") + "\")")
expressionMenu.addCommand('Pixel/create inf pixel', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/create_inf.nk") + "\")")
expressionMenu.addCommand('Pixel/kill inf pixel', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/kill_inf.nk") + "\")")
#TRANSFORM
expressionMenu.addCommand('Transform/Coordinates', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/coordinates.nk") + "\")")
expressionMenu.addCommand('Transform/UV to Vector', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/UV_to_Vector.nk") + "\")")
expressionMenu.addCommand('Transform/Vector to UV', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/Vector_to_UV.nk") + "\")")
expressionMenu.addCommand('Transform/transform', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/transform.nk") + "\")")
expressionMenu.addCommand('Transform/transform advanced', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/transform_advanced.nk") + "\")")
expressionMenu.addCommand('Transform/twist', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/twist.nk") + "\")")
expressionMenu.addCommand('Transform/STMap_invert', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/STMap_invert.nk") + "\")")
#3D and DEEP
expressionMenu.addCommand('3D and Deep/Normal Pass - Relight', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/normalPass_relight.nk") + "\")")
expressionMenu.addCommand('3D and Deep/C4x4', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/C4x4.nk") + "\")")
expressionMenu.addCommand('3D and Deep/Deep Thickness', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/deepThickness.nk") + "\")")
expressionMenu.addCommand('3D and Deep/Deep to Depth', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/deepToDepth.nk") + "\")")
expressionMenu.addCommand('3D and Deep/Depth normalize', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/depth_normalize.nk") + "\")")
#KEYING and DESPILL
expressionMenu.addCommand('Keying and Despill/despill green', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/despill_green.nk") + "\")")
expressionMenu.addCommand('Keying and Despill/despill green list', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/despill_green_list.nk") + "\")")
expressionMenu.addCommand('Keying and Despill/despill blue', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/despill_blue.nk") + "\")")
expressionMenu.addCommand('Keying and Despill/despill blue list', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/despill_blue_list.nk") + "\")")
expressionMenu.addCommand('Keying and Despill/keying', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/keying.nk") + "\")")
expressionMenu.addCommand('Keying and Despill/differenceKey', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/differenceKey.nk") + "\")")
expressionMenu.addCommand('Keying and Despill/IBKGizmo_Expression', "nuke.nodePaste(\"" + os.path.join(NST_FolderPath + "/nk_files/IBKGizmo_Expression.nk") + "\")")
expressionMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
#INFO
expressionMenu.addCommand('Info e Tutorial', "nuke.tcl('start', 'http://www.andreageremia.it/tutorial_expression_node.html')", icon = os.path.join(NST_FolderPath, "icons/question_mark.png"))
drawMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
drawMenu.addCommand('GradMagic TL', "nuke.createNode('{}GradMagic')".format(prefixNST), icon="GradMagic.png")
drawMenu.addCommand('NoiseAdvanced TL', "nuke.createNode('{}NoiseAdvanced')".format(prefixNST), icon="Noise.png")
drawMenu.addCommand('RadialAdvanced TL', "nuke.createNode('{}RadialAdvanced')".format(prefixNST), icon="Radial.png")
drawMenu.addCommand('UV Map AG', "nuke.createNode('{}UV_Map')".format(prefixNST), icon="AG_UVMap.png")
drawMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
drawMenu.addCommand('WaterLens MJT', "nuke.createNode('{}WaterLens')".format(prefixNST), icon="WaterLens.png")
drawMenu.addCommand("Silk MHD", "nuke.createNode('{}h_silk')".format(prefixNST), icon="h_silk.png")

# Try to add GradientEditor
try:
    import ColorGradientUi
    drawMenu.addCommand("GradientEditor MHD", "nuke.createNode('{}h_gradienteditor')".format(prefixNST), icon="h_gradienteditor.png")
except:
    cprint("Could not load ColorGradientUi from HagbarthTools folder")
    pass

drawMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
drawMenu.addCommand('VoronoiGradient NKPD', "nuke.createNode('{}VoronoiGradient')".format(prefixNST), icon="GradMagic.png")
drawMenu.addCommand('CellNoise NKPD', "nuke.createNode('{}CellNoise')".format(prefixNST), icon="Noise.png")
drawMenu.addCommand('LineTool NKPD', "nuke.createNode('{}LineTool')".format(prefixNST), icon="nukepedia_icon.png")
drawMenu.addCommand('PlotScanline NKPD', "nuke.createNode('{}PlotScanline')".format(prefixNST), icon="nukepedia_icon.png")
drawMenu.addCommand('SliceTool FR', "nuke.createNode('{}SliceTool')".format(prefixNST), icon="Histogram.png")
drawMenu.addCommand('PerspectiveGuide NKPD', "nuke.createNode('{}PerspectiveGuide')".format(prefixNST), icon="nukepedia_icon.png")
drawMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
drawMenu.addCommand('DasGrain FH', "nuke.createNode('{}DasGrain')".format(prefixNST), icon="Grain.png")
drawMenu.addCommand('LumaGrain LUMA', "nuke.createNode('{}LumaGrain')".format(prefixNST), icon="nukepedia_icon.png")
drawMenu.addCommand('Grain_Advanced SPIN', "nuke.createNode('{}Grain_Advanced')".format(prefixNST), icon="spin_tools.png")
drawMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
drawMenu.addCommand("X_Tesla XM", "nuke.createNode('{}X_Tesla')".format(prefixNST), icon="X_Tesla.png")
drawMenu.addCommand('SpotFlare MHD', "nuke.createNode('{}SpotFlare')".format(prefixNST), icon="Flare.png")
drawMenu.addCommand('FlareSuperStar NKPD', "nuke.createNode('{}FlareSuperStar')".format(prefixNST), icon="nukepedia_icon.png")
drawMenu.addCommand('AutoFlare NKPD', "NST_helper.filepathCreateNode('{}AutoFlare2')".format(prefixNST), icon="Flare.png")
drawMenu.addCommand("BokehBuilder KB", "nuke.createNode('{}BokehBuilder')".format(prefixNST), icon="K_BokehBuilder.png")
drawMenu.addCommand("LensEngine KB", "nuke.createNode('{}LensEngine')".format(prefixNST), icon="K_LensEngine.png")

cprint("| >> -SUCCESS- Loaded: NukeSurvivalToolkitGizmos .....100%")
cprint("+-<NukeSurvivalToolkitGizmos.printGizmos()>-----------")
cprint("| >> Adding node: ('Creations/Random/Random Colors')")
cprint("| >> Adding node: ('Creations/Random/Random every Frame')")
cprint("| >> Adding node: ('Creations/Random/Random every Pixel')")
cprint("| >> Adding node: ('Creations/Noise/Noise')")
cprint("| >> Adding node: ('Creations/Noise/fBm')")
cprint("| >> Adding node: ('Creations/Noise/Turbulence')")
cprint("| >> Adding node: ('Creations/lines vertical')")
cprint("| >> Adding node: ('Creations/lines horizontal')")
cprint("| >> Adding node: ('Creations/lines vertical animated')")
cprint("| >> Adding node: ('Creations/lines horizontal animated')")
cprint("| >> Adding node: ('Creations/circles')")
cprint("| >> Adding node: ('Creations/circles user')")
cprint("| >> Adding node: ('Creations/points')")
cprint("| >> Adding node: ('Creations/points advanced')")
cprint("| >> Adding node: ('Creations/bricks')")
cprint("| >> Adding node: ('Creations/gradient horizontal')")
cprint("| >> Adding node: ('Creations/gradient horizontal invert')")
cprint("| >> Adding node: ('Creations/gradient vertical')")
cprint("| >> Adding node: ('Creations/gradient vertical invert')")
cprint("| >> Adding node: ('Creations/gradient 4 corners')")
cprint("| >> Adding node: ('Creations/radial')")
cprint("| >> Adding node: ('Creations/radial gradient')")
cprint("| >> Adding node: ('Creations/radial rays')")
cprint("| >> Adding node: ('Creations/Trunc')")
cprint("| >> Adding node: ('Alpha/alpha binary')")
cprint("| >> Adding node: ('Alpha/alpha comparison')")
cprint("| >> Adding node: ('Alpha/alpha exists?')")
cprint("| >> Adding node: ('Alpha/alpha sum')")
cprint("| >> Adding node: ('Pixel/absolute value')")
cprint("| >> Adding node: ('Pixel/check negative')")
cprint("| >> Adding node: ('Pixel/check nan inf pixels')")
cprint("| >> Adding node: ('Pixel/create nan pixel')")
cprint("| >> Adding node: ('Pixel/kill nan pixel')")
cprint("| >> Adding node: ('Pixel/create inf pixel')")
cprint("| >> Adding node: ('Pixel/kill inf pixel')")
cprint("| >> Adding node: ('Transform/Coordinates')")
cprint("| >> Adding node: ('Transform/UV to Vector')")
cprint("| >> Adding node: ('Transform/Vector to UV')")
cprint("| >> Adding node: ('Transform/transform')")
cprint("| >> Adding node: ('Transform/transform advanced')")
cprint("| >> Adding node: ('Transform/twist')")
cprint("| >> Adding node: ('Transform/STMap_invert')")
cprint("| >> Adding node: ('3D and Deep/Normal Pass - Relight')")
cprint("| >> Adding node: ('3D and Deep/C4x4')")
cprint("| >> Adding node: ('3D and Deep/Deep Thickness')")
cprint("| >> Adding node: ('3D and Deep/Deep to Depth')")
cprint("| >> Adding node: ('3D and Deep/Depth normalize')")
cprint("| >> Adding node: ('Keying and Despill/despill green')")
cprint("| >> Adding node: ('Keying and Despill/despill green list')")
cprint("| >> Adding node: ('Keying and Despill/despill blue')")
cprint("| >> Adding node: ('Keying and Despill/despill blue list')")
cprint("| >> Adding node: ('Keying and Despill/keying')")
cprint("| >> Adding node: ('Keying and Despill/differenceKey')")
cprint("| >> Adding node: ('Keying and Despill/IBKGizmo_Expression')")
cprint("| >> Adding node: ('Draw/GradMagic TL')")
cprint("| >> Adding node: ('Draw/NoiseAdvanced TL')")
cprint("| >> Adding node: ('Draw/RadialAdvanced TL')")
cprint("| >> Adding node: ('Draw/UV Map AG')")
cprint("| >> Adding node: ('Draw/WaterLens MJT')")
cprint("| >> Adding node: ('Draw/Silk MHD')")
cprint("| >> Adding node: ('Draw/h_gradienteditor')")
cprint("| >> Adding node: ('Draw/VoronoiGradient NKPD')")
cprint("| >> Adding node: ('Draw/CellNoise NKPD')")
cprint("| >> Adding node: ('Draw/LineTool NKPD')")
cprint("| >> Adding node: ('Draw/PlotScanline NKPD')")
cprint("| >> Adding node: ('Draw/SliceTool FR')")
cprint("| >> Adding node: ('Draw/PerspectiveGuide NKPD')")
cprint("| >> Adding node: ('Draw/DasGrain FH')")
cprint("| >> Adding node: ('Draw/LumaGrain LUMA')")
cprint("| >> Adding node: ('Draw/Grain_Advanced SPIN')")
cprint("| >> Adding node: ('Draw/X_Tesla XM')")
cprint("| >> Adding node: ('Draw/SpotFlare MHD')")
cprint("| >> Adding node: ('Draw/FlareSuperStar NKPD')")
cprint("| >> Adding node: ('Draw/AutoFlare NKPD')")
cprint("| >> Adding node: ('Draw/BokehBuilder KB')")
cprint("| >> Adding node: ('Draw/LensEngine KB')")
cprint("| >> Adding node: ('Draw/RotoPaintBrush')")
cprint("| >> Adding node: ('Draw/LabelFromRead TL')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading BL_Tools")

# Add /gizmos/bl_* nodes
BL = m.addMenu('BL_Tools', icon = 'icons/BL.png', index = 30)
nuke.menu('Nodes').addCommand('BL/bl_Arc', "nuke.createNode('bl_Arc.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_BlurChroma', "nuke.createNode('bl_BlurChroma.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Bokeh', "nuke.createNode('bl_Bokeh.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Bulge', "nuke.createNode('bl_Bulge.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Bytes', "nuke.createNode('bl_Bytes.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_ChannelBox', "nuke.createNode('bl_ChannelBox.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_ChromaticAberation', "nuke.createNode('bl_ChromaticAberation.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_CleanOUT', "nuke.createNode('bl_CleanOUT.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_ColorEdge', "nuke.createNode('bl_ColorEdge.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_ColorSupress', "nuke.createNode('bl_ColorSupress.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Compress', "nuke.createNode('bl_Compress.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Convolve', "nuke.createNode('bl_Convolve.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_CurveFilter', "nuke.createNode('bl_CurveFilter.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Despillator', "nuke.createNode('bl_Despillator.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_EdgeExtend2', "nuke.createNode('bl_EdgeExtend2.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Emboss', "nuke.createNode('bl_Emboss.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Expand', "nuke.createNode('bl_Expand.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Filler', "nuke.createNode('bl_Filler.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_GUISwitch', "nuke.createNode('bl_GUISwitch.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_HSVKeyer', "nuke.createNode('bl_HSVKeyer.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_IBlur', "nuke.createNode('bl_IBlur.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_IBokeh', "nuke.createNode('bl_IBokeh.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_IDilateErode', "nuke.createNode('bl_IDilateErode.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_IDisplace', "nuke.createNode('bl_IDisplace.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_ITime', "nuke.createNode('bl_ITime.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_LayerAE', "nuke.createNode('bl_LayerAE.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Line', "nuke.createNode('bl_Line.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Match', "nuke.createNode('bl_Match.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_mf_Binary', "nuke.createNode('bl_mf_Binary.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_mf_Border', "nuke.createNode('bl_mf_Border.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_mf_DirectionalBlur', "nuke.createNode('bl_mf_DirectionalBlur.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_mf_Occlusion', "nuke.createNode('bl_mf_Occlusion.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_mf_ShapeSofter', "nuke.createNode('bl_mf_ShapeSofter.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Monochrome', "nuke.createNode('bl_Monochrome.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Mosaic', "nuke.createNode('bl_Mosaic.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Normalizer', "nuke.createNode('bl_Normalizer.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Random', "nuke.createNode('bl_Random.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Randomizer', "nuke.createNode('bl_Randomizer.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Sample', "nuke.createNode('bl_Sample.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_SaturationRGB', "nuke.createNode('bl_SaturationRGB.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_ScanLines', "nuke.createNode('bl_ScanLines.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Scatterize', "nuke.createNode('bl_Scatterize.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Scroll', "nuke.createNode('bl_Scroll.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_SetBBOXColor', "nuke.createNode('bl_SetBBOXColor.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Shape', "nuke.createNode('bl_Shape.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Slice', "nuke.createNode('bl_Slice.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Solarize', "nuke.createNode('bl_Solarize.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_SpillSupress', "nuke.createNode('bl_SpillSupress.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Star', "nuke.createNode('bl_Star.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Threshold', "nuke.createNode('bl_Threshold.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_TileMosaic', "nuke.createNode('bl_TileMosaic.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_ToBBOX', "nuke.createNode('bl_ToBBOX.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Twirl', "nuke.createNode('bl_Twirl.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Wave', "nuke.createNode('bl_Wave.gizmo')")
nuke.menu('Nodes').addCommand('BL/bl_Zebrafy', "nuke.createNode('bl_Zebrafy.gizmo')")


cprint("| >> -SUCCESS- Loaded: BL_Tools .....100%")
cprint("+-<BLTools.printGizmos()>-------------")
cprint("| >> Adding node: ('BL/bl_Arc')")
cprint("| >> Adding node: ('BL/bl_BlurChroma')")
cprint("| >> Adding node: ('BL/bl_Bokeh')")
cprint("| >> Adding node: ('BL/bl_Bulge')")
cprint("| >> Adding node: ('BL/bl_Bytes')")
cprint("| >> Adding node: ('BL/bl_ChannelBox')")
cprint("| >> Adding node: ('BL/bl_ChromaticAberation')")
cprint("| >> Adding node: ('BL/bl_CleanOUT')")
cprint("| >> Adding node: ('BL/bl_ColorEdge')")
cprint("| >> Adding node: ('BL/bl_ColorSupress')")
cprint("| >> Adding node: ('BL/bl_Compress')")
cprint("| >> Adding node: ('BL/bl_Convolve')")
cprint("| >> Adding node: ('BL/bl_CurveFilter')")
cprint("| >> Adding node: ('BL/bl_Despillator')")
cprint("| >> Adding node: ('BL/bl_EdgeExtend2')")
cprint("| >> Adding node: ('BL/bl_Emboss')")
cprint("| >> Adding node: ('BL/bl_Expand')")
cprint("| >> Adding node: ('BL/bl_Filler')")
cprint("| >> Adding node: ('BL/bl_GUISwitch')")
cprint("| >> Adding node: ('BL/bl_HSVKeyer')")
cprint("| >> Adding node: ('BL/bl_IBlur')")
cprint("| >> Adding node: ('BL/bl_IBokeh')")
cprint("| >> Adding node: ('BL/bl_IDilateErode')")
cprint("| >> Adding node: ('BL/bl_IDisplace')")
cprint("| >> Adding node: ('BL/bl_ITime')")
cprint("| >> Adding node: ('BL/bl_LayerAE')")
cprint("| >> Adding node: ('BL/bl_Line')")
cprint("| >> Adding node: ('BL/bl_Match')")
cprint("| >> Adding node: ('BL/bl_mf_Binary')")
cprint("| >> Adding node: ('BL/bl_mf_Border')")
cprint("| >> Adding node: ('BL/bl_mf_DirectionalBlur')")
cprint("| >> Adding node: ('BL/bl_mf_Occlusion')")
cprint("| >> Adding node: ('BL/bl_mf_ShapeSofter')")
cprint("| >> Adding node: ('BL/bl_Monochrome')")
cprint("| >> Adding node: ('BL/bl_Mosaic')")
cprint("| >> Adding node: ('BL/bl_Normalizer')")
cprint("| >> Adding node: ('BL/bl_Random')")
cprint("| >> Adding node: ('BL/bl_Randomizer')")
cprint("| >> Adding node: ('BL/bl_Sample')")
cprint("| >> Adding node: ('BL/bl_SaturationRGB')")
cprint("| >> Adding node: ('BL/bl_ScanLines')")
cprint("| >> Adding node: ('BL/bl_Scatterize')")
cprint("| >> Adding node: ('BL/bl_Scroll')")
cprint("| >> Adding node: ('BL/bl_SetBBOXColor')")
cprint("| >> Adding node: ('BL/bl_Shape')")
cprint("| >> Adding node: ('BL/bl_Slice')")
cprint("| >> Adding node: ('BL/bl_Solarize')")
cprint("| >> Adding node: ('BL/bl_SpillSupress')")
cprint("| >> Adding node: ('BL/bl_Star')")
cprint("| >> Adding node: ('BL/bl_Threshold')")
cprint("| >> Adding node: ('BL/bl_TileMosaic')")
cprint("| >> Adding node: ('BL/bl_ToBBOX')")
cprint("| >> Adding node: ('BL/bl_Twirl')")
cprint("| >> Adding node: ('BL/bl_Wave')")
cprint("| >> Adding node: ('BL/bl_Zebrafy')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading PxF_Tools")

# Add PxF .gizmos
PxF_Tools = m.addMenu('PxF_Tools', icon = 'icons/PxF_Menu.png', index = 30)
nuke.menu('Nodes').addCommand('PxF_Tools/PxF_Bandpass', "nuke.createNode('Pxf_Bandpass.gizmo')", icon='PxF_Bandpass.png')
nuke.menu('Nodes').addCommand('PxF_Tools/PxF_ChromaBlur', "nuke.createNode('PxF_ChromaBlur.gizmo')", icon='PxF_ChromaBlur.png')
nuke.menu('Nodes').addCommand('PxF_Tools/PxF_Distort', "nuke.createNode('Pxf_Distort.gizmo')", icon='PxF_Distort.png')
nuke.menu('Nodes').addCommand('PxF_Tools/PxF_Erode', "nuke.createNode('Pxf_Erode.gizmo')", icon='PxF_Erode.png')
nuke.menu('Nodes').addCommand('PxF_Tools/PxF_Filler', "nuke.createNode('Pxf_Filler.gizmo')", icon='PxF_Filler.png')
nuke.menu('Nodes').addCommand('PxF_Tools/PxF_Grain', "nuke.createNode('Pxf_Grain.gizmo')", icon='PxF_Grain.png')
nuke.menu('Nodes').addCommand('PxF_Tools/PxF_HueSat', "nuke.createNode('Pxf_HueSat.gizmo')", icon='PxF_HueSat.png')
nuke.menu('Nodes').addCommand('PxF_Tools/PxF_IDefocus', "nuke.createNode('Pxf_PxF_IDefocus.gizmo')", icon='PxF_PxF_IDefocus.png')
nuke.menu('Nodes').addCommand('PxF_Tools/PxF_KillSpill', "nuke.createNode('Pxf_KillSpill.gizmo')", icon='PxF_KillSpill.png')
nuke.menu('Nodes').addCommand('PxF_Tools/PxF_Line', "nuke.createNode('Pxf_Line.gizmo')", icon='PxF_Line.png')
nuke.menu('Nodes').addCommand('PxF_Tools/PxF_MergeWrap', "nuke.createNode('Pxf_MergeWrap.gizmo')", icon='PxF_MergeWrap.png')
nuke.menu('Nodes').addCommand('PxF_Tools/PxF_ScreenClean', "nuke.createNode('Pxf_ScreenClean.gizmo')", icon='PxF_ScreenClean.png')

cprint("| >> -SUCCESS- Loaded: PxF_Tools .....100%")
cprint("+-<PxFTools.printGizmos()>-------------")
cprint("| >> Adding node: ('PxF_Tools/PxF_Bandpass')")
cprint("| >> Adding node: ('PxF_Tools/PxF_ChromaBlur')") 
cprint("| >> Adding node: ('PxF_Tools/PxF_Distort')")
cprint("| >> Adding node: ('PxF_Tools/PxF_Erode')")
cprint("| >> Adding node: ('PxF_Tools/PxF_Filler')")
cprint("| >> Adding node: ('PxF_Tools/PxF_Grain')")
cprint("| >> Adding node: ('PxF_Tools/PxF_HueSat')")
cprint("| >> Adding node: ('PxF_Tools/PxF_IDefocus')")
cprint("| >> Adding node: ('PxF_Tools/PxF_KillSpill')")
cprint("| >> Adding node: ('PxF_Tools/PxF_Line')")
cprint("| >> Adding node: ('PxF_Tools/PxF_MergeWrap')")
cprint("| >> Adding node: ('PxF_Tools/PxF_ScreenClean')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading Connect")

# Add 'Connect.gizmo' to Channel menu;
nuke.menu('Nodes').addCommand('Channel/Connect', "nuke.createNode('Connect.gizmo')", icon='Connect.png')

cprint("| >> -SUCCESS- Loaded: Connect .....100%")
cprint("+-<Connect.printGizmos()>-------------")
cprint("| >> Adding node: ('Channel/Connect')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading LR_Tools")

#Add LR_AnimProject3D
nuke.menu('Nodes').addCommand('3D/LR_AnimProject3D', "nuke.createNode('LR_AnimProject3D.gizmo')")
nuke.menu('Nodes').addCommand('3D/LR_StaticProject3D', "nuke.createNode('LR_StaticProject3D.gizmo')")

cprint("| >> -SUCCESS- Loaded: LR_Tools .....100%")
cprint("+-<LRTools.printGizmos()>-------------") 
cprint("| >> Adding node: ('3D/LR_AnimProject3D')")
cprint("| >> Adding node: ('3D/LR_StaticProject3D')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading td_faster_rebuild")

#Add td_faster_rebuild
nuke.menu('Nodes').addCommand('3D/td_faster_rebuild', "nuke.createNode('td_faster_rebuild.gizmo')")

cprint("| >> -SUCCESS- Loaded: td_faster_rebuild .....100%")
cprint("+-<td_faster_rebuild.printGizmos()>-------------")
cprint("| >> Adding node: ('3D/td_faster_rebuild')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading Time_Tools")

timeMenu = m.addMenu('Time', icon = 'ToolbarTime.png', index = 30) # Create Time Menu
timeMenu.addCommand('apLoop AP', 'nuke.createNode("{}apLoop")'.format(prefixNST), icon='apLoop.png')
timeMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
timeMenu.addCommand('FrameHold Special AG', "nuke.createNode('{}FrameHoldSpecial')".format(prefixNST), icon="FrameHold.png")
timeMenu.addCommand('Looper DB', "nuke.createNode('{}Looper')".format(prefixNST), icon="nukepedia_icon.png")
timeMenu.addCommand('FrameMedian MHD', "nuke.createNode('{}FrameMedian')".format(prefixNST), icon="FrameBlend.png")
timeMenu.addCommand('TimeMachine NKPD', "nuke.createNode('{}TimeMachine')".format(prefixNST), icon="nukepedia_icon.png")
timeMenu.addCommand('FrameFiller MJT', "nuke.createNode('{}FrameFiller')".format(prefixNST), icon="FrameFiller.png")

cprint("| >> -SUCCESS- Loaded: time_Tools .....100%")
cprint("+-<TimeTools.printGizmos()>-------------")
cprint("| >> Adding node: ('Time/FrameFiller')")
cprint("| >> Adding node: ('Time/FrameHold Special')")
cprint("| >> Adding node: ('Time/Looper')")
cprint("| >> Adding node: ('Time/FrameMedian')")
cprint("| >> Adding node: ('Time/TimeMachine')")
cprint("| >> Adding node: ('Time/apLoop')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading Channel_Tools")

channelMenu = m.addMenu('Channel', icon = 'ToolbarChannel.png', index = 40) # Create Channel Menu
channelMenu.addCommand('BinaryAlpha TL', "nuke.createNode('{}BinaryAlpha')".format(prefixNST), icon="BumpBoss.png")
channelMenu.addCommand('ChannelCombiner TL', "nuke.createNode('{}ChannelCombiner')".format(prefixNST), icon="ChannelMerge.png")
channelMenu.addCommand('ChannelControl TL', "nuke.createNode('{}ChannelControl')".format(prefixNST), icon="LayerChannel.png")
channelMenu.addCommand('ChannelCreator TL', "nuke.createNode('{}ChannelCreator')".format(prefixNST), icon="Add.png")
channelMenu.addCommand('InjectMatteChannel TL', "nuke.createNode('{}InjectMatteChannel')".format(prefixNST), icon="ChannelMerge.png")
channelMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
channelMenu.addCommand('streamCart MJT', "nuke.createNode('{}streamCart')".format(prefixNST), icon="streamCart.png")
channelMenu.addCommand('renameChannels AG', "nuke.createNode('{}renameChannels')".format(prefixNST), icon="nukepedia_icon.png")

cprint("| >> -SUCCESS- Loaded: Channel_Tools .....100%")
cprint("+-<ChannelTools.printGizmos()>-------------")
cprint("| >> Adding node: ('Channel/BinaryAlpha')")
cprint("| >> Adding node: ('Channel/ChannelCombiner')")
cprint("| >> Adding node: ('Channel/ChannelControl')")
cprint("| >> Adding node: ('Channel/ChannelCreator')")
cprint("| >> Adding node: ('Channel/InjectMatteChannel')")
cprint("| >> Adding node: ('Channel/streamCart')")
cprint("| >> Adding node: ('Channel/renameChannels')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading Color_Tools")

colorMenu = m.addMenu('Color', icon = 'ToolbarColor.png', index = 50) # Create Color Menu
colorMenu.addCommand('BlacksMatch TL', "nuke.createNode('{}BlacksMatch')".format(prefixNST), icon="BlacksMatch.png")
colorMenu.addCommand('ColorCopy TL', "nuke.createNode('{}ColorCopy')".format(prefixNST), icon="Crosstalk.png")
colorMenu.addCommand('Contrast TL', "nuke.createNode('{}Contrast')".format(prefixNST), icon="ColorCorrect.png")
colorMenu.addCommand('GradeLayerPass TL', "nuke.createNode('{}GradeLayerPass')".format(prefixNST), icon="Grade.png")
colorMenu.addCommand('HighlightSuppress TL', "nuke.createNode('{}HighlightSuppress')".format(prefixNST), icon="ColorLookup.png")
colorMenu.addCommand('ShadowMult TL', "nuke.createNode('{}ShadowMult')".format(prefixNST), icon="SpotLight.png")
colorMenu.addCommand('WhiteSoftClip TL', "nuke.createNode('{}WhiteSoftClip')".format(prefixNST), icon="SoftClip.png")
colorMenu.addCommand('WhiteBalance TL', "nuke.createNode('{}WhiteBalance')".format(prefixNST), icon="HueShift.png")
colorMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
colorMenu.addCommand('apColorSampler AP', 'nuke.createNode("{}ColorSampler")'.format(prefixNST), icon='ColorSampler.png')
colorMenu.addCommand('apVignette AP', 'nuke.createNode("{}apVignette")'.format(prefixNST), icon='apeVignette.png')
colorMenu.addCommand('GammaPlus MJT', "nuke.createNode('{}GammaPlus')".format(prefixNST), icon="GammaPlus.png")
colorMenu.addCommand('MonochromePlus CF', "nuke.createNode('{}MonochromePlus')".format(prefixNST), icon="Saturation.png")
colorMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
colorMenu.addCommand('Suppress_RGBCMY SPIN', 'nuke.createNode("{}Suppress_RGBCMY")'.format(prefixNST), icon='spin_tools.png')
colorMenu.addCommand('BiasedSaturation NKPD', "nuke.createNode('{}BiasedSaturation')".format(prefixNST), icon="Saturation.png")
colorMenu.addCommand('HSL_Tool NKPD', "nuke.createNode('{}HSL_Tool')".format(prefixNST), icon="HSVTool.png")

cprint("| >> -SUCCESS- Loaded: Color_Tools .....100%")
cprint("+-<ColorTools.printGizmos()>-------------")
cprint("| >> Adding node: ('Color/BlacksMatch')")
cprint("| >> Adding node: ('Color/ColorCopy')")
cprint("| >> Adding node: ('Color/Contrast')")
cprint("| >> Adding node: ('Color/GradeLayerPass')")
cprint("| >> Adding node: ('Color/HighlightSuppress')")
cprint("| >> Adding node: ('Color/ShadowMult')")
cprint("| >> Adding node: ('Color/WhiteSoftClip')")
cprint("| >> Adding node: ('Color/WhiteBalance')")
cprint("| >> Adding node: ('Color/apColorSampler')")
cprint("| >> Adding node: ('Color/apVignette')")
cprint("| >> Adding node: ('Color/GammaPlus')")
cprint("| >> Adding node: ('Color/MonochromePlus')")
cprint("| >> Adding node: ('Color/Suppress_RGBCMY')")
cprint("| >> Adding node: ('Color/BiasedSaturation')")
cprint("| >> Adding node: ('Color/HSL_Tool')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading Filter_Tools")
# Create Filter Menu

filterMenu = m.addMenu('Filter', icon = 'ToolbarFilter.png', index = 60)

glowMenu = filterMenu.addMenu("Glows", icon="Glow.png")
#-
glowMenu.addCommand('apGlow AP', 'nuke.createNode("{}apeGlow")'.format(prefixNST), icon='apGlow.png')
glowMenu.addCommand('ExponGlow TL', 'nuke.createNode("{}ExponGlow")'.format(prefixNST), icon='Glow.png')
glowMenu.addCommand('Glow_Exponential SPIN', 'nuke.createNode("{}Glow_Exponential")'.format(prefixNST), icon="spin_tools.png")
glowMenu.addCommand('bm_OpticalGlow BM', "nuke.createNode('{}bm_OpticalGlow')".format(prefixNST), icon='bm_OpticalGlow_icon.png')
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
#-
BlurMenu = filterMenu.addMenu("Blurs", icon="Median.png")
BlurMenu.addCommand('ExponBlurSimple TL', "nuke.createNode('{}ExponBlurSimple')".format(prefixNST), icon="Glow.png")
BlurMenu.addCommand('DirectionalBlur TL', "nuke.createNode('{}DirectionalBlur')".format(prefixNST), icon="DirBlur.png")
BlurMenu.addCommand('MotionBlurPaint AG', "nuke.createNode('{}MotionBlurPaint')".format(prefixNST), icon="MotionBlur2D.png")
BlurMenu.addCommand('iBlur NKPD', "nuke.createNode('{}iBlurU')".format(prefixNST), icon="Blur.png")
BlurMenu.addCommand("WaveletBlur MHD", "nuke.createNode('{}WaveletBlur')".format(prefixNST), icon="h_tools.png")
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
#-
EdgesMenu = filterMenu.addMenu("Edges", icon="FilterErode.png")
EdgesMenu.addCommand('apEdgePush AP', 'nuke.createNode("{}apEdgePush")'.format(prefixNST), icon='apEdgePush.png')
EdgesMenu.addCommand('EdgeDetectAlias TL', "nuke.createNode('{}EdgeDetectAlias')".format(prefixNST), icon="FilterErod.png")
EdgesMenu.addCommand('AntiAliasingFilter AG', "nuke.createNode('{}AntiAliasingFilter')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('ErodeSmooth TL', "nuke.createNode('{}ErodeSmooth')".format(prefixNST), icon="FilterErode.png")
EdgesMenu.addCommand('Edge_RimLight AG', "nuke.createNode('{}Edge_RimLight')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('EdgeDetectPRO AG', "nuke.createNode('{}EdgeDetectPRO')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('Erode_Fine SPIN', "nuke.createNode('{}Erode_Fine')".format(prefixNST), icon="spin_tools.png")
EdgesMenu.addCommand('Edge_Expand SPIN', "nuke.createNode('{}Edge_Expand')".format(prefixNST), icon="spin_tools.png")
EdgesMenu.addCommand('Edge RB', "nuke.createNode('{}Edge')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('KillOutline NKPD', "nuke.createNode('{}KillOutline')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('ColorSmear NKPD', "nuke.createNode('{}ColorSmear')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('EdgeFromAlpha FR', "nuke.createNode('{}EdgeFromAlpha')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('VectorExtendEdge NKPD', "nuke.createNode('{}VectorExtendEdge')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
EdgesMenu.addCommand('FractalBlur NKPD', "nuke.createNode('{}FractalBlur')".format(prefixNST), icon="nukepedia_icon.png")
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
#-
distortMenu = filterMenu.addMenu("Distortions", icon="IDistort.png")
distortMenu.addCommand('Glass FR', "nuke.createNode('{}Glass')".format(prefixNST), icon="nukepedia_icon.png")
distortMenu.addCommand('HeatWave DB', "nuke.createNode('{}HeatWave')".format(prefixNST), icon="HeatWave_Icon.png")
distortMenu.addCommand("X_Distort XM", "nuke.createNode(\"{}X_Distort\")".format(prefixNST), icon="X_Distort.png")
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
#-
X_ToolsMenu = filterMenu.addMenu("X_Tools XM", icon="X_Tools.png")
X_ToolsMenu.addCommand("X_Aton_Volumetrics XM", "nuke.createNode(\"{}X_Aton_Volumetrics\")".format(prefixNST), icon="X_Aton.png")
X_ToolsMenu.addCommand("X_Denoise XM", "nuke.createNode(\"{}X_Denoise\")".format(prefixNST), icon="X_Denoise.png")
X_ToolsMenu.addCommand("X_Sharpen XM", "nuke.createNode(\"{}X_Sharpen\")".format(prefixNST), icon="X_Sharpen.png")
X_ToolsMenu.addCommand("X_Soften XM", "nuke.createNode(\"{}X_Soften\")".format(prefixNST), icon="X_Soften.png")
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
filterMenu.addCommand('BeautifulSkin TL', "nuke.createNode('{}BeautifulSkin')".format(prefixNST), icon="Median.png")
filterMenu.addCommand('BlacksExpon TL', "nuke.createNode('{}BlacksExpon')".format(prefixNST), icon="Toe.png")
filterMenu.addCommand('Halation TL', "nuke.createNode('{}Halation')".format(prefixNST), icon="EdgeBlur.png")
filterMenu.addCommand('HighPass TL', "nuke.createNode('{}HighPass')".format(prefixNST), icon="Invert.png")
filterMenu.addCommand('Diffusion TL', "nuke.createNode('{}Diffusion')".format(prefixNST), icon="Spark.png")
#-
filterMenu = m.addMenu('Filter', icon = 'ToolbarFilter.png', index = 60) # Create Filter Menu
glowMenu = filterMenu.addMenu("Glows", icon="Glow.png")
glowMenu.addCommand('apGlow AP', 'nuke.createNode("{}apeGlow")'.format(prefixNST), icon='apGlow.png')
glowMenu.addCommand('ExponGlow TL', 'nuke.createNode("{}ExponGlow")'.format(prefixNST), icon='Glow.png')
glowMenu.addCommand('Glow_Exponential SPIN', 'nuke.createNode("{}Glow_Exponential")'.format(prefixNST), icon="spin_tools.png")
glowMenu.addCommand('bm_OpticalGlow BM', "nuke.createNode('{}bm_OpticalGlow')".format(prefixNST), icon='bm_OpticalGlow_icon.png')
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
#-
BlurMenu = filterMenu.addMenu("Blurs", icon="Median.png")
BlurMenu.addCommand('ExponBlurSimple TL', "nuke.createNode('{}ExponBlurSimple')".format(prefixNST), icon="Glow.png")
BlurMenu.addCommand('DirectionalBlur TL', "nuke.createNode('{}DirectionalBlur')".format(prefixNST), icon="DirBlur.png")
BlurMenu.addCommand('MotionBlurPaint AG', "nuke.createNode('{}MotionBlurPaint')".format(prefixNST), icon="MotionBlur2D.png")
BlurMenu.addCommand('iBlur NKPD', "nuke.createNode('{}iBlurU')".format(prefixNST), icon="Blur.png")
BlurMenu.addCommand("WaveletBlur MHD", "nuke.createNode('{}WaveletBlur')".format(prefixNST), icon="h_tools.png")
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
#-
EdgesMenu = filterMenu.addMenu("Edges", icon="FilterErode.png")
EdgesMenu.addCommand('apEdgePush AP', 'nuke.createNode("{}apEdgePush")'.format(prefixNST), icon='apEdgePush.png')
EdgesMenu.addCommand('EdgeDetectAlias TL', "nuke.createNode('{}EdgeDetectAlias')".format(prefixNST), icon="FilterErod.png")
EdgesMenu.addCommand('AntiAliasingFilter AG', "nuke.createNode('{}AntiAliasingFilter')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('ErodeSmooth TL', "nuke.createNode('{}ErodeSmooth')".format(prefixNST), icon="FilterErode.png")
EdgesMenu.addCommand('Edge_RimLight AG', "nuke.createNode('{}Edge_RimLight')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('EdgeDetectPRO AG', "nuke.createNode('{}EdgeDetectPRO')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('Erode_Fine SPIN', "nuke.createNode('{}Erode_Fine')".format(prefixNST), icon="spin_tools.png")
EdgesMenu.addCommand('Edge_Expand SPIN', "nuke.createNode('{}Edge_Expand')".format(prefixNST), icon="spin_tools.png")
EdgesMenu.addCommand('Edge RB', "nuke.createNode('{}Edge')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('KillOutline NKPD', "nuke.createNode('{}KillOutline')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('ColorSmear NKPD', "nuke.createNode('{}ColorSmear')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('EdgeFromAlpha FR', "nuke.createNode('{}EdgeFromAlpha')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('VectorExtendEdge NKPD', "nuke.createNode('{}VectorExtendEdge')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addCommand('VectorFrameBlend NKPD', "nuke.createNode('VectorFrameBlend')".format(prefixNST), icon="nukepedia_icon.png")
EdgesMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
EdgesMenu.addCommand('FractalBlur NKPD', "nuke.createNode('{}FractalBlur')".format(prefixNST), icon="nukepedia_icon.png")
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
#-
distortMenu = filterMenu.addMenu("Distortions", icon="IDistort.png")
distortMenu.addCommand('Glass FR', "nuke.createNode('{}Glass')".format(prefixNST), icon="nukepedia_icon.png")
distortMenu.addCommand('HeatWave DB', "nuke.createNode('{}HeatWave')".format(prefixNST), icon="HeatWave_Icon.png")
distortMenu.addCommand("X_Distort XM", "nuke.createNode(\"{}X_Distort\")".format(prefixNST), icon="X_Distort.png")
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
#-
X_ToolsMenu = filterMenu.addMenu("X_Tools XM", icon="X_Tools.png")
X_ToolsMenu.addCommand("X_Aton_Volumetrics XM", "nuke.createNode(\"{}X_Aton_Volumetrics\")".format(prefixNST), icon="X_Aton.png")
X_ToolsMenu.addCommand("X_Denoise XM", "nuke.createNode(\"{}X_Denoise\")".format(prefixNST), icon="X_Denoise.png")
X_ToolsMenu.addCommand("X_Sharpen XM", "nuke.createNode(\"{}X_Sharpen\")".format(prefixNST), icon="X_Sharpen.png")
X_ToolsMenu.addCommand("X_Soften XM", "nuke.createNode(\"{}X_Soften\")".format(prefixNST), icon="X_Soften.png")
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
filterMenu.addCommand('BeautifulSkin TL', "nuke.createNode('{}BeautifulSkin')".format(prefixNST), icon="Median.png")
filterMenu.addCommand('BlacksExpon TL', "nuke.createNode('{}BlacksExpon')".format(prefixNST), icon="Toe.png")
filterMenu.addCommand('Halation TL', "nuke.createNode('{}Halation')".format(prefixNST), icon="EdgeBlur.png")
filterMenu.addCommand('HighPass TL', "nuke.createNode('{}HighPass')".format(prefixNST), icon="Invert.png")
filterMenu.addCommand('Diffusion TL', "nuke.createNode('{}Diffusion')".format(prefixNST), icon="Spark.png")
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
filterMenu.addCommand('LightWrapPro TL', "nuke.createNode('{}LightWrapPro')".format(prefixNST), icon="LightWrap.png")
filterMenu.addCommand('bm_Lightwrap BM', "nuke.createNode('{}bm_Lightwrap')".format(prefixNST), icon="bm_Lightwrap_icon.png")
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
filterMenu.addCommand('iConvolve AP', 'nuke.createNode("{}iConvolve")'.format(prefixNST), icon='ap_tools.png')
filterMenu.addCommand('ConvolutionMatrix AG', 'nuke.createNode("{}ConvolutionMatrix")'.format(prefixNST), icon="ColorMatrix.png")
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
filterMenu.addCommand('LightWrapPro TL', "nuke.createNode('{}LightWrapPro')".format(prefixNST), icon="LightWrap.png")
filterMenu.addCommand('bm_Lightwrap BM', "nuke.createNode('{}bm_Lightwrap')".format(prefixNST), icon="bm_Lightwrap_icon.png")
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
filterMenu.addCommand('iConvolve AP', 'nuke.createNode("{}iConvolve")'.format(prefixNST), icon='ap_tools.png')
filterMenu.addCommand('ConvolutionMatrix AG', 'nuke.createNode("{}ConvolutionMatrix")'.format(prefixNST), icon="ColorMatrix.png")
#-
apChromaMenu = filterMenu.addMenu("apChroma Tools AP", icon="apChroma.png") #Add apChroma submenu
apChromaMenu.addCommand('apChroma AP', 'nuke.createNode("{}apChroma")'.format(prefixNST), icon='apChroma.png')
apChromaMenu.addCommand('apChromaMerge AP', 'nuke.createNode("{}apChromaMergeNew")'.format(prefixNST), icon='apChroma.png')
apChromaMenu.addCommand('apChromaBlur AP', 'nuke.createNode("{}apChromaBlurNew")'.format(prefixNST), icon='apChroma.png')
apChromaMenu.addCommand('apChromaTransform AP', 'nuke.createNode("{}apChromaTransformNew")'.format(prefixNST), icon='apChroma.png')
apChromaMenu.addCommand('apChromaUnpremult AP', 'nuke.createNode("{}apChromaUnpremult")'.format(prefixNST), icon='apChroma.png')
apChromaMenu.addCommand('apChromaPremult AP', 'nuke.createNode("{}apChromaPremult")'.format(prefixNST), icon='apChroma.png')
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
nuke.menu('Nodes').addCommand('Filter/PixelSort', "nuke.createNode('PixelSort.gizmo')", icon='PixelSort.png') #Add pixelSort submenu
nuke.menu('Nodes').addCommand('Filter/Hue_Mask', "nuke.createNode('Hue_Mask.gizmo')", icon='Hue_Mask.png') #Add pixelSort submenu
nuke.menu('Nodes').addCommand('Filter/Crypto_Auto', "nuke.createNode('Crypto_Auto.nk')") #Add Crypto_Auto submenu
nuke.menu('Nodes').addCommand('Filter/P_Matte_Auto', "nuke.createNode('P_matte_Auto.nk')") #Add P_Matte_Auto submenu
filterMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
filterMenu.addCommand('Chromatik SPIN', "nuke.createNode('{}Chromatik')".format(prefixNST), icon='spin_tools.png')
filterMenu.addCommand('CatsEyeDefocus NKPD', "nuke.createNode('{}CatsEyeDefocus')".format(prefixNST), icon="nukepedia_icon.png")
filterMenu.addCommand('DefocusSwirlyBokeh NKPD', "nuke.createNode('{}DefocusSwirlyBokeh')".format(prefixNST), icon="nukepedia_icon.png")
filterMenu.addCommand('deHaze NKPD', "nuke.createNode('{}deHaze')".format(prefixNST), icon="nukepedia_icon.png")
filterMenu.addCommand('RankFilter JP', "nuke.createNode('{}RankFilter')".format(prefixNST), icon="Median.png")
filterMenu.addCommand('DeflickerVelocity NKPD', "nuke.createNode('{}DeflickerVelocity')".format(prefixNST), icon="nukepedia_icon.png")
filterMenu.addCommand('FillSampler NKPD', "nuke.createNode('{}FillSampler')".format(prefixNST), icon="nukepedia_icon.png")
filterMenu.addCommand('MECfiller NKPD', "nuke.createNode('{}MECfiller')".format(prefixNST), icon="nukepedia_icon.png")

cprint("| >> -SUCCESS- Loaded: Filter_Tools .....100%")
cprint("+-<FilterTools.printGizmos()>-------------")
cprint("| >> Adding node: ('Filter/ExponGlow')")
cprint("| >> Adding node: ('Filter/Glow_Exponential')")
cprint("| >> Adding node: ('Filter/bm_OpticalGlow')")
cprint("| >> Adding node: ('Filter/ExponBlurSimple')")
cprint("| >> Adding node: ('Filter/DirectionalBlur')")
cprint("| >> Adding node: ('Filter/MotionBlurPaint')")
cprint("| >> Adding node: ('Filter/iBlur')")
cprint("| >> Adding node: ('Filter/WaveletBlur')")
cprint("| >> Adding node: ('Filter/apEdgePush')")
cprint("| >> Adding node: ('Filter/EdgeDetectAlias')")
cprint("| >> Adding node: ('Filter/AntiAliasingFilter')")
cprint("| >> Adding node: ('Filter/ErodeSmooth')")
cprint("| >> Adding node: ('Filter/Edge_RimLight')")
cprint("| >> Adding node: ('Filter/EdgeDetectPRO')")
cprint("| >> Adding node: ('Filter/Erode_Fine')")
cprint("| >> Adding node: ('Filter/Edge_Expand')")
cprint("| >> Adding node: ('Filter/Edge')")
cprint("| >> Adding node: ('Filter/KillOutline')")
cprint("| >> Adding node: ('Filter/ColorSmear')")
cprint("| >> Adding node: ('Filter/EdgeFromAlpha')")
cprint("| >> Adding node: ('Filter/VectorExtendEdge')")
cprint("| >> Adding node: ('Filter/VectorFrameBlend')")
cprint("| >> Adding node: ('Filter/FractalBlur')")
cprint("| >> Adding node: ('Filter/Glass')")
cprint("| >> Adding node: ('Filter/HeatWave')")
cprint("| >> Adding node: ('Filter/X_Distort')")
cprint("| >> Adding node: ('Filter/X_Aton_Volumetrics')")
cprint("| >> Adding node: ('Filter/X_Denoise')")
cprint("| >> Adding node: ('Filter/X_Sharpen')")
cprint("| >> Adding node: ('Filter/X_Soften')")
cprint("| >> Adding node: ('Filter/BeautifulSkin')")
cprint("| >> Adding node: ('Filter/BlacksExpon')")
cprint("| >> Adding node: ('Filter/Halation')")
cprint("| >> Adding node: ('Filter/HighPass')")
cprint("| >> Adding node: ('Filter/Diffusion')")
cprint("| >> Adding node: ('Filter/LightWrapPro')")
cprint("| >> Adding node: ('Filter/bm_Lightwrap')")
cprint("| >> Adding node: ('Filter/iConvolve')")
cprint("| >> Adding node: ('Filter/ConvolutionMatrix')")
cprint("| >> Adding node: ('Filter/apChroma')")
cprint("| >> Adding node: ('Filter/apChromaMerge')")
cprint("| >> Adding node: ('Filter/apChromaBlur')")
cprint("| >> Adding node: ('Filter/apChromaTransform')")
cprint("| >> Adding node: ('Filter/apChromaUnpremult')")
cprint("| >> Adding node: ('Filter/apChromaPremult')")
cprint("| >> Adding node: ('Filter/PixelSort')")
cprint("| >> Adding node: ('Filter/Hue_Mask')")
cprint("| >> Adding node: ('Filter/Crypto_Auto')")
cprint("| >> Adding node: ('Filter/P_Matte_Auto')")
cprint("| >> Adding node: ('Filter/Chromatik')")
cprint("| >> Adding node: ('Filter/CatsEyeDefocus')")
cprint("| >> Adding node: ('Filter/DefocusSwirlyBokeh')")
cprint("| >> Adding node: ('Filter/deHaze')")
cprint("| >> Adding node: ('Filter/RankFilter')")
cprint("| >> Adding node: ('Filter/DeflickerVelocity')")
cprint("| >> Adding node: ('Filter/FillSampler')")
cprint("| >> Adding node: ('Filter/MECfiller')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading OpticalDefocus")

nuke.menu('Nodes').addCommand('Filter/OpticalZDefocus', "nuke.createNode('OpticalZDefocus.gizmo')") #Add OpticalZDefocus

cprint("| >> -SUCCESS- Loaded: OpticalDefocus .....100%")
cprint("+-<OpticalDefocus.printGizmos()>-------------")
cprint("| >> Adding node: ('Filter/OpticalZDefocus')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading TX_Tools")

keyerMenu = m.addMenu('TX_Tools', icon = 'ToolbarKeyer.png', index = 70) #Add TX gizmos
nuke.menu('Nodes').addCommand('TX_Tools/TX_Bloom', "nuke.createNode('TX_Bloom.gizmo')")
nuke.menu('Nodes').addCommand('TX_Tools/TX_Fog', "nuke.createNode('TX_Fog.gizmo')")
nuke.menu('Nodes').addCommand('TX_Tools/TX_HueKeyer', "nuke.createNode('TX_HueKeyer.gizmo')")

cprint("| >> -SUCCESS- Loaded: TX_Tools .....100%")
cprint("+-<TX_Tools.printGizmos()>-------------")
cprint("| >> Adding node: ('TX_Tools/TX_Bloom')")
cprint("| >> Adding node: ('TX_Tools/TX_Fog')")
cprint("| >> Adding node: ('TX_Tools/TX_HueKeyer')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading Keyer_Tools")

keyerMenu = m.addMenu('Keyer', icon = 'ToolbarKeyer.png', index = 70) # Create Keyer Menu
keyerMenu.addCommand('apDespill AP', 'nuke.createNode("{}apDespill_v2")'.format(prefixNST), icon='apDespill.png')
keyerMenu.addCommand('SpillCorrect SPIN', "nuke.createNode('{}Spill_Correct')".format(prefixNST), icon='spin_tools.png')
keyerMenu.addCommand('DespillToColor NKPD', "nuke.createNode('{}DespillToColor')".format(prefixNST), icon="nukepedia_icon.png")
keyerMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
keyerMenu.addCommand('AdditiveKeyerPro TL', "nuke.createNode('{}AdditiveKeyerPro')".format(prefixNST), icon="Bilateral.png")
keyerMenu.addCommand('apScreenClean AP', 'nuke.createNode("{}apeScreenClean")'.format(prefixNST), icon='apScreenClean.png')
keyerMenu.addCommand('apScreenGrow AP', 'nuke.createNode("{}apeScreenGrow")'.format(prefixNST), icon='apScreenGrow.png')
keyerMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
keyerMenu.addCommand('KeyChew NKPD', "nuke.createNode('{}KeyChew')".format(prefixNST), icon="Keyer.png")
keyerMenu.addCommand('LumaKeyer DR', "nuke.createNode('{}LumaKeyer')".format(prefixNST), icon="Keyer.png")

cprint("| >> -SUCCESS- Loaded: Keyer_Tools .....100%")
cprint("+-<KeyerTools.printGizmos()>-------------")
cprint("| >> Adding node: ('Keyer/apDespill_v2')")
cprint("| >> Adding node: ('Keyer/Spill_Correct')")
cprint("| >> Adding node: ('Keyer/DespillToColor')")
cprint("| >> Adding node: ('Keyer/AdditiveKeyerPro')")
cprint("| >> Adding node: ('Keyer/apeScreenClean')")
cprint("| >> Adding node: ('Keyer/apeScreenGrow')")
cprint("| >> Adding node: ('Keyer/KeyChew')")
cprint("| >> Adding node: ('Keyer/LumaKeyer')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading Merge_Tools")

mergeMenu = m.addMenu('Merge', icon = 'ToolbarMerge.png', index = 80) # Create Merge Menu
mergeMenu.addCommand('ContactSheetAuto TL', "nuke.createNode('{}ContactSheetAuto')".format(prefixNST), icon="ContactSheet.png")
mergeMenu.addCommand('KeymixBBox TL', "nuke.createNode('{}KeymixBBox')".format(prefixNST), icon="Keymix.png")
mergeMenu.addCommand('MergeAtmos TL', "nuke.createNode('{}MergeAtmos')".format(prefixNST), icon="PointCloudMesh.png")
mergeMenu.addCommand('MergeBlend TL', "nuke.createNode('{}MergeBlend')".format(prefixNST), icon="Dissolve.png")
mergeMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
mergeMenu.addCommand('MergeAll AP', "nuke.createNode('{}MergeAll')".format(prefixNST), icon="Merge.png")

cprint("| >> -SUCCESS- Loaded: Merge_Tools .....100%")
cprint("+-<MergeTools.printGizmos()>-------------")
cprint("| >> Adding node: ('Merge/ContactSheetAuto')")
cprint("| >> Adding node: ('Merge/KeymixBBox')")
cprint("| >> Adding node: ('Merge/MergeAtmos')")
cprint("| >> Adding node: ('Merge/MergeBlend')")
cprint("| >> Adding node: ('Merge/MergeAll')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading Transform_Tools")

transformMenu = m.addMenu('Transform', icon = 'ToolbarTransform.png', index = 90) # Create Transform Menu
VMTmenu = transformMenu.addMenu('Vector Math Tools VM', icon = 'Math.png') # Add Vector Tools SubMenu
VMT_mathMenu = VMTmenu.addMenu('Math', icon = 'Math.png')
VMT_mathAxisMenu = VMT_mathMenu.addMenu('Axis', icon = 'Axis.png')
VMT_mathMatrixFourMenu = VMT_mathMenu.addMenu('Matrix4', icon = 'Matrix4.png')
VMT_mathVectorTwoMenu = VMT_mathMenu.addMenu('Vector2', icon = 'Vector2.png')
VMT_mathVectorThreeMenu = VMT_mathMenu.addMenu('Vector3', icon = 'Vector3.png')
VMT_mathAxisMenu.addCommand('Invert Axis', "nuke.createNode('{}InvertAxis')".format(prefixNST), icon = 'Axis.png')
VMT_mathAxisMenu.addCommand('Zero Axis', "nuke.createNode('{}ZeroAxis')".format(prefixNST), icon = 'Axis.png')
VMT_mathMatrixFourMenu.addCommand('Invert Matrix4', "nuke.createNode('{}InvertMatrix4')".format(prefixNST), icon = 'InvertMatrix4.png')
VMT_mathMatrixFourMenu.addCommand('Product Matrix4', "nuke.createNode('{}ProductMatrix4')".format(prefixNST), icon = 'ProductMatrix4.png')
VMT_mathMatrixFourMenu.addCommand('Rotate Matrix4', "nuke.createNode('{}RotateMatrix4')".format(prefixNST), icon = 'RotateMatrix4.png')
VMT_mathMatrixFourMenu.addCommand('Scale Matrix4', "nuke.createNode('{}ScaleMatrix4')".format(prefixNST), icon = 'ScaleMatrix4.png')
VMT_mathMatrixFourMenu.addCommand('Transform Matrix4', "nuke.createNode('{}TransformMatrix4')".format(prefixNST), icon = 'TransformMatrix4.png')
VMT_mathMatrixFourMenu.addCommand('Translate Matrix4', "nuke.createNode('{}TranslateMatrix4')".format(prefixNST), icon = 'TranslateMatrix4.png')
VMT_mathMatrixFourMenu.addCommand('Transpose Matrix4', "nuke.createNode('{}TransposeMatrix4')".format(prefixNST), icon = 'TransposeMatrix4.png')
VMT_mathVectorTwoMenu.addCommand('Cross Product Vector2', "nuke.createNode('{}CrossProductVector2')".format(prefixNST), icon = 'CrossProductVector3.png')
VMT_mathVectorTwoMenu.addCommand('Dot Product Vector2', "nuke.createNode('{}DotProductVector2')".format(prefixNST), icon = 'DotProductVector3.png')
VMT_mathVectorTwoMenu.addCommand('Magnitude Vector2', "nuke.createNode('{}MagnitudeVector2')".format(prefixNST), icon = 'MagnitudeVector3.png')
VMT_mathVectorTwoMenu.addCommand('Normalize Vector2', "nuke.createNode('{}NormalizeVector2')".format(prefixNST), icon = 'NormalizeVector3.png')
VMT_mathVectorTwoMenu.addCommand('Rotate Vector2', "nuke.createNode('{}RotateVector2')".format(prefixNST), icon = 'RotateVector3.png')
VMT_mathVectorTwoMenu.addCommand('Transform Vector2', "nuke.createNode('{}TransformVector2')".format(prefixNST), icon = 'TransformVector3.png')
VMT_mathVectorThreeMenu.addCommand('Cross Product Vector3', "nuke.createNode('{}CrossProductVector3')".format(prefixNST), icon = 'CrossProductVector3.png')
VMT_mathVectorThreeMenu.addCommand('Dot Product Vector3', "nuke.createNode('{}DotProductVector3')".format(prefixNST), icon = 'DotProductVector3.png')
VMT_mathVectorThreeMenu.addCommand('Magnitude Vector3', "nuke.createNode('{}MagnitudeVector3')".format(prefixNST), icon = 'MagnitudeVector3.png')
VMT_mathVectorThreeMenu.addCommand('Multiply Vector3 Matrix3', "nuke.createNode('{}MultiplyVector3Matrix3')".format(prefixNST), icon = 'ProductVector3.png')
VMT_mathVectorThreeMenu.addCommand('Normalize Vector3', "nuke.createNode('{}NormalizeVector3')".format(prefixNST), icon = 'NormalizeVector3.png')
VMT_mathVectorThreeMenu.addCommand('Rotate Vector3', "nuke.createNode('{}RotateVector3')".format(prefixNST), icon = 'RotateVector3.png')
VMT_mathVectorThreeMenu.addCommand('Transform Vector3', "nuke.createNode('{}TransformVector3')".format(prefixNST), icon = 'TransformVector3.png')
#-
VMT_generateMenu = VMTmenu.addMenu('Generate', icon = 'IdentityMatrix4.png')
VMT_generateMenu.addCommand('Generate Matrix4', "nuke.createNode('{}GenerateMatrix4')".format(prefixNST), icon = 'IdentityMatrix4.png')
VMT_generateMenu.addCommand('Generate STMap', "nuke.createNode('{}GenerateSTMap')".format(prefixNST), icon = 'AG_UVMap.png')
#-
VMT_convertMenu = VMTmenu.addMenu('Convert', icon = 'ProductVector3.png')
VMT_convertMenu.addCommand('Luma To Vector3', "nuke.createNode('{}LumaToVector3')".format(prefixNST), icon = 'vectorToolsBW.png')
VMT_convertMenu.addCommand('STMap To Vector2', "nuke.createNode('{}STMapToVector2')".format(prefixNST), icon = 'Vector2.png')
VMT_convertMenu.addCommand('Vector2 To STMap', "nuke.createNode('{}Vector2ToSTMap')".format(prefixNST), icon = 'AG_UVMap.png')
VMT_convertMenu.addCommand('Vector3 To Matrix4', "nuke.createNode('{}Vector3ToMatrix4')".format(prefixNST), icon = 'ProductVector3.png')
transformMenu.addCommand('vector3DMathExpression EL', "nuke.createNode('{}vector3DMathExpression')".format(prefixNST), icon = 'vectorTools.png')
transformMenu.addCommand('Vectors_Direction EL', "nuke.createNode('{}Vectors_Direction')".format(prefixNST), icon = 'vectorTools.png')
transformMenu.addCommand('Vectors_to_Degrees EL', "nuke.createNode('{}Vectors_to_Degrees')".format(prefixNST), icon = 'vectorTools.png')

# Add VectorTracker python file
try:
    nuke.load('{}VectorTracker.py'.format(prefixNST))
    transformMenu.addCommand('VectorTracker NKPD', "nuke.createNode('{}VectorTracker.gizmo')".format(prefixNST), icon = 'vectorTools.png')
except:
    cprint("Could not load VectorTracker.py")
    pass

transformMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
transformMenu.addCommand('AutoCropTool TL', "nuke.createNode('{}AutoCropTool')".format(prefixNST), icon="AutoCrop.png")
transformMenu.addCommand('BBoxToFormat TL', "nuke.createNode('{}BBoxToFormat')".format(prefixNST), icon="Rectangle.png")
transformMenu.addCommand('ImagePlane3D TL', "nuke.createNode('{}ImagePlane3D')".format(prefixNST), icon="Card.png")
transformMenu.addCommand('Matrix_Inverse TL', "nuke.createNode('{}Matrix4x4_Inverse')".format(prefixNST), icon="ColorMatrix.png")
transformMenu.addCommand('Matrix4x4Math TL', "nuke.createNode('{}Matrix4x4Math')".format(prefixNST), icon="ColorMath.png")
transformMenu.addCommand('MirrorBorder TL', "nuke.createNode('{}MirrorBorder')".format(prefixNST), icon="AdjBBox.png")
transformMenu.addCommand('TransformCutOut TL', "nuke.createNode('{}TransformCutOut')".format(prefixNST), icon="MergeOut.png")
transformMenu.addCommand('iMorph AP', "nuke.createNode('{}iMorph')".format(prefixNST), icon="VectorDistort.png")
transformMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
transformMenu.addCommand('RP_Reformat MJT', "nuke.createNode('{}RP_Reformat')".format(prefixNST), icon='RP_Reformat.png')
transformMenu.addCommand('InverseMatrix3x3 MJT', "nuke.createNode('{}InverseMatrix33')".format(prefixNST), icon='iMatrix33.png')
transformMenu.addCommand('InverseMatrix4x4 MJT', "nuke.createNode('{}InverseMatrix44')".format(prefixNST), icon='iMatrix44.png')
transformMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
transformMenu.addCommand('CardToTrack AK', "nuke.createNode('{}CardToTrack')".format(prefixNST), icon='Card.png')
transformMenu.addCommand('CProject AK', "nuke.createNode('{}CProject')".format(prefixNST), icon='CornerPin.png')
transformMenu.addCommand('TProject AK', "nuke.createNode('{}TProject')".format(prefixNST), icon='Transform.png')
transformMenu.addCommand("StickIt MHD", "nuke.createNode('{}h_stickit')".format(prefixNST), icon="h_stickit.png")
transformMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
transformMenu.addCommand('TransformMatrix AG', "nuke.createNode('{}TransformMatrix')".format(prefixNST), icon="Transform.png")
transformMenu.addCommand('CornerPin2D_Matrix AG', "nuke.createNode('{}CornerPin2D_Matrix')".format(prefixNST), icon="CornerPin.png")
transformMenu.addCommand('RotoPaintTransform AG', "nuke.createNode('{}RotoPaintTransform')".format(prefixNST), icon="RotoPaint.png")
transformMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
transformMenu.addCommand('IIDistort EL', "nuke.createNode('{}IIDistort')".format(prefixNST), icon="nukepedia_icon.png")
transformMenu.addCommand('bm_CameraShake BM', "nuke.createNode('{}bm_CameraShake')".format(prefixNST), icon="bm_CameraShake_icon.png")
transformMenu.addCommand('ITransform FR', "nuke.createNode('{}ITransformU')".format(prefixNST), icon="STMap.png")
transformMenu.addCommand('MorphDissolve SPIN', "nuke.createNode('{}MorphDissolve')".format(prefixNST), icon="spin_tools.png")
transformMenu.addCommand('RotoCentroid NKPD', "nuke.createNode('{}RotoCentroid')".format(prefixNST), icon="nukepedia_icon.png")
transformMenu.addCommand('STmapInverse NKPD', "nuke.createNode('{}STmapInverse')".format(prefixNST), icon="nukepedia_icon.png")
transformMenu.addCommand('TransformMix NKPD', "nuke.createNode('{}TransformMix')".format(prefixNST), icon="Transform.png")
transformMenu.addCommand('PlanarProjection NKPD', "nuke.createNode('{}PlanarProjection')".format(prefixNST), icon="nukepedia_icon.png")
transformMenu.addCommand('Reconcile3DFast DR', "nuke.createNode('{}Reconcile3DFast')".format(prefixNST), icon="Reconcile3D.png")

cprint("| >> -SUCCESS- Loaded: Transform_Tools .....100%")
cprint("+-<TransformTools.printGizmos()>-------------")
cprint("| >> Adding node: ('Transform/Vector Math Tools')")
cprint("| >> Adding node: ('Transform/VectorTracker')")
cprint("| >> Adding node: ('Transform/InvertAxis')")
cprint("| >> Adding node: ('Transform/ZeroAxis')")
cprint("| >> Adding node: ('Transform/InvertMatrix4')")
cprint("| >> Adding node: ('Transform/ProductMatrix4')")
cprint("| >> Adding node: ('Transform/RotateMatrix4')")
cprint("| >> Adding node: ('Transform/ScaleMatrix4')")
cprint("| >> Adding node: ('Transform/TransformMatrix4')")
cprint("| >> Adding node: ('Transform/TranslateMatrix4')")
cprint("| >> Adding node: ('Transform/TransposeMatrix4')")
cprint("| >> Adding node: ('Transform/CrossProductVector2')")
cprint("| >> Adding node: ('Transform/DotProductVector2')")
cprint("| >> Adding node: ('Transform/MagnitudeVector2')")
cprint("| >> Adding node: ('Transform/NormalizeVector2')")
cprint("| >> Adding node: ('Transform/RotateVector2')")
cprint("| >> Adding node: ('Transform/TransformVector2')")
cprint("| >> Adding node: ('Transform/CrossProductVector3')")
cprint("| >> Adding node: ('Transform/DotProductVector3')")
cprint("| >> Adding node: ('Transform/MagnitudeVector3')")
cprint("| >> Adding node: ('Transform/MultiplyVector3Matrix3')")
cprint("| >> Adding node: ('Transform/NormalizeVector3')")
cprint("| >> Adding node: ('Transform/RotateVector3')")
cprint("| >> Adding node: ('Transform/TransformVector3')")
cprint("| >> Adding node: ('Transform/GenerateMatrix4')")
cprint("| >> Adding node: ('Transform/GenerateSTMap')")
cprint("| >> Adding node: ('Transform/LumaToVector3')")
cprint("| >> Adding node: ('Transform/STMapToVector2')")
cprint("| >> Adding node: ('Transform/Vector2ToSTMap')")
cprint("| >> Adding node: ('Transform/Vector3ToMatrix4')")
cprint("| >> Adding node: ('Transform/AutoCropTool')")
cprint("| >> Adding node: ('Transform/BBoxToFormat')")
cprint("| >> Adding node: ('Transform/ImagePlane3D')")
cprint("| >> Adding node: ('Transform/Matrix4x4_Inverse')")
cprint("| >> Adding node: ('Transform/Matrix4x4Math')")
cprint("| >> Adding node: ('Transform/MirrorBorder')")
cprint("| >> Adding node: ('Transform/TransformCutOut')")
cprint("| >> Adding node: ('Transform/iMorph')")
cprint("| >> Adding node: ('Transform/RP_Reformat')")
cprint("| >> Adding node: ('Transform/InverseMatrix3x3')")
cprint("| >> Adding node: ('Transform/InverseMatrix4x4')")
cprint("| >> Adding node: ('Transform/CardToTrack')")
cprint("| >> Adding node: ('Transform/CProject')")
cprint("| >> Adding node: ('Transform/TProject')")
cprint("| >> Adding node: ('Transform/StickIt')")
cprint("| >> Adding node: ('Transform/TransformMatrix')")
cprint("| >> Adding node: ('Transform/CornerPin2D_Matrix')")
cprint("| >> Adding node: ('Transform/RotoPaintTransform')")
cprint("| >> Adding node: ('Transform/IIDistort')")
cprint("| >> Adding node: ('Transform/bm_CameraShake')")
cprint("| >> Adding node: ('Transform/ITransform')")
cprint("| >> Adding node: ('Transform/MorphDissolve')")
cprint("| >> Adding node: ('Transform/RotoCentroid')")
cprint("| >> Adding node: ('Transform/STmapInverse')")
cprint("| >> Adding node: ('Transform/TransformMix')")
cprint("| >> Adding node: ('Transform/PlanarProjection')")
cprint("| >> Adding node: ('Transform/Reconcile3DFast')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading 3D_Tools")

ThreeDMenu = m.addMenu('3D', icon = 'Toolbar3D.png', index = 100) # Create 3D Menu
ThreeDMenu.addCommand('aPCard AP', 'nuke.createNode("{}aPCard")'.format(prefixNST), icon='ap_tools.png')
ThreeDMenu.addCommand('DummyCam', 'nuke.createNode("{}DummyCam")'.format(prefixNST), icon='DummyCam.png')
ThreeDMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
ThreeDMenu.addCommand('mScatterGeo MJT', 'nuke.createNode("{}mScatterGeo")'.format(prefixNST), icon='mScatterGeo.png')
ThreeDMenu.addCommand('GeoToPoints MHD', "nuke.createNode('{}GeoToPoints')".format(prefixNST), icon="nukepedia_icon.png")
ThreeDMenu.addCommand('origami MJT', 'nuke.createNode("{}origami")'.format(prefixNST), icon='origami.png')
ThreeDMenu.addCommand('RayDeepAO MJT', 'nuke.createNode("{}RayDeepAO")'.format(prefixNST), icon='RayDeepAO.png')
ThreeDMenu.addCommand('SceneDepthCalculator MJT', 'nuke.createNode("{}SceneDepthCalculator")'.format(prefixNST), icon='SceneDepthCalculator.png')
ThreeDMenu.addCommand('SSMesh MJT', 'nuke.createNode("{}SSMesh")'.format(prefixNST), icon='SSMesh.png')
ThreeDMenu.addCommand('Unify3DCoordinate MJT', 'nuke.createNode("{}Unify3DCoordinate")'.format(prefixNST), icon='Unify3DCoordinate.png')
ThreeDMenu.addCommand('UVEditor MJT', 'nuke.createNode("{}UVEditor")'.format(prefixNST), icon='UVEditor.png')
ThreeDMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
ThreeDMenu.addCommand('Distance3D NKPD', "nuke.createNode('{}Distance3D')".format(prefixNST), icon="nukepedia_icon.png")
ThreeDMenu.addCommand('DistanceBetween_CS NKPD', "nuke.createNode('{}DistanceBetween_CS')".format(prefixNST), icon="nukepedia_icon.png")
ThreeDMenu.addCommand('Lightning3D EL', "nuke.createNode('{}Lightning3D')".format(prefixNST), icon="nukepedia_icon.png")
ThreeDMenu.addCommand('Noise3DTexture NKPD', "nuke.createNode('{}Noise3DTexture')".format(prefixNST), icon="noise3dicon.png")
ThreeDMenu.addCommand('GodRaysProjector CF', "nuke.createNode('{}GodRaysProjector')".format(prefixNST), icon="VolumeRays.png")

cprint("| >> -SUCCESS- Loaded: 3D_Tools .....100%")
cprint("+-<ThreeDTools.printGizmos()>-------------")
cprint("| >> Adding node: ('3D/aPCard')")
cprint("| >> Adding node: ('3D/DummyCam')")
cprint("| >> Adding node: ('3D/mScatterGeo')")
cprint("| >> Adding node: ('3D/GeoToPoints')")
cprint("| >> Adding node: ('3D/origami')")
cprint("| >> Adding node: ('3D/RayDeepAO')")
cprint("| >> Adding node: ('3D/SceneDepthCalculator')")
cprint("| >> Adding node: ('3D/SSMesh')")
cprint("| >> Adding node: ('3D/Unify3DCoordinate')")
cprint("| >> Adding node: ('3D/UVEditor')")
cprint("| >> Adding node: ('3D/Distance3D')")
cprint("| >> Adding node: ('3D/DistanceBetween_CS')")
cprint("| >> Adding node: ('3D/Lightning3D')")
cprint("| >> Adding node: ('3D/Noise3DTexture')")
cprint("| >> Adding node: ('3D/GodRaysProjector')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading Particles_Tools")

particlesMenu = m.addMenu('Particles', icon = 'ToolbarParticles.png', index = 110) # Create Paricles Menu
particlesMenu.addCommand('waterSchmutz DR', "nuke.createNode('{}waterSchmutz')".format(prefixNST), icon="WaterLens.png")
particlesMenu.addCommand('RainMaker MR', "nuke.createNode('{}RainMaker')".format(prefixNST), icon="ParticleDrag.png")
particlesMenu.addCommand('Sparky DB', "nuke.createNode('{}Sparky')".format(prefixNST), icon="Sparky.png")
particlesMenu.addCommand('ParticleLights MHD', "nuke.createNode('{}ParticleLights')".format(prefixNST), icon="ToolbarParticles.png")
particlesMenu.addCommand('ParticleKiller NKPD', "nuke.createNode('{}ParticleKiller')".format(prefixNST), icon="ToolbarParticles.png")

cprint("| >> -SUCCESS- Loaded: Particles_Tools .....100%")
cprint("+-<ParticlesTools.printGizmos()>-------------")
cprint("| >> Adding node: ('Particles/waterSchmutz')")
cprint("| >> Adding node: ('Particles/RainMaker')")
cprint("| >> Adding node: ('Particles/Sparky')")
cprint("| >> Adding node: ('Particles/ParticleLights')")
cprint("| >> Adding node: ('Particles/ParticleKiller')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading Deep_Tools")

deepMenu = m.addMenu('Deep', icon = 'ToolbarDeep.png', index = 120) # Create Deep Menu
deep2VP_suite = deepMenu.addMenu("Deep2VP Suite MJT", icon='Deep2VP.png')
deep2VP_suite.addCommand('Deep2VP MJT', "nuke.createNode('{}Deep2VP')".format(prefixNST), icon="Deep2VP.png")
deep2VP_suite.addCommand('DVPColorCorrect MJT', "nuke.createNode('{}DVPColorCorrect')".format(prefixNST), icon="DVPColorCorrect.png")
deep2VP_suite.addCommand('DVPortal MJT', "nuke.createNode('{}DVPortal')".format(prefixNST), icon="DVPortal.png")
deep2VP_suite.addCommand('DVPToImage MJT', "nuke.createNode('{}DVPToImage')".format(prefixNST), icon="DVPToImage.png")
deep2VP_suite.addSeparator() #--------------------------------------------------------------------------------------------------------
deep2VP_suite.addCommand('DVPfresnel MJT', "nuke.createNode('{}DVPfresnel')".format(prefixNST), icon="DVPfresnel.png")
deep2VP_suite.addCommand('DVPrelight MJT', "nuke.createNode('{}DVPrelight')".format(prefixNST), icon="DVPrelight.png")
deep2VP_suite.addCommand('DVPrelightPT MJT', "nuke.createNode('{}DVPrelightPT')".format(prefixNST), icon="DVPrelightPT.png")
deep2VP_suite.addCommand('DVPscene MJT', "nuke.createNode('{}DVPscene')".format(prefixNST), icon="DVPscene.png")
deep2VP_suite.addCommand('DVPsetLight MJT', "nuke.createNode('{}DVPsetLight')".format(prefixNST), icon="DVPsetLight.png")
deep2VP_suite.addSeparator() #--------------------------------------------------------------------------------------------------------
deep2VP_suite.addCommand('DVPattern MJT', "nuke.createNode('{}DVPattern')".format(prefixNST), icon="DVPattern.png")
deep2VP_suite.addCommand('DVPmatte MJT', "nuke.createNode('{}DVPmatte')".format(prefixNST), icon="DVPmatte.png")
deep2VP_suite.addCommand('DVProjection MJT', "nuke.createNode('{}DVProjection')".format(prefixNST), icon="DVProjection.png")
deep2VP_suite.addSeparator() #--------------------------------------------------------------------------------------------------------
deep2VP_suite.addCommand('DVP_ToonShader MJT', "nuke.createNode('{}DVP_ToonShader')".format(prefixNST), icon="DVP_ToonShader.png")
deep2VP_suite.addCommand('DVP_Shader MJT', "nuke.createNode('{}DVP_Shader')".format(prefixNST), icon="DVP_Shader.png")
deepMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
deepMenu.addCommand('DeepBoolean MJT', "nuke.createNode('{}DeepBoolean')".format(prefixNST), icon="DeepBoolean.png")
deepMenu.addCommand('DeepFromPosition MJT', "nuke.createNode('{}DeepFromPosition')".format(prefixNST), icon="DeepFromPosition.png")
deepMenu.addCommand('DeepSampleCount MJT', "nuke.createNode('{}DeepSampleCount')".format(prefixNST), icon="DeepSampleCount.png")
deepMenu.addCommand('DeepSer MJT', "nuke.createNode('{}DeepSer')".format(prefixNST), icon="DeepSer.png")
deepMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
deepMenu.addCommand('DeepFromDepth AG', "nuke.createNode('{}DeepFromDepth')".format(prefixNST), icon="DeepRecolor.png")
deepMenu.addCommand('DeepToPosition TL', "nuke.createNode('{}DeepToPosition')".format(prefixNST), icon="Deep2VPosition.png")
deepMenu.addCommand('DeepRecolorMatte TL', "nuke.createNode('{}DeepRecolorMatte')".format(prefixNST), icon="DeepRecolor.png")
deepMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
deepMenu.addCommand('DeepMerge_Advanced BM', "nuke.createNode('{}DeepMerge_Advanced')".format(prefixNST), icon="DeepMerge.png")
deepMenu.addCommand('DeepCropSoft NKPD', "nuke.createNode('{}DeepCropSoft')".format(prefixNST), icon="DeepCrop.png")
deepMenu.addCommand('DeepKeyMix NKPD', "nuke.createNode('{}DeepKeyMix')".format(prefixNST), icon="DeepMerge.png")
deepMenu.addCommand('DeepHoldoutSmoother NKPD', "nuke.createNode('{}DeepHoldoutSmoother')".format(prefixNST), icon="DeepHoldout.png")
deepMenu.addCommand('DeepCopyBBox NKPD', "nuke.createNode('{}DeepCopyBBox')".format(prefixNST), icon="DeepMerge.png")

cprint("| >> -SUCCESS- Loaded: Deep_Tools .....100%")
cprint("+-<DeepTools.printGizmos()>-------------")
cprint("| >> Adding node: ('Deep/Deep2VP')")
cprint("| >> Adding node: ('Deep/DVPColorCorrect')")
cprint("| >> Adding node: ('Deep/DVPortal')")
cprint("| >> Adding node: ('Deep/DVPToImage')")
cprint("| >> Adding node: ('Deep/DVPfresnel')")
cprint("| >> Adding node: ('Deep/DVPrelight')")
cprint("| >> Adding node: ('Deep/DVPrelightPT')")
cprint("| >> Adding node: ('Deep/DVPscene')")
cprint("| >> Adding node: ('Deep/DVPsetLight')")
cprint("| >> Adding node: ('Deep/DVPattern')")
cprint("| >> Adding node: ('Deep/DVPmatte')")
cprint("| >> Adding node: ('Deep/DVProjection')")
cprint("| >> Adding node: ('Deep/DVP_ToonShader')")
cprint("| >> Adding node: ('Deep/DVP_Shader')")
cprint("| >> Adding node: ('Deep/DeepBoolean')")
cprint("| >> Adding node: ('Deep/DeepFromPosition')")
cprint("| >> Adding node: ('Deep/DeepSampleCount')")
cprint("| >> Adding node: ('Deep/DeepSer')")
cprint("| >> Adding node: ('Deep/DeepFromDepth')")
cprint("| >> Adding node: ('Deep/DeepToPosition')")
cprint("| >> Adding node: ('Deep/DeepRecolorMatte')")
cprint("| >> Adding node: ('Deep/DeepMerge_Advanced')")
cprint("| >> Adding node: ('Deep/DeepCropSoft')")
cprint("| >> Adding node: ('Deep/DeepKeyMix')")
cprint("| >> Adding node: ('Deep/DeepHoldoutSmoother')")
cprint("| >> Adding node: ('Deep/DeepCopyBBox')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading CG_Tools")

cgMenu = m.addMenu('CG', icon = 'RenderManShader.png', index = 130) # Create CG Menu
cgMenu.addCommand('UV Mapper TL', "nuke.createNode('{}UV_Mapper')".format(prefixNST), icon="Tile.png")
cgMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
PNZsuite = cgMenu.addMenu('PNZsuite MJT', icon = 'ConvertPNZ.png')
PNZsuite.addCommand('ConvertPNZ MJT', 'nuke.createNode("{}ConvertPNZ")'.format(prefixNST), icon='ConvertPNZ.png')
PNZsuite.addCommand('P2N MJT', 'nuke.createNode("{}P2N")'.format(prefixNST), icon='P2N.png')
PNZsuite.addCommand('P2Z MJT', 'nuke.createNode("{}P2Z")'.format(prefixNST), icon='P2Z.png')
PNZsuite.addCommand('Z2N MJT', 'nuke.createNode("{}Z2N")'.format(prefixNST), icon='Z2N.png')
PNZsuite.addCommand('Z2P MJT', 'nuke.createNode("{}Z2P")'.format(prefixNST), icon='Z2P.png')
PosToolkit = cgMenu.addMenu('PosToolkit MJT', icon = 'PosMatte_MJ.png')
#-
PosToolkit.addCommand('PosMatte MJT', 'nuke.createNode("{}PosMatte_MJ")'.format(prefixNST), icon='PosMatte_MJ.png')
PosToolkit.addCommand('PosPattern MJT', 'nuke.createNode("{}PosPattern_MJ")'.format(prefixNST), icon='PosPattern_MJ.png')
PosToolkit.addCommand('PosProjection MJT', 'nuke.createNode("{}PosProjection_MJ")'.format(prefixNST), icon='PosProjection_MJ.png')
cgMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
cgMenu.addCommand('Noise_3D SPIN', 'nuke.createNode("{}Noise3D_spin")'.format(prefixNST), icon='spin_tools.png')
cgMenu.addCommand('Noise4D MHD', 'nuke.nodePaste("{}/nk_files/{}Noise4D.nk")'.format(NST_FolderPath, prefixNST), icon='Noise.png')
cgMenu.addCommand('Relight_Simple SPIN', 'nuke.createNode("{}Relight_Simple")'.format(prefixNST), icon='spin_tools.png')
cgMenu.addCommand('ReProject_3D SPIN', 'nuke.createNode("{}ReProject_3D")'.format(prefixNST), icon='spin_tools.png')
cgMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
cgMenu.addCommand('C44Kernel AP', 'nuke.createNode("{}C44Kernel")'.format(prefixNST), icon='C44Kernel.png')
cgMenu.addCommand('apDirLight AP', 'nuke.createNode("{}apDirLight")'.format(prefixNST), icon='apDirLight.png')
cgMenu.addCommand('apFresnel AP', 'nuke.createNode("{}apFresnel")'.format(prefixNST), icon='ap_tools.png')
cgMenu.addCommand('CameraNormals NKPD', "nuke.createNode('{}CameraNormals')".format(prefixNST), icon="Camera.png")
cgMenu.addCommand('NormalsRotate NKPD', "nuke.createNode('{}NormalsRotate')".format(prefixNST), icon="SpotLight.png")
cgMenu.addCommand('Relight_bb NKPD', "nuke.createNode('{}Relight_bb')".format(prefixNST), icon="SpotLight.png")
cgMenu.addCommand('EnvReflect_bb NKPD', "nuke.createNode('{}EnvReflect_BB')".format(prefixNST), icon="Sphere.png")
cgMenu.addCommand('N_Reflection NKPD', "nuke.createNode('{}N_Reflection')".format(prefixNST), icon="Sphere.png")
cgMenu.addCommand('SimpleSSS MHD', "nuke.createNode('{}SimpleSSS')".format(prefixNST), icon="Toolbar3D.png")
cgMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
cgMenu.addCommand('aPmatte AP', 'nuke.createNode("{}aPMatte_v2")'.format(prefixNST), icon='aPmatte.png')
cgMenu.addCommand('P_Ramp NKPD', "nuke.createNode('{}F_P_Ramp')".format(prefixNST), icon="F_pramp.png")
cgMenu.addCommand('P_Project NKPD', "nuke.createNode('{}F_P_Project')".format(prefixNST), icon="F_pproject.png")
cgMenu.addCommand('Glue_P LS', "nuke.createNode('{}GlueP')".format(prefixNST), icon="PosProjection_MJ.png")
cgMenu.addCommand('P_Noise_Advanced NKPD', "nuke.createNode('{}P_Noise_Advanced')".format(prefixNST), icon="Noise.png")

cprint("| >> -SUCCESS- Loaded: CG_Tools .....100%")
cprint("+-<CGTools.printGizmos()>-------------")
cprint("| >> Adding node: ('CG/UV Mapper')")
cprint("| >> Adding node: ('CG/PNZsuite/ConvertPNZ')")
cprint("| >> Adding node: ('CG/PNZsuite/P2N')")
cprint("| >> Adding node: ('CG/PNZsuite/P2Z')")
cprint("| >> Adding node: ('CG/PNZsuite/Z2N')")
cprint("| >> Adding node: ('CG/PNZsuite/Z2P')")
cprint("| >> Adding node: ('CG/PosToolkit/PosMatte')")
cprint("| >> Adding node: ('CG/PosToolkit/PosPattern')")
cprint("| >> Adding node: ('CG/PosToolkit/PosProjection')")
cprint("| >> Adding node: ('CG/Noise_3D')")
cprint("| >> Adding node: ('CG/Noise4D')")
cprint("| >> Adding node: ('CG/Relight_Simple')")
cprint("| >> Adding node: ('CG/ReProject_3D')")
cprint("| >> Adding node: ('CG/C44Kernel')")
cprint("| >> Adding node: ('CG/apDirLight')")
cprint("| >> Adding node: ('CG/apFresnel')")
cprint("| >> Adding node: ('CG/CameraNormals')")
cprint("| >> Adding node: ('CG/NormalsRotate')")
cprint("| >> Adding node: ('CG/Relight_bb')")
cprint("| >> Adding node: ('CG/EnvReflect_bb')")
cprint("| >> Adding node: ('CG/N_Reflection')")
cprint("| >> Adding node: ('CG/SimpleSSS')")
cprint("| >> Adding node: ('CG/aPmatte')")
cprint("| >> Adding node: ('CG/P_Ramp')")
cprint("| >> Adding node: ('CG/P_Project')")
cprint("| >> Adding node: ('CG/Glue_P')")
cprint("| >> Adding node: ('CG/P_Noise_Advanced')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading Curves_Tools")

# Create Curves Menu
curvesMenu = m.addMenu('Curves', icon = 'ParticleCurve.png', index = 140)
waveMachineMenu = curvesMenu.addMenu("Wave Machine FL", icon='waveMachine.png')
waveMachineMenu.addCommand('WaveMaker FL', "nuke.createNode('{}waveMaker')".format(prefixNST), icon="waveMaker.png")
waveMachineMenu.addCommand('WaveCustom FL', "nuke.createNode('{}waveCustom')".format(prefixNST), icon="waveCustom.png")
waveMachineMenu.addCommand('WaveGrade FL', "nuke.createNode('{}waveGrade')".format(prefixNST), icon="waveGrade.png")
waveMachineMenu.addCommand('WaveRetime FL', "nuke.createNode('{}waveRetime')".format(prefixNST), icon="waveRetime.png")
waveMachineMenu.addCommand('WaveMerge FL', "nuke.createNode('{}waveMerge')".format(prefixNST), icon="waveMerge.png")
curvesMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
curvesMenu.addCommand('Randomizer TL', "nuke.createNode('{}Randomizer')".format(prefixNST), icon="RenderMan.png")
curvesMenu.addCommand('AnimationCurve AG', "nuke.createNode('{}AnimationCurve')".format(prefixNST), icon="nukepedia_icon.png")
curvesMenu.addCommand('bm_CurveRemapper BM', "nuke.createNode('{}bm_CurveRemapper')".format(prefixNST), icon="bm_CurveRemapper_icon.png")
curvesMenu.addCommand('bm_NoiseGen BM', "nuke.createNode('{}bm_NoiseGen')".format(prefixNST), icon="bm_NoiseGen_icon.png")

cprint("| >> -SUCCESS- Loaded: Curves_Tools .....100%")
cprint("+-<CurvesTools.printGizmos()>-------------")
cprint("| >> Adding node: ('Curves/Wave Machine/WaveMaker')")
cprint("| >> Adding node: ('Curves/Wave Machine/WaveCustom')")
cprint("| >> Adding node: ('Curves/Wave Machine/WaveGrade')")
cprint("| >> Adding node: ('Curves/Wave Machine/WaveRetime')")
cprint("| >> Adding node: ('Curves/Wave Machine/WaveMerge')")
cprint("| >> Adding node: ('Curves/Randomizer')")
cprint("| >> Adding node: ('Curves/AnimationCurve')")
cprint("| >> Adding node: ('Curves/bm_CurveRemapper')")
cprint("| >> Adding node: ('Curves/bm_NoiseGen')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading Utilities_Tools")

utilitiesMenu = m.addMenu('Utilities', icon = 'Modify.png', index = 150) # Create Utilities Menu
utilitiesMenu.addCommand('GUI Switch TL', "nuke.createNode('{}GUI_Switch')".format(prefixNST), icon="Switch.png")
utilitiesMenu.addCommand('NAN INF Killer TL', "nuke.createNode('{}NAN_INF_Killer')".format(prefixNST), icon="Assert.png")
utilitiesMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
utilitiesMenu.addCommand('apViewerBlocker AP', 'nuke.createNode("{}apViewerBlocker")'.format(prefixNST), icon='ap_tools.png')
utilitiesMenu.addCommand('Python_and_TCL AG', 'nuke.createNode("{}Python_and_TCL")'.format(prefixNST), icon="nukepedia_icon.png")
utilitiesMenu.addCommand('RotoQC NKPD', "nuke.createNode('{}RotoQC')".format(prefixNST), icon="Roto.png")
utilitiesMenu.addCommand('bm_MatteCheck BM', "nuke.createNode('{}bm_MatteCheck')".format(prefixNST), icon="bm_MatteCheck_icon.png")
utilitiesMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
utilitiesMenu.addCommand('viewer_render MJT', 'nuke.createNode("{}viewer_render")'.format(prefixNST), icon='viewer_render.png')
utilitiesMenu.addCommand('NukeZ MJT', 'nuke.createNode("{}NukeZ")'.format(prefixNST), icon='NukeZ.png')
utilitiesMenu.addCommand('Pyclopedia MJT', 'nuke.createNode("{}Pyclopedia")'.format(prefixNST), icon='Pyclopedia.png')

cprint("| >> -SUCCESS- Loaded: Utilities_Tools .....100%")
cprint("+-<UtilitiesTools.printGizmos()>-------------")
cprint("| >> Adding node: ('Utilities/GUI Switch')")
cprint("| >> Adding node: ('Utilities/NAN INF Killer')")
cprint("| >> Adding node: ('Utilities/apViewerBlocker')")
cprint("| >> Adding node: ('Utilities/Python_and_TCL')")
cprint("| >> Adding node: ('Utilities/RotoQC')")
cprint("| >> Adding node: ('Utilities/bm_MatteCheck')")
cprint("| >> Adding node: ('Utilities/viewer_render')")
cprint("| >> Adding node: ('Utilities/NukeZ')")
cprint("| >> Adding node: ('Utilities/Pyclopedia')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading Templates_Tools")
templatesMenu = m.addMenu('Templates', icon = 'PointsTo3D.png', index = 200) # Create Templates Menu
templatesMenu.addCommand('Advanced Keying Template Stamps TL', "nuke.nodePaste('{}/nk_files/{}AdvancedKeyingTemplate_Stamps.nk')".format(NST_FolderPath, prefixNST), icon="Keyer.png")
templatesMenu.addCommand('Advanced Keying Template TL', "nuke.nodePaste('{}/nk_files/{}AdvancedKeyingTemplate.nk')".format(NST_FolderPath, prefixNST), icon="Keyer.png")
templatesMenu.addCommand('STMap Keyer Setup EL', "nuke.nodePaste('{}/nk_files/{}STMap_Keying_Setup.nk')".format(NST_FolderPath, prefixNST), icon="HueKeyer.png")

cprint("| >> -SUCCESS- Loaded: Templates_Tools .....100%")
cprint("+-<TemplatesTools.printGizmos()>-------------")
cprint("| >> Adding node: ('Templates/Advanced Keying Template Stamps')")
cprint("| >> Adding node: ('Templates/Advanced Keying Template')")
cprint("| >> Adding node: ('Templates/STMap Keyer Setup')")
cprint("+-----------------------------------------------------")

templatesMenu.addSeparator() #--------------------------------------------------------------------------------------------------------
############################################################################################################
############################################################################################################
#-Gizmo Demo Scripts
cprint("| Loading GizmoDemo_Tools")

gizmoDemoMenu = templatesMenu.addMenu("Gizmo Demo Scripts", icon='Group.png')
gizmoDemoMenu.addCommand('WaterLens Demo MJT', "NST_helper.filepathCreateNode('{}/nk_files/{}WaterLens_sampleScript.nk')".format(NST_FolderPath, prefixNST), icon="WaterLens.png")
gizmoDemoMenu.addCommand('SSMesh Demo MJT', "nuke.nodePaste('{}/nk_files/{}SSMesh_demo.nk')".format(NST_FolderPath, prefixNST), icon="SSMesh.png")
gizmoDemoMenu.addCommand('UVEditor Demo MJT', "nuke.nodePaste('{}/nk_files/{}UVEditor_demo_clean.nk')".format(NST_FolderPath, prefixNST), icon="UVEditor.png")
gizmoDemoMenu.addCommand('Sparky Demo DB', "nuke.nodePaste('{}/nk_files/{}SparkyExampleScene.nk')".format(NST_FolderPath, prefixNST), icon="Sparky.png")
gizmoDemoMenu.addCommand('ParticleLights Demo MHD', "nuke.nodePaste('{}/nk_files/{}ParticleLights_ExampleScript.nk')".format(NST_FolderPath, prefixNST), icon="ToolbarParticles.png")
gizmoDemoMenu.addCommand("X_Aton Volumetric Demo XM", "nuke.nodePaste('{}/nk_files/{}X_Aton_Examples.nk')".format(NST_FolderPath, prefixNST), icon="X_Aton.png")

cprint("| >> -SUCCESS- Loaded: GizmoDemo_Tools .....100%")
cprint("+-<GizmoDemoTools.printGizmos()>-------------")
cprint("| >> Adding node: ('Templates/Gizmo Demo Scripts/WaterLens Demo')")
cprint("| >> Adding node: ('Templates/Gizmo Demo Scripts/SSMesh Demo')")
cprint("| >> Adding node: ('Templates/Gizmo Demo Scripts/UVEditor Demo')")
cprint("| >> Adding node: ('Templates/Gizmo Demo Scripts/Sparky Demo')")
cprint("| >> Adding node: ('Templates/Gizmo Demo Scripts/ParticleLights Demo')")
cprint("| >> Adding node: ('Templates/Gizmo Demo Scripts/X_Aton Volumetric Demo')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading eTools")

toolbar = nuke.menu('Nodes')
eMenu = toolbar.addMenu('eTools', icon='eTools.png')
eMenu.addCommand('eFibonacciGlow', 'nuke.createNode("eFibonacciGlow")', icon='eFibonacciGlow.png')

cprint("| >> -SUCCESS- Loaded: eTools .....100%")
cprint("+-<eTools.printGizmos()>-------------")
cprint("| >> Adding node: ('eTools/eFibonacciGlow')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading ShotManager")

# Add .nuke/shotmanager to sys.path so we can import shotmanager
shotmanager_path = os.path.join(os.path.dirname(__file__), "shotmanager")
if shotmanager_path not in sys.path:
    sys.path.append(shotmanager_path)

# Add shortcut to access shotmanager:
shotmanager_key = "F10"
shotstudio_key = "F9"

try:
    # Try importing from .nuke/shotmanager/shotmanager_ui.py
    import shotmanager
    from shotmanager import shotmanager_ui
except ImportError as e:
    nuke.tprint(f"[ShotManager] Failed to import shotmanager_ui: {e}")
    shotmanager = None

try: 
    import shotmanager
    from shotmanager import shotstudio
except ImportError as e:
    nuke.tprint(f"[ShotManager] Failted to import shotstudio: {e}")

menu = nuke.menu("Nuke")
shotmanager_menu = menu.findItem("ShotManager") or menu.addMenu("ShotManager")
shotmanager_menu.addCommand("Launch ShotStudio", "shotstudio.launch_shotstudio()", shotstudio_key, icon="ShotStudio.png")
shotmanager_menu.addCommand("Launch ShotBrowser", "shotmanager_ui.launch_shotmanager_ui()", shotmanager_key, icon="ShotManager.png")
shotmanager_menu.addSeparator()
shotmanager_menu.addCommand("Help for ShotStudio", "shotmanager_ui.launch_help_window()", icon="info_icon.png")
shotmanager_menu.addCommand("Help for ShotBrowser", "shotmanager_ui.launch_help_window()", icon="info_icon.png")

cprint("| >> -SUCCESS- Loaded: ShotManager .....100%")
cprint("+-<ShotManager.printMenus()>-------------")
cprint("| >> Adding menu item: ('ShotManager/ShotStudio')")
cprint("| >> Adding menu item: ('ShotManager/ShotBrowser')")
cprint("+-----------------------------------------------------")
############################################################################################################
############################################################################################################
cprint("| Loading TractorSpool")

# Add .nuke/tractor to sys.path so we can import submit_to_tractor
tractor_path = os.path.join(os.path.dirname(__file__), "tractor")
if tractor_path not in sys.path:
    sys.path.append(tractor_path)

# Add shortcut to access tractorspool:
tractorspool_key = "F11"

try:
    # Try importing from .nuke/tractor/submit_to_tractor.py
    import submit_to_tractor
    from tractor import submit_to_tractor_ui
except ImportError as e:
    nuke.tprint(f"[Tractor] Failed to import submit_to_tractor: {e}")
    submit_to_tractor = None

if submit_to_tractor and hasattr(submit_to_tractor, "submit_to_tractor"):
    menu = nuke.menu("Nuke")
    tractor_menu = menu.findItem("Tractor") or menu.addMenu("Tractor")
    tractor_menu.addCommand("TractorSpool", "submit_to_tractor_ui.launch_submit_to_tractor_ui()", tractorspool_key, icon="TractorSpool.png")
    tractor_menu.addSeparator()
    tractor_menu.addCommand("Help for TractorSpool", "submit_to_tractor_ui.launch_help_window()", icon="info_icon.png")

cprint("| >> -SUCCESS- Loaded: TractorSpool .....100%")  
cprint("+-<TractorSpool.printMenus()>-------------")
cprint("| >> Adding menu item: ('Tractor/TractorSpool')")
cprint("+-----------------------------------------------------")
############################################################################################################
##############################  MENU.PY STARTUP COMPLETED  #################################################   
############################################################################################################

cprint("""+==============================================================================================+
<<<<<  MENU.PY STARTUP COMPLETED
+==============================================================================================+
      """)

# Call the hello function to print the welcome message
hello.nukeHello()

cprint("""+-<hello.nukeReady()>----------------------------------
| >> Running hello.nukeReady()""")
hello.nukeReady()
cprint("+-----------------------------------------------------")

cprint("""+-<hello.nukeTime()>----------------------------------
| >> Running hello.nukeTime()""")
hello.nukeTime()
cprint("+-----------------------------------------------------")

cprint("""
+============================+

REVERTING TO <NUKE_LOG> CALLS:""")
