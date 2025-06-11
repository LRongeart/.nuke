TO INSTALL “Tractor for Nuke”, version 1.0
———————————————————————————————————

1. Unzip the archive
2. Drag and drop the folder in your .nuke folder
	#in your .nuke folder, path would be something like this:

	#Linux:       /home/login name/.nuke
	#Mac OS X:    /Users/login name/.nuke
	#Windows:     drive letter:\Users\user name\.nuke

3. Add this code to your file init.py and of course modify the Tractor_path (do not change the file init.py in the folder Tractor) 

	Tractor_path = "/Users/yourPath/.nuke/Tractor"
	nuke.pluginAddPath(Tractor_path)

4. Run Nuke

——————————————————————

If you have troubles, contact me: andrea.geremia89@gmail.com