# BC Dashboard Suite - Windows Setup (One Page)

This guide is for non-technical users.

## 1. Install Python (one-time)
1. Go to: `https://www.python.org/downloads/windows/`
2. Download and install Python 3.11+.
3. In the installer, check: **Add Python to PATH**.
4. Finish install.

If Python is already installed, skip install and do this:
1. Open **Start** -> search **Environment Variables** -> open **Edit the system environment variables**.
2. Click **Environment Variables...**
3. Under **User variables**, select **Path** -> **Edit** -> **New**
4. Add your Python folders (example):
   - `C:\Users\<YourUser>\AppData\Local\Programs\Python\Python311\`
   - `C:\Users\<YourUser>\AppData\Local\Programs\Python\Python311\Scripts\`
5. Click **OK** on all windows.
6. Re-open Command Prompt and run: `python -V`

## 2. Copy the app to your laptop
1. Receive the `BCLS_Dashboard_App.zip` file.
2. Right-click it -> **Extract All...**
3. Open the extracted folder.

## 3. Start the dashboard app
1. Double-click: `BC_Dashboard_App.bat`
2. Your browser opens the BC Dashboard Hub automatically.
3. Keep the black terminal window open while using the dashboards.
4. If you see an `openpyxl` error, run this once in Command Prompt:
   - `python -m pip install openpyxl`

## 4. Connect confidential SharePoint Excel data (required)
When `scripts/serve.py` runs for the first time, it creates:
`%USERPROFILE%\BCLS\DATA_FILE_MAP.xlsx`

Open that file and fill these keys with your local synced SharePoint file paths:
- `life_sciences_main`
- `look_west_media`
- `look_west_funding`

If paths are blank or invalid, those dashboards show **Data not connected**.

## 5. Stop the app
1. Click the terminal window.
2. Press `Ctrl + C`.
3. Close the terminal window.

## 6. If it does not start
1. Re-open `BC_Dashboard_App.bat`.
2. If you see a Python error:
   - Reinstall Python and make sure **Add Python to PATH** is selected.
   - If already installed, add Python to `Path` (steps above), then retry.
3. If you see `ModuleNotFoundError: openpyxl`:
   - Run: `python -m pip install openpyxl`
4. If Windows Firewall asks for access:
   - Click **Allow access** (Private networks).
