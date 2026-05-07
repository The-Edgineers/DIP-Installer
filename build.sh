#!/bin/bash

pyinstaller main.py \
  --name DIP-Installer \
  --onefile \
  --noconsole \
  --add-data "assets:assets" \
  --add-data "installers/dotnet-install.sh:installers" \
  --add-data "installers/MelonLoader.Installer.Linux:installers" \
  --icon assets/DIP_Installer_Icon.png