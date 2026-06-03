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
#### Prerequisites
1. Your system must have `winget`. Open the command prompt and type in `winget`. If this returns a list of options, you are good to go.
2. If you do not have `winget`, get it here: https://apps.microsoft.com/detail/9nblggh4nns1 (`winget` is provided by App Installer)

#### Usage
1. Double click on `DIP-Installer.exe`
2. Click on `Select UAD Folder` and browse to select your UAD folder. This is commonly `../steamapps/common/Ultimate Admiral Dreadnoughts`
3. Click on `Select DIP .zip`. Select the desired .zip you wish to install. For example, using the Nexus all-in-one archive, you could select `DIP Extended 1.3.4.zip`
4. Press `Install`
5. Go through the .NET 6.0 Desktop Runtime installer (You may first see a shell, do not close it, just wait for the Windows application to load up)
6. Wait until MelonLoader installation finishes
7. Wait until you receive a popup that says your DIP .zip from step 3 is installed
8. Launch UAD & Enjoy DIP

### Linux
#### Prerequisites
1. Having Protontricks installed. We recommend installing it [through Flatpak (also do the shell alias section)](https://github.com/Matoking/protontricks#flatpak-recommended)
2. In Steam, go to Ultimate Admiral Dreadnoughts. Right click > Properties > Launch Options > insert the following: `WINEDLLOVERRIDES="version=n,b" %command%`
3. Before running the installer, you **MUST** either set your global Steam compatibility setting to use a Proton version or specifically set UAD's compatibility setting to use one (**tested to work with Proton Experimental**). Also be sure that you have launched the game at least once prior to running this application

**WARNING: DIP-Installer has only been tested with Flatpak-based Protontricks**. You are free to install Protontricks differently, the important part is that `protontricks` is a viable command inside your terminal/CLI

#### Usage
1. Double click `DIP_Installer-x86_64.AppImage`
2. Click on `Select UAD Folder` and browse to select your UAD folder. This is commonly `../steamapps/common/Ultimate Admiral Dreadnoughts`
3. Click on `Select DIP .zip`. Select the desired .zip you wish to install. For example, using the Nexus all-in-one archive, you could select `DIP Extended 1.3.4.zip`
4. Press `Install`
5. Go through the .NET 6.0 Desktop Runtime installer (It will pop up 2 times. Go through it both times.)
6. Wait until MelonLoader installation finishes
7. Wait until you receive a popup that says your DIP .zip from step 3 is installed
8. Launch UAD & Enjoy DIP

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

## Notices
### Old Installations
The DIP-Installer injects a version.txt into a DIP installation based on the archive name (useful for debugging etc). However, installations not conducted by the DIP-Installer don't have this. In order to make your old installation compatible with DIP-Installer you need to perform some manual actions, see the steps below:

1. In your UAD folder, go into (one of) your Mods folder(s)
2. In that folder, add a file "version.txt" and inside of that file, on line 1, add some simple recogniseable text (i.e. "DIP-Extended-1.3.4-dd-mm-yyyy")
3. Now in the DIP-Installer, select the location of your UAD folder
4. In the DIP-Installer, once your UAD folder location has been set, press the "Backup" button. If you have multiple Mods folders, select the DIP installation inside the Mods folder you prepared in step 2
5. You should now have a backup of your previous installation in a folder called "DIP-Backups/{name of your Mods folder}/{name of your DIP installation from the version.txt}", allowing you to install other DIP .zip archives or alternative installations if you are more experimental

### Too-high-version of MelonLoader installed
DIP is designed exclusively around MelonLoader version 0.6.6. To rule out (one) source of issues, make sure you run DIP with MelonLoader v0.6.6  

In order to downgrade, should you have a higher version, follow the guide below depending on what you used prior:

#### You used DIP-Installer (v1.0.0 to v1.1.0)
1. Go to your UAD folder and select your MelonLoader folder. Delete that folder.
2. Run DIP-Installer.exe / DIP_Installer-x86_64.AppImage (See the `Installation Walkthrough` section for your platform)

#### You used the MelonLoader Installer .exe / .Linux graphical installation tool
1. Download `MelonLoader.Installer.exe` (Windows) or `MelonLoader.Installer.Linux` (Linux) [(0.6.6 MelonLoader release page)](https://github.com/LavaGang/MelonLoader/releases/tag/v0.6.6)
2. Run the downloaded tool
3. Inside this tool, select UAD
4. Now you'll see a dropdown version menu. Make sure that says `0.6.6`
5. Hit (re)install. Done