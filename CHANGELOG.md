# 2.0.0
- Removed .ps1 and .sh scripts for .NET 6.0 Core Runtime
- Added .NET 6.0 Desktop Runtime dedicated installation logic for Windows and Linux respectively
- Removed MelonLoader installer .exe and .Linux
- Added MelonLoader 0.6.6 .zip for Linux and Windows
- Refactored the installation logic to deploy the MelonLoader .zip inside the UAD directory if no existing MelonLoader can be found there

# 1.1.0
- Added CHANGELOG
- Core functionalities now support non-Nexus archives
- Removed .zip name filter
- Added TAF detection to refine DIP archive validation
- Added an explicit installation abort when using an unsupported OS

# 1.0.0
Initial release of core functionalities, Nexus-archives support only
- Install
- Uninstall
- Backup
- Restore