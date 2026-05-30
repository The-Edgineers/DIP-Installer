pyinstaller main.py `
  --name DIP-Installer `
  --onefile `
  --noconsole `
  --add-data "assets;assets" `
  --add-data "assets/MelonLoader.x64.zip;assets" `
  --icon "assets\DIP_Installer_Icon.png"