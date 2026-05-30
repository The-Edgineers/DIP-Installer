# DIP-Installer
Installer for the [Dreadnought Improvement Project (DIP)](https://github.com/brothermunro/Dreadnought-Improvement-Project), a mod for [Ultimate Admiral: Dreadnoughts](https://store.steampowered.com/app/1069660/Ultimate_Admiral_Dreadnoughts/), a game made by [Game-Labs](https://en.wikipedia.org/wiki/Game-Labs), whom have [since December 27 2024](https://store.steampowered.com/news/app/1069660/view/515196931452962390) ceased further development of the game.

## Overview
Provides a user friendly UI to aid with the installation of DIP. Also provides:
- Microsoft .NET Desktop Runtime 6.0 installer
- MelonLoader deployment (Linux and Windows (v0.6.6), If you already have MelonLoader set up with UAD, DIP-Installer will skip this)
- Backup & Restore
- Uninstall (Only removes DIP, not MelonLoader or .NET Desktop Runtime 6.0)

## Supported sources for DIP .zip archives
https://www.nexusmods.com/ultimateadmiraldreadnoughts/mods/7?tab=files **(RECOMMENDED)**  
https://github.com/brothermunro/Dreadnought-Improvement-Project/releases

## Installation Walkthrough
### Windows
**MANUAL ACTIONS REQUIRED PRIOR: None**

1. Launch DIP-Installer.exe
2. Click on `Select UAD Folder` and browse to select your UAD folder. This is commonly `../steamapps/common/Ultimate Admiral Dreadnoughts`
3. Click on `Select DIP .zip`. Select the desired .zip you wish to install. For example, using the Nexus all-in-one archive, you could select `DIP Extended 1.3.4.zip`
4. Press `Install`
5. Go through the .NET 6.0 Desktop Runtime installer (if another .NET 6.0 Desktop Runtime installer pops up after u have completed .NET installation, press cancel and conduct step 4 again, it should now detect your installation and proceed to MelonLoader)
6. Wait until MelonLoader installation finishes
7. Wait until you receive a popup that says your DIP .zip from step 3 is installed
8. Launch UAD & Enjoy DIP

### Linux
**MANUAL ACTIONS REQUIRED PRIOR:** Having Protontricks installed. We recommend installing it [through Flatpak (also do the shell alias section)](https://github.com/Matoking/protontricks#flatpak-recommended)

**WARNING: DIP-Installer has only been tested with Flatpak-based Protontricks**. You are free to install Protontricks differently, the important part is that `protontricks` is a viable command inside your terminal/CLI

1. Launch DIP-Installer.Linux
2. Click on `Select UAD Folder` and browse to select your UAD folder. This is commonly `../steamapps/common/Ultimate Admiral Dreadnoughts`
3. Click on `Select DIP .zip`. Select the desired .zip you wish to install. For example, using the Nexus all-in-one archive, you could select `DIP Extended 1.3.4.zip`
4. Press `Install`
5. Go through the .NET 6.0 Desktop Runtime installer (if another .NET 6.0 Desktop Runtime installer pops up after u have completed .NET installation, press cancel and conduct step 4 again, it should now detect your installation and proceed to MelonLoader)
6. Wait until MelonLoader installation finishes
7. Wait until you receive a popup that says your DIP .zip from step 3 is installed
8. In Steam, go to Ultimate Admiral Dreadnoughts. Right click > Properties > Launch Options > insert the following: `WINEDLLOVERRIDES="version=n,b" %command%`
9. Launch UAD & Enjoy DIP

## Support
We provide help should you encounter issues. You can contact us in [BrotherMunro's Discord](https://discord.gg/2F4eDfzd9). Once in there, seek help within the **dip-tech-support** channel, specifically, the **DIP-Installer Support Thread**

## Contribution
As this is an open source application, contribution is simple:
- Make a fork of this repository's develop branch
- Conduct change(s) on your fork repository
- Once your repository is ready, conduct a merge request to this repository's develop branch

## TODO
- Managing custom ship designs
- Support for submods

## IMPORTANT NOTICE REGARDING OLD INSTALLATIONS / NON DIP-INSTALLER INSTALLATIONS
The DIP-Installer injects a version.txt into a DIP installation based on the archive name (useful for debugging etc). However, installations not conducted by the DIP-Installer don't have this. In order to make your old installation compatible with DIP-Installer you need to perform some manual actions, see the steps below:

1. In your UAD folder, go into (one of) your Mods folder(s)
2. In that folder, add a file "version.txt" and inside of that file, on line 1, add some simple recogniseable text (i.e. "DIP-Extended-1.3.4-dd-mm-yyyy")
3. Now in the DIP-Installer, select the location of your UAD folder
4. In the DIP-Installer, once your UAD folder location has been set, press the "Backup" button. If you have multiple Mods folders, select the DIP installation inside the Mods folder you prepared in step 2
5. You should now have a backup of your previous installation in a folder called "DIP-Backups/{name of your Mods folder}/{name of your DIP installation from the version.txt}", allowing you to install other DIP .zip archives or alternative installations if you are more experimental