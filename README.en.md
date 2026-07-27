[🇬🇧 English](README.en.md) | [🇷🇺 Русский](README.md)

# ScanMyOpel Log Decoder

> **Compatible with [ScanMyOpel](https://scanmyopel.com) 1.1.36**. If it doesn't work, blame the electric sheep! 😉
> *Authors' collective — GPT 5.5, GLM 5.2, and Kimi K3.*

The scripts require **Python 3.6** or higher to be installed.

---

## 🚀 Quick Start

1. Connect a compatible OBD2 adapter to your phone.
2. In the ScanMyOpel app:
   - Left menu ➔ Settings ➔ select protocol and your OBD2.
   - Select year, model, transmission ➔ connect.
   - Left menu:
     - Check the "enable" box to start logging.
     - Do whatever you want to test on the car.
     - Uncheck the box at the end.
     - Press **Send Logs** — send the archive to your computer.
3. On the computer:
   - Download the scripts from this repository (see instructions below).
   - Extract the `ScanMyOpel_Logging_Global__[date_time].smo` files from the `.zip` archive (sent from the phone) and place them next to the scripts.
   - Two script options are available:
     - `smo_decode` 0.1.4 — a simple decoder to `.txt`, just raw decoding.
     - `smo_decode_plus` 0.2.13 — removes garbage, builds tables and graphs. Supports output to `.txt` (sparklines) and `.xlsx` (Excel with colored charts).
   - `.py` files are the scripts themselves, `.bat` files are for running on Windows via double-click.

---

## ⬇️ How to download the scripts

Since this is an open code repository, you can download the program in two ways:

### Method 1: Download ZIP archive (Easiest, for everyone)
1. On the main project page (click the GitHub logo in the top left corner to go to the repository root).
2. Find the green **`<> Code`** button and click it.
3. In the appearing menu, select **`Download ZIP`**.
4. The `smo_decode-main.zip` archive will be downloaded. Extract it to any folder on your computer (e.g., Desktop).
5. Inside the extracted folder, you will find the required `.py` and `.bat` files.

### Method 2: Via Git (For advanced users)
If you have Git installed, run in the terminal:
```bash
git clone https://github.com/tabookot/smo_decode.git
```

---

## 📖 Detailed Usage Instructions

The `smo_decode_plus` script reads the proprietary log files of the [ScanMyOpel](https://scanmyopel.com) app (`*.smo`), decodes them, cleans them from service garbage, and combines repeated polling cycles into a single table.

Two output formats are available (set by `--txt` or `--xlsx` keys):
- **Text (`.txt`)**: builds pseudo-tables and text graphs (sparklines) for numeric parameters.
- **Excel (`.xlsx`)**: generates a transposed Live Data table and builds visual charts.

### 1. System Requirements
- **OS:** Windows, macOS, or Linux.
- **Python:** version 3.6 or higher.
- **Additional libraries:** NOT REQUIRED for basic `.txt` output. To generate Excel reports (`.xlsx`), the `openpyxl` module is needed (the script will offer to install it automatically on the first run with the `--xlsx` key).

### 2. Python Installation

#### 💻 For Windows:
1. Go to the official website: https://www.python.org/downloads/
2. Download the latest version of Python 3 ("Download Python 3.x.x" button).
3. Run the downloaded installer.
4. ⚠️ **IMPORTANT:** At the bottom of the installer window, make sure to check the **"Add python.exe to PATH"** box.
5. Click "Install Now" and wait for the installation to finish.

#### 🍎 For macOS:
1. Open the "Terminal" app (`Command + Space` ➔ Terminal).
2. If you have the Homebrew package manager installed (recommended), run the command:
   ```bash
   brew install python
   ```
3. If you don't have Homebrew, download the installer from https://www.python.org/downloads/ and install it as a regular application.

#### 🐧 For Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3
```

#### 🐧 For Linux (Fedora/RHEL):
```bash
sudo dnf install python3
```

### 3. File Preparation
1. If you downloaded the ZIP archive (see "How to download" section), extract it to a convenient folder (e.g., `OpelLogs` on your Desktop).
2. Copy the log files from the ScanMyOpel app (files with the `.smo` extension) and place them in the same folder, next to the `smo_decode_plus.py` and `smo_decode.py` scripts.

### 4. Running the Script

You need to open a Terminal (in Windows — "Command Prompt" or "PowerShell", in macOS/Linux — "Terminal") and navigate to your folder.

#### Method A: Decode ALL `.smo` files in the folder at once
*(The script will automatically find all `.smo` files next to itself)*

1. In the terminal, navigate to the folder with the script using the `cd` command:
   ```bash
   cd %USERPROFILE%\Desktop\OpelLogs
   ```
2. Run the script:
   ```bash
   # Windows (simple text output)
   python smo_decode_plus.py
   ```
   ```bash
   # Windows (Excel output with charts)
   python smo_decode_plus.py --xlsx
   ```

   ```bash
   # macOS / Linux (simple text output in Russian)
   python3 smo_decode_plus.py -l ru
   ```

#### Method B: Decode only ONE specific file

1. In the terminal, navigate to the folder with the script (see step 1 above).
2. Run the script, specifying the file name:
   ```bash
   # Windows
   python smo_decode_plus.py my_log.smo
   ```

   ```bash
   # macOS / Linux
   python3 smo_decode_plus.py my_log.smo
   ```

> 💡 **TIP:** You can also add the `-l ru` or `-l en` key to select the language of the headers in the report (defaults to `en`).

### 5. Where to find the result?

After successful execution of the script, new report files with the same name but with a `.txt` extension (by default) or `.xlsx` (if run with the `--xlsx` key) will appear in the same folder.

For example, if you processed the `log_2023.smo` file, a `log_2023.txt` or `log_2023.xlsx` file will appear next to it. Open it in any text editor ("Notepad", Notepad++) or in Microsoft Excel / LibreOffice Calc.

> 💡 **TIP:** For convenient viewing of text tables without column distortion, open the file in editors with a monospaced font (e.g., Notepad++, VS Code, or standard Notepad) and disable word wrap.

### 6. Possible Issues

**Error:** `python: command not found` or `python is not recognized`
**Solution:** You didn't check the "Add to PATH" box during Python installation (on Windows). Alternatively, use the `python3` command instead of `python`.

**Error:** `FileNotFoundError`
**Solution:** You are trying to run the script from the wrong folder where the `.smo` files are not located, or you specified the file name incorrectly.

**Error:** `openpyxl` installation error when running with `--xlsx`
**Solution:** Make sure you have internet access, or install the library manually with the command:
   ```bash
   pip install openpyxl
   ```

> ⚠️ **NOTE ON LOG CONTENTS:**
> If the ScanMyOpel app log only recorded "raw" data (lines like `80 F1 18 22 61 01...`) without text parameter names, the script will process such a log, but the "Live Data" section will be empty because the app failed to record the parameter names.