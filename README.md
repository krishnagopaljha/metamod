# Meta Mod - Metadata Editor

Meta Mod is a Python-based graphical user interface (GUI) tool for viewing, editing, and managing metadata of various file types. The tool leverages `exiftool` for robust metadata handling.

##Compatibility

This tool has been tested exclusively on Kali Linux and may not function as expected on other operating systems.

## Features

- **View Metadata**: Displays all available metadata of a selected file in a user-friendly table.
- **Add or Update Metadata**: Allows users to add new metadata tags or update existing ones.
- **Rename Metadata Key**: Rename a metadata key while preserving its value.
- **Delete Metadata Tag**: Delete a specific metadata tag from the file.
- **Remove All Metadata**: Wipe all metadata from the file to prevent tracking (with a clear warning prompt).
- **Save File**: Save the updated file to a user-specified location.

## Requirements

This tool is designed to work only on **Kali Linux** and requires the following:

1. **Python 3.x**
2. **tkinter**: For GUI support.
3. **exiftool**: The core tool for metadata handling. Install it using:
   ```bash
   sudo apt update
   sudo apt install exiftool

## How to Use

Clone or download the repository.

1. **Ensure all dependencies are installed.**
2. **Run the tool using**:
   ```bash
   python3 metamod.py
