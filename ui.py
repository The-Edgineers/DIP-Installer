import sys
import functions
import pathlib
import tkinter as tk
from tkinter import ttk

class Frame(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)

class Label(ttk.Label):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        styleLabel = ttk.Style()
        styleLabel.configure("My.TLabel",font=("Arial",14))
        self.configure(style="My.TLabel")

class Button(ttk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        styleButton = ttk.Style()
        styleButton.configure("My.TButton",font=("Arial",14))
        self.configure(style="My.TButton")

class MainWindow(tk.Tk):
    def __init__(self,version):
        super().__init__()
        self.title(f"Dreadnought Improvement Project Installer - {version}")
        self.configure(bg="#2b2b2b")
        self.columnconfigure(1,weight=3)
        self.rowconfigure(0, weight=1)

        # Frame - Left
        frameLeft = Frame(self)
        frameLeft.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)

        # Frame - Right
        frameRight = Frame(self)
        frameRight.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)

        # Button - Select UAD folder Location
        btnSelectUADFolder = Button(frameLeft,text="Select UAD Folder",command=lambda: functions.select_UAD_location(labelSelectedUADFolderPath))
        btnSelectUADFolder.grid(row=0,column=0,pady=5,padx=5)

        # Button - Select DIP archive Location
        btnSelectDIPZIP = Button(frameLeft,text="Select DIP .zip",command=lambda: functions.select_DIP_zip(labelSelectedDIPZIPPath))
        btnSelectDIPZIP.grid(row=0,column=1,pady=5,padx=5)

        # Button - Install
        btnInstall = Button(frameLeft,text="Install",command=lambda: functions.install(labelOutput))
        btnInstall.grid(row=1,column=0,pady=5)

        # Button - Uninstall
        btnUninstall = Button(frameLeft,text="Uninstall",command=lambda: functions.uninstall(labelOutput))
        btnUninstall.grid(row=1,column=1,pady=5)

        # Button - Backup
        btnBackup = Button(frameLeft,text="Backup",command=lambda: functions.backup(labelOutput))
        btnBackup.grid(row=2,column=0,pady=5)

        # Button - Restore
        btnRestore = Button(frameLeft,text="Restore",command=lambda: functions.restore(labelOutput))
        btnRestore.grid(row=2,column=1,pady=5)

        # Label - Selected UAD folder Location (preamble)
        labelSelectedUADFolder = Label(frameRight,text="Selected UAD folder:")
        labelSelectedUADFolder.grid(row=0,column=0,padx=5,pady=8,sticky="w")

        # Label - Selected UAD folder Location (selection)
        labelSelectedUADFolderPath = Label(frameRight,text="No folder selected yet")
        labelSelectedUADFolderPath.grid(row=0,column=1,padx=5,pady=8,sticky="w")

        # Label - Selected DIP archive Location (preamble)
        labelSelectedDIPZIP = Label(frameRight,text="Selected DIP archive:")
        labelSelectedDIPZIP.grid(row=1,column=0,padx=5,pady=8,sticky="w")

        # Label - Selected DIP archive Location (selection)
        labelSelectedDIPZIPPath = Label(frameRight,text="No DIP archive selected yet")
        labelSelectedDIPZIPPath.grid(row=1,column=1,padx=5,pady=8,sticky="w")

        # Label - Output text
        labelOutput = Label(frameRight,text="")
        styleOutputLabel = ttk.Style()
        styleOutputLabel.configure("Output.TLabel",font=("Arial",22))
        labelOutput.configure(style="Output.TLabel")
        labelOutput.grid(row=2,column=0,padx=5,pady=10,columnspan=2)

# Main
def render():
    app = MainWindow("Version 1.0.0")
    appIconPath = functions.get_base_path() / "assets" / "DIP_Installer_Icon.png"
    appIcon = tk.PhotoImage(file=appIconPath)
    app.iconphoto(True, appIcon)
    app.mainloop()