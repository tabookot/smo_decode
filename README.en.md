[🇷🇺 Русский](README.md) | [🇬🇧 English](README.en.md)

# ScanMyOpel Log Decoder

> **Compatible with "ScanMyOpel 1.1.36"**. If it doesn't work — direct all complaints to the electric sheep! 😉

The scripts require **Python 3.6** or higher to be installed.

---

## 🚀 Quick Start

1. Connect a compatible OBD2 to your phone.
2. In the ScanMyOpel app:
   - Left menu ➔ Settings ➔ select protocol and your OBD2.
   - Select year, model, transmission ➔ connect.
   - Left menu:
     - Check the "enable" box to start recording the log.
     - Do whatever you want to test on the car.
     - Uncheck the box at the end.
     - Click **Send Logs** — send the archive to your computer.
3. On your computer:
   - Download the scripts from this repository (see instructions below).
   - Extract the files `ScanMyOpel_Logging_Global__[date_time].smo` from the `.zip` archive (sent from the phone) and place them next to the scripts.
   - Two script options are available:
     - `smo_decode` — a simple decoder to `.txt`, just raw decoding.
     - `smo_decode_plus` — removes garbage, builds a pseudo-table and text graphs (sparklines).
   - `.py` files are the scripts themselves, `.bat` files are for launching on Windows with a double-click.

---

## ⬇️ How to download the scripts

Since this is an open code repository, you can download the program in two ways:

### Method 1: Download ZIP archive (The easiest, for everyone)
1. On the main page of the repository.
2. Find the green **`<> Code`** button and click it.
3. In the menu that appears, select **`Download ZIP`**.
4. The `smo_decode-main.zip` archive will be downloaded. Extract it to any folder on your computer (e.g., Desktop).
5. Inside the extracted folder, you will find the required `.py` and `.bat` files.

### Method 2: Via Git (For advanced users)
If you have Git installed, run in the terminal:
```bash
git clone https://github.com/tabookot/smo_decode.git
```

---

## 📖 Detailed instructions for use

The `smo_decode_plus` script reads the closed log files of the ScanMyOpel application (`*.smo`), decodes them, cleans them from service garbage, combines repeated polling cycles into a single table, and builds text graphs (sparklines) for digital parameters.

### 1. System Requirements
- **OS:** Windows, macOS, or Linux.
- **Python:** version 3.6 or higher.
- **Additional libraries:** NOT REQUIRED (the script uses only standard Python modules).

### 2. Installing Python

#### 💻 For Windows:
1. Go to the official website: https://www.python.org/downloads/
2. Download the latest version of Python 3 (button "Download Python 3.x.x").
3. Run the downloaded installer.
4. ⚠️ **IMPORTANT:** At the bottom of the installer window, MAKE SURE to check the box **"Add python.exe to PATH"**.
5. Click "Install Now" and wait for the installation to finish.

#### 🍎 For macOS:
1. Open the "Terminal" app (`Command + Space` ➔ Terminal).
2. If you have the Homebrew package manager installed (recommended), run the command:
   ```bash
   brew install python
   ```
3. If you don't have Homebrew, download the installer from https://www.python.org/downloads/ and install it as a regular program.

#### 🐧 For Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3
```

#### 🐧 For Linux (Fedora/RHEL):
```bash
sudo dnf install python3
```

### 3. Preparing the files
1. If you downloaded the ZIP archive (see the "How to download" section), extract it to a convenient folder (e.g., `OpelLogs` on your Desktop).
2. Copy the log files from the ScanMyOpel app (files with the `.smo` extension) and place them in the same folder, next to the `smo_decode_plus.py` and `smo_decode.py` scripts.

### 4. Running the script

You need to open a Terminal (in Windows — "Command Prompt" or "PowerShell", in macOS/Linux — "Terminal") and specify the path to your folder.

#### Method A: Decode ALL `.smo` files in the folder at once
*(The script will automatically find all `.smo` files next to itself)*

1. In the terminal, navigate to the folder with the script using the `cd` command:
   ```bash
   # Windows
   cd %USERPROFILE%\Desktop\OpelLogs

   # macOS
   cd ~/Desktop/OpelLogs

   # Linux
   cd ~/Desktop/OpelLogs
   ```
2. Run the script:
   ```bash
   # Windows
   python smo_decode_plus.py

   # macOS / Linux
   python3 smo_decode_plus.py
   ```

#### Method B: Decode only ONE specific file

1. In the terminal, navigate to the folder with the script (see step 1 above).
2. Run the script, specifying the file name:
   ```bash
   # Windows
   python smo_decode_plus.py my_log.smo

   # macOS / Linux
   python3 smo_decode_plus.py my_log.smo
   ```

### 5. Where to find the result?

After the script successfully executes, new text files with the same name but with a `.txt` extension will appear in the same folder.

For example, if you processed the file `log_2023.smo`, a file `log_2023.txt` will appear next to it. Open it in any text editor ("Notepad", Notepad++, VS Code, TextEdit).

> 💡 **TIP:** For convenient viewing of tables without distorting the columns, open the file in editors with a monospaced font (e.g., Notepad++, VS Code, or standard Notepad) and turn off word wrapping.

### 6. Possible issues

**Error:** `python: command not found` or `python is not recognized`
**Solution:** You didn't check the "Add to PATH" box during Python installation (on Windows). Alternatively, use the `python3` command instead of `python`.

**Error:** `FileNotFoundError`
**Solution:** You are trying to run the script from the wrong folder where the `.smo` files are located, or you specified the file name incorrectly.

> ⚠️ **NOTE REGARDING LOG CONTENTS:**
> If the ScanMyOpel app log recorded only "raw" data (lines like `80 F1 18 22 61 01...`) without text parameter names, the script will process such a log, but the "Live data" section will be empty because the app failed to record the parameter names.