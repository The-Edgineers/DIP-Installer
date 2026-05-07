pyinstaller main.py `
  --name DIP-Installer `
  --onefile `
  --noconsole `
  --add-data "assets;assets" `
  --add-data "installers/dotnet-install.ps1;installers" `
  --add-data "installers/MelonLoader.Installer.exe;installers" `
  --icon "assets\DIP_Installer_Icon.png"