import pathlib
import subprocess
import threading
import shutil
import zipfile
import sys
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
        return pathlib.Path(sys._MEIPASS)
    return pathlib.Path(__file__).resolve().parent

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
        selectedUADDir = str(pathlib.Path(path).resolve())
        label.config(text=selectedUADDir)


def select_DIP_zip(label):
    global selectedDIPZip

    downloads = pathlib.Path.home() / "Downloads"

    path = filedialog.askopenfilename(
        title="Select DIP .zip archive",
        initialdir=downloads,
        filetypes=[("ZIP files", "DIP*.zip")]
    )

    if path:
        selectedDIPZip = str(pathlib.Path(path).resolve())
        label.config(text=selectedDIPZip)


# =========================================================
# VALIDATION
# =========================================================
def verify_uad_dir() -> bool:
    global selectedUADDir
    if not selectedUADDir:
        return False

    path = pathlib.Path(selectedUADDir).resolve()
    parts = tuple(p.lower() for p in path.parts)
    expected = ("steamapps", "common", "ultimate admiral dreadnoughts")
    return parts[-3:] == expected

def verify_dip_zip():
    return (
        selectedDIPZip
        and pathlib.Path(selectedDIPZip).suffix == ".zip"
        and "dip" in pathlib.Path(selectedDIPZip).name.lower()
    )

def get_mods_path():
    if not selectedUADDir:
        return None

    mods = pathlib.Path(selectedUADDir) / "Mods"
    return mods if mods.exists() else None


def find_existing_dip(mods_path: pathlib.Path):
    if not mods_path or not mods_path.exists():
        return None

    version_file = mods_path / "version.txt"
    if version_file.exists():
        return version_file.read_text().strip()

    return None


# =========================================================
# UNINSTALL
# =========================================================
def uninstall(output_label=None):
    if output_label is not None:
        set_output_label(output_label)
    mods_path = get_mods_path()

    if not mods_path:
        update_output("Invalid UAD directory")
        return False

    existing = find_existing_dip(mods_path)

    if not existing:
        update_output("No DIP installation found")
        return False

    update_output(f"Uninstalling {existing}")

    shutil.rmtree(mods_path)
    mods_path.mkdir(parents=True, exist_ok=True)

    update_output(f"{existing} uninstalled")
    return True


# =========================================================
# DIP INSTALL
# =========================================================
def install_DIP():
    mods_path = get_mods_path()

    if not mods_path:
        update_output("Invalid Mods path")
        return

    zip_path = pathlib.Path(selectedDIPZip)
    existing = find_existing_dip(mods_path)

    def extract():
        update_output(f"Extracting {zip_path.name}")

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(mods_path)

        (mods_path / "version.txt").write_text(zip_path.stem)

        update_output(f"{zip_path.stem} installed")

    def do_install():
        if existing:
            uninstall()
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
    mods = get_mods_path()

    if mods:
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

    mods = get_mods_path()

    if not mods:
        update_output("Invalid UAD directory")
        return

    existing = find_existing_dip(mods)

    if not existing:
        update_output("No DIP installation found")
        return

    backup_root = pathlib.Path(selectedUADDir) / "DIP-Backups" / existing

    # -----------------------------
    # STOP if backup already exists
    # -----------------------------
    if backup_root.exists():
        update_output(f"A backup of {existing} already exists")
        return

    backup_root.mkdir(parents=True)

    update_output(f"Backing up {existing}")

    for item in mods.iterdir():
        target = backup_root / item.name

        if item.is_file():
            shutil.copy2(item, target)

        elif item.is_dir():
            shutil.copytree(item, target)

    update_output(f"{existing} backed up")


# =========================================================
# RESTORE SYSTEM
# =========================================================
def restoreBackup(backup_path, version):
    mods = get_mods_path()

    if not mods:
        update_output("Invalid Mods path")
        return

    backup_path = pathlib.Path(backup_path)

    update_output(f"Restoring {version}")

    uninstall()

    for item in backup_path.iterdir():
        target = mods / item.name

        if item.is_file():
            shutil.copy2(item, target)
        elif item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)

    update_output(f"{version} restored")


def check_for_restore_folders():

    if verify_uad_dir() is False:
        update_output("Invalid UAD directory selected")
        return

    base = pathlib.Path(selectedUADDir)

    backup_root = base / "DIP-Backups"

    if backup_root.exists():
        return backup_root
    else:
        update_output("No backups found")
        return None


def restore(output_label=None):
    if output_label is not None:
        set_output_label(output_label)

    folder = check_for_restore_folders()

    if not folder:
        return

    selected = filedialog.askdirectory(
        title="Select backup to restore",
        initialdir=str(folder)
    )

    if selected:
        mods = get_mods_path()
        existing = find_existing_dip(mods)
        if existing:
            def ask():
                result = messagebox.askyesno(
                    "Existing Installation Detected",
                    f"You currently have '{existing}' installed.\n\nOverwrite?"
                )

                if result:
                    version = pathlib.Path(selected).name
                    uninstall()
                    restoreBackup(selected, version)
                else:
                    update_output("Installation cancelled")

            selected_output_label.after(0, ask)
        else:
            version = pathlib.Path(selected).name
            uninstall()
            restoreBackup(selected, version)