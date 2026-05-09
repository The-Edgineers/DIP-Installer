# DIP-Installer
Installer for the [Dreadnought Improvement Project (DIP)](https://github.com/brothermunro/Dreadnought-Improvement-Project), a mod for Ultimate Admiral: Dreadnoughts

## Overview
Provides a user friendly UI to aid with the installation of DIP. Also provides:
- Microsoft .NET Runtime 6.0 (Linux and Windows scripts from Microsoft - They will complete very quickly if you already have this)
- MelonLoader Installer (Linux and Windows (v0.6.6), If you already have MelonLoader set up with UAD, DIP-Installer will skip this)
- Backup & Restore
- Uninstall (Only removes DIP, not MelonLoader or .NET Runtime 6.0)

## Supported sources for DIP .zip archives
https://www.nexusmods.com/ultimateadmiraldreadnoughts/mods/7?tab=files (*Currently the DIP-Installer only works properly with Nexus-based DIP archives*)

## Instructions
1. Ensure you have Ultimate Admiral Dreadnoughts installed through Steam
2. Download your desired DIP .zip archive(s). Put them in your user's Downloads folder
3. Download the latest DIP-Installer release (.exe for Windows, .Linux for Linux)

## IMPORTANT NOTICE REGARDING OLD INSTALLATIONS / NON DIP-INSTALLER INSTALLATIONS
The DIP-Installer injects a version.txt into a DIP installation based on the archive name (useful for debugging etc). However, installations not conducted by the DIP-Installer don't have this. In order to make your old installation compatible with DIP-Installer you need to perform some manual actions, see the steps below:

1. In your UAD folder, go into (one of) your Mods folder(s)
2. In that folder, add a file "version.txt" and inside of that file, on line 1, add some simple recogniseable text (i.e. "DIP-Extended-dd-mm-yyyy")
3. Now in the DIP-Installer, select the location of your UAD folder
4. In the DIP-Installer, once your UAD folder location has been set, press the "Backup" button. If you have multiple Mods folders, select the DIP installation inside the Mods folder you prepared in step 2
5. You should now have a backup of your previous installation in a folder called "DIP-Backups/{name of your Mods folder}/{name of your DIP installation from the version.txt}", allowing you to install other DIP .zip archives or alternative installations if you are more experimental

## Support
We provide help should you encounter issues. You can contact us in [BrotherMunro's Discord](https://discord.gg/2F4eDfzd9). Once in there, seek help within the **dip-tech-support** channel

## Contribution
As this is an open source application, contribution is simple:
- Make a fork of this repository's develop branch
- Conduct change(s) on your fork repository
- Once your repository is ready, conduct a merge request to this repository's develop branch

## TODO
- Managing custom ship designs
- Support for non-Nexus DIP archives
- Support for submods