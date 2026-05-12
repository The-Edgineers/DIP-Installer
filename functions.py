import sys
import shutil
import subprocess
import threading
import zipfile

from pathlib import Path
from datetime import datetime
from tkinter import filedialog, messagebox


# =========================================================
# GLOBAL STATE
# =========================================================
selectedUADDir = ""
selectedDIPZip = ""
selected_output_label = None

# =========================================================
# PYINSTALLER HELPER FUNCTION
# =========================================================
def get_base_path():
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent

# =========================================================
# UI HELPERS
# =========================================================
def set_output_label(label):
    global selected_output_label
    selected_output_label = label

def update_output(text):
    if selected_output_label:
        selected_output_label.after(
            0,lambda: selected_output_label.config(text=text)
        )

# =========================================================
# OS DETECTION
# =========================================================
def get_OS():
    if sys.platform == "win32":
        return "Windows"
    elif sys.platform.startswith("linux"):
        return "Linux"
    return None


# =========================================================
# PATH SELECTION
# =========================================================
def select_UAD_location(label):
    global selectedUADDir

    path = filedialog.askdirectory(
        title="Select your Ultimate Admirals: Dreadnoughts directory"
    )

    if path:
        selectedUADDir = str(Path(path).resolve())
        label.config(text=selectedUADDir)


def select_DIP_zip(label):
    global selectedDIPZip

    downloads = Path.home() / "Downloads"

    path = filedialog.askopenfilename(
        title="Select DIP .zip archive",
        initialdir=downloads,
        filetypes=[("ZIP files", "*DIP*.zip"),("ZIP files", "*dip*.zip")]
    )

    if path:
        selectedDIPZip = str(Path(path).resolve())
        label.config(text=selectedDIPZip)


# =========================================================
# VALIDATION
# =========================================================
def verify_uad_dir() -> bool:
    global selectedUADDir
    if not selectedUADDir:
        return False

    path = Path(selectedUADDir).resolve()
    parts = tuple(p.lower() for p in path.parts)
    expected = ("steamapps", "common", "ultimate admiral dreadnoughts")
    return parts[-3:] == expected

def verify_dip_zip():
    return (
        selectedDIPZip
        and Path(selectedDIPZip).suffix == ".zip"
        and "dip" in Path(selectedDIPZip).name.lower()
    )

def verify_melonloader_installation():
    expectedFolder = Path(selectedUADDir) / "MelonLoader"
    if expectedFolder.exists():
        return True
    return False

def get_mods_path(uninstall_entrybool=False,backing_up=False):
    modsFolders = []

    for object in Path(selectedUADDir).iterdir():
        if object.is_dir() and object.name.lower().__contains__("mods"):
            modFolderPath = str(Path(object).resolve())
            modsFolders.append(modFolderPath)

    if modsFolders.__len__() > 0 and modsFolders.__len__() < 2:
        return Path(modsFolders[0]).resolve()
    elif modsFolders.__len__() > 1:
        if uninstall_entrybool:
            title = "Select the Mods folder containing the DIP installation you wish to uninstall"
        elif backing_up:
            title = "Select the Mods folder containing the DIP installation you wish to backup"
        else:
            title = "Select the Mods folder where your wish to install the selected DIP archive into"
        path = filedialog.askdirectory(
        title=f"{title}",
        initialdir=selectedUADDir,
    )
        if path and path.lower().__contains__("mods"):
            return Path(path).resolve()
        else:
            update_output("Invalid Mods folder selected, please try again")
            return False
    else:
        if not uninstall_entrybool:
            modsFolderToCreate = Path(selectedUADDir) / "Mods"
            modsFolderToCreate.mkdir(parents=True,exist_ok=True)
            return Path(modsFolderToCreate).resolve()
        else:
            update_output("No mods folder found in your UAD directory")
            return False

def find_existing_dip(mods_path: Path):
    if not mods_path or not mods_path.exists():
        return None

    version_file = mods_path / "version.txt"
    if version_file.exists():
        return version_file.read_text().strip()

    return None


# =========================================================
# UNINSTALL
# =========================================================
def uninstall(output_label=None,mods_path=None):

    existing = None

    if output_label is not None:
        set_output_label(output_label)
    
    if not selectedUADDir:
        update_output("No valid UAD directory selected")
        return False

    if mods_path is None:
        selected_mods_path = get_mods_path(uninstall_entrybool=True)
        if selected_mods_path is not False:
            mods_path = selected_mods_path
            existing = find_existing_dip(selected_mods_path)
        else:
            return
    else:
        existing = find_existing_dip(mods_path)

    if not existing:
        update_output("No DIP installation found (No contents / version.txt not found)")
        return False

    update_output(f"Uninstalling {existing}")

    shutil.rmtree(mods_path)
    mods_path.mkdir(parents=True,exist_ok=True)

    update_output(f"{existing} uninstalled")
    return True


# =========================================================
# DIP INSTALL
# =========================================================
def install_DIP():
    zip_path = Path(selectedDIPZip)
    update_output(f"Installing {zip_path.stem}")
    mods_path = get_mods_path()

    if mods_path is False:
        return

    existing = find_existing_dip(mods_path)

    def extract():
        update_output(f"Extracting {zip_path.name}")

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(mods_path)

        (mods_path / "version.txt").write_text(zip_path.stem)

        update_output(f"{zip_path.stem} installed")

    def do_install():
        if existing:
            uninstall(mods_path=mods_path)
        extract()

    if existing:
        def ask():
            result = messagebox.askyesno(
                "Existing Installation Detected",
                f"You currently have '{existing}' installed.\n\nOverwrite?"
            )

            if result:
                selected_output_label.after(0, do_install)
            else:
                update_output("Installation cancelled")

        selected_output_label.after(0, ask)
    else:
        extract()


