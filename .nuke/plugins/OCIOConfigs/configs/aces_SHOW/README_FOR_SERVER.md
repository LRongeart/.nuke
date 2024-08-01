### ACES_SHOW DIRECTORY ###

__DESCRIPTION__
ACES_SHOW is a package derivated from the ACES 1.2 OCIO config, originally created to reduce confusion in a production environment.
This project is inspired by VFX vendors that create custom ICMW (Image ColorManagement Workflows) for each Show they work on.
It is pretty common that artists have wrong habits when dealing with colorSpaces, resulting in picture quality deprecation along the
pipeline, or additional technical issues that could easily be avoided with an appropriate work environment.
ICMW are designed to simplify and automate certain of these aspects to reduce friction & build stronger pipelines.

ColorSpaces needs vary less in a 100% CGI-produced Feature production environment. 
It's then more appropriate to have a generic template to use for every Show -- This package aims to fill all these requirements.

ACES 1.2 provide the widest range of colorSpaces & can help to work in an ACEScg gamut right off the bat -- Thus leading to less issues
when working on sRGB due to its dynamic range being far narrower than ACEScg.
It's probably the best base to build a state-of-the-art ICMW with the lowest resource investment; also as most issues have already been documented online.


__FOLDER CONTENT__
This package provides:
- custom colorSpaces added to the .OCIO file, in the master folder;
- In the '__INSTALL__' folder:
	- template files for multiple production softwares;
	- setup instructions for every software;
	- testScenes for every software to make sure things work appropriately; 


__CUSTOM COLORSPACES__
- show_acescg_view
- show_acescg_in
- show_acescg_out
- show_acescgraw_in
- show_acescglog_in


__SOFTWARE INSTALL INSTRUCTIONS & TEST SCENES:
- Maya;
- Houdini;
- Nuke;
- Mari;
- SubstancePainter;
- SubstanceDesigner;
- Affinity;


-LR;