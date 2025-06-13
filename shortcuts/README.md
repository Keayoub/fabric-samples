# Fabric Shortcuts Automation

This folder contains a PowerShell script (`create-shortcuts.ps1`) to automate the bulk creation of Microsoft Fabric shortcuts to ADLS Gen2 using the fab CLI.

## What does `create-shortcuts.ps1` do?
- Reads shortcut definitions from `shortcuts.csv`.
- Looks up Fabric workspace and lakehouse by name.
- Ensures the destination folder exists (creates it if needed).
- Creates shortcuts in the specified Fabric lakehouse using the fab CLI.
- Provides error and debug output for each operation.

## Prerequisites
- **Microsoft Fabric CLI (fab CLI)** must be installed and authenticated.
- You must have Contributor or Admin permissions on the target workspace and lakehouse.
- A valid `shortcuts.csv` file with the following columns:
  - `location`, `subpath`, `connectionId`, `workspace`, `lakehouse`, `target`, `shortcutName`

## How to install fab CLI

You can install the fab CLI using either npm (Node.js) or pip (Python):

### Option 1: Install with npm (Node.js)
1. Install Node.js (if not already installed):
   - Download from https://nodejs.org/
2. Install fab CLI globally:
   ```sh
   npm install -g @microsoft/fabric-cli
   ```

### Option 2: Install with pip (Python)
1. Install Python 3.10, 3.11, or 3.12 (if not already installed):
   - Download from https://www.python.org/downloads/
2. Install fab CLI globally:
   ```sh
   pip install ms-fabric-cli
   ```
   To upgrade:
   ```sh
   pip install --upgrade ms-fabric-cli
   ```

3. Authenticate with your Fabric account:
   ```sh
   fab auth login
   ```

## How to use the script

1. Place your shortcut definitions in a CSV file (see the sample in this folder).
2. Open a PowerShell terminal in this folder.
3. Run the script, specifying your CSV file if not using the default:
   ```powershell
   ./create-shortcuts.ps1 -CsvPath shortcuts.csv
   ```
   If you omit `-CsvPath`, the script will use `shortcuts.csv` by default.

The script will process each row in the CSV and create the corresponding shortcut in Fabric.

---

For more details on fab CLI, see: <https://www.npmjs.com/package/@microsoft/fabric-cli>
Official docs: <https://microsoft.github.io/fabric-cli/>