# =========================================================
# MELONLOADER
# =========================================================
def install_melonloader():

    if verify_melonloader_installation():
        update_output("MelonLoader already installed")
        install_DIP()
        return

    update_output("Installing MelonLoader")

    base = get_base_path() / "installers"

    if get_OS() == "Linux":
        script = base / "MelonLoader.Installer.Linux"
        script.chmod(0o755)
    else:
        script = base / "MelonLoader.Installer.exe"

    cmd = [str(script)]

    def worker():
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            process.wait()
            success = process.returncode == 0

            def next_step():
                if success:
                    update_output("MelonLoader installed")
                    install_DIP()
                else:
                    update_output("MelonLoader installation failed")

            selected_output_label.after(0, next_step)
        except Exception as e:
            update_output(f"MelonLoader installation error: {e}")
            return

    threading.Thread(target=worker, daemon=True).start()


# =========================================================
# DOTNET 6
# =========================================================
def install_dotnet6():
    update_output("Installing .NET 6.0")

    base = get_base_path() / "installers"

    if get_OS() == "Linux":
        script = base / "dotnet-install.sh"
        script.chmod(0o755)
        cmd = ["bash", str(script), "--runtime", "dotnet", "--channel", "6.0"]

    else:
        script = base / "dotnet-install.ps1"
        cmd = [
            "powershell.exe",
            "-ExecutionPolicy", "Bypass",
            "-File", str(script),
            "-Runtime", "dotnet",
            "-Channel", "6.0"
        ]

    def worker():
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            process.wait()
            success = process.returncode == 0

            def next_step():
                if success:
                    update_output(".NET 6 installed")
                    install_melonloader()
                else:
                    update_output(".NET 6 failed")

            selected_output_label.after(0, next_step)
        except Exception as e:
            update_output(f".NET 6 installation error: {e}")
            return

    threading.Thread(target=worker, daemon=True).start()


# =========================================================
# INSTALL
# =========================================================
def install(output_label=None):
    if output_label is not None:
        set_output_label(output_label)

    if not verify_uad_dir():
        update_output("No valid UAD directory selected")
        return

    if not verify_dip_zip():
        update_output("No valid DIP zip selected")
        return

    install_dotnet6()


# =========================================================
# BACKUP SYSTEM
# =========================================================
def backup(output_label=None):
    if output_label is not None:
        set_output_label(output_label)

    if not verify_uad_dir():
        update_output("No valid UAD directory selected")
        return

    mods = get_mods_path(backing_up=True)
    if not mods:
        return

    existing = find_existing_dip(mods)

    if not existing:
        update_output("No DIP installation found (No contents / version.txt not found)")
        return

    modsPathFolderName = tuple(mods.parts)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"{existing}_{timestamp}"

    backup_root = (
        Path(selectedUADDir)
        / "DIP-Backups"
        / modsPathFolderName[-1]
        / backup_name
    )

    backup_root.mkdir(parents=True)

    update_output(f"Backing up {modsPathFolderName[-1]}/{existing}")

    for item in mods.iterdir():
        target = backup_root / item.name

        if item.is_file():
            shutil.copy2(item, target)

        elif item.is_dir():
            shutil.copytree(item, target)

    update_output(f"Backup created: {modsPathFolderName[-1]}/{backup_name}")


# =========================================================
# RESTORE SYSTEM
# =========================================================
def check_for_restore_folder():
    if (Path(selectedUADDir)/"DIP-Backups").exists():
        return True
    else:
        return False

def restoreBackup(sourcePath,targetPath):
    if targetPath.exists():
        confirmation = messagebox.askyesno(
            "Restore confirmation",
            f"{targetPath} already exists.\n\n Do you wish to overwrite it?"
        )
        if confirmation:
            shutil.rmtree(targetPath)
            targetPath.mkdir(parents=True,exist_ok=True)

            for item in sourcePath.iterdir():
                target = targetPath / item.name

                if item.is_file():
                    shutil.copy2(item, target)
                elif item.is_dir():
                    shutil.copytree(item, target)
            update_output("Restore completed")
        else:
            update_output("Restore cancelled")
            return
    else:
        targetPath.mkdir(parents=True)
        for item in sourcePath.iterdir():
            target = targetPath / item.name

            if item.is_file():
                shutil.copy2(item, target)
            elif item.is_dir():
                shutil.copytree(item, target)
        update_output("Restore completed")
        return

def restore(output_label=None):
    if output_label is not None:
        set_output_label(output_label)

    if not verify_uad_dir():
        update_output("No valid UAD directory selected")
        return
    
    if check_for_restore_folder():
        backupsFolder = Path(selectedUADDir)/"DIP-Backups"
    else:
        update_output("No DIP-Backups folder found. Make a backup first")
        return

    folderToRestore = filedialog.askdirectory(
        title="Select DIP backup to restore",
        initialdir=backupsFolder
    )

    if folderToRestore:
        restorePathFolderName = tuple(Path(folderToRestore).parts)
        if restorePathFolderName[-1].lower().__contains__("dip") and "backups" not in restorePathFolderName[-1].lower():
            restoreSource = Path(folderToRestore)
            restoreDestination = Path(selectedUADDir) / restorePathFolderName[-2]
            restoreBackup(restoreSource,restoreDestination)
        else:
            update_output("No valid DIP backup selected")
            return
    else:
        update_output("Restore procedure aborted")
        return