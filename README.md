# Hashcat Advanced GUI

A sleek, modern, and user-friendly Graphical User Interface for Hashcat, built with Python and PyQt6. This tool is designed to make password cracking, specifically for Wi-Fi (WPA/WPA2) handshakes, accessible and visually appealing.

![Screenshot](screenshot.png)

## Features
- **Dark Theme:** Modern aesthetic that's easy on the eyes.
- **Portable:** Includes everything needed out of the box (requires no installation if using the release `.exe`).
- **Dynamic Wordlists:** Supports selecting and combining multiple dictionaries simultaneously.
- **Smart Output:** Real-time, color-coded terminal output inside the GUI. Successfully cracked passwords are highlighted in bright green!

## 🚀 How to Use (For Windows Users)

### The Easy Way (Pre-compiled)
1. Go to the [Releases page](../../releases) and download `HashcatGUI.exe`.
2. Place the `.exe` in a folder (for example, `C:\HashcatGUI`).
3. Make sure you have the `hashcat_core` and `wordlists` folders next to your `.exe` (you can download the source code `.zip` for these folders).
4. Run `HashcatGUI.exe`.

### How to Crack a Wi-Fi Password:
1. **Get your Hash:** You need a `.hc22000` file. If you have a `.pcap` or `.cap` file from a Wi-Fi handshake capture, convert it using the official [Hashcat Online Converter](https://hashcat.net/cap2hashcat/).
2. **Select Hash:** In the GUI, click "Browse" next to Hash File and select your `.hc22000` file.
3. **Select Dictionaries:** Click "Browse" next to Wordlist(s) and pick one or more `.txt` files containing passwords (e.g., from the `wordlists` folder).
4. **Start Attack:** Click the green **Start Attack** button and wait for the results!

---

## 🛠️ For Developers (Running from Source)

If you prefer to run the Python script directly or modify the code:

### Prerequisites
You need Python 3 installed.

1. **Clone the repository:**
```bash
git clone https://github.com/homychokk/HashCatGuiV2.git
cd HashCatGuiV2
```

2. **Install requirements:**
```bash
pip install -r requirements.txt
```

3. **Run the GUI:**
```bash
python hashcat_core/hashcat_pyqt.py
```

### Folder Structure
* `hashcat_core/` - Contains the actual Hashcat executable, kernels, and the Python GUI script.
* `wordlists/` - A dedicated folder for your password dictionaries.
* `screenshot.png` - Preview image.
* `requirements.txt` - Python dependencies.
