______TWEAKS_______
	1_ Edit 'C:\Program Files\Pixar\RenderManProServer-26.1\etc/it.ini
		Change:
			l72- SetPref itOcioConfig ACES-1.2
			l76- SetPref itOcioUseRoles 1

______ENV VARIABLES TO CREATE:________
OCIO -- '(aces_CUSTOMfolder)/config.ocio'
RMAN_COLOR_CONFIG_DIR -- '(aces_CUSTOMfolder)/txmanager'
IT_OCIOV1 -- '(aces_CUSTOMfolder)/config.ocio'