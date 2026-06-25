import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, 
                             QTextEdit, QFileDialog, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QTextCharFormat, QIcon

class WorkerSignals(QThread):
    output_ready = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = None

    def run(self):
        try:
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            for line in iter(self.process.stdout.readline, ''):
                self.output_ready.emit(line)
            self.process.stdout.close()
            self.process.wait()
        except Exception as e:
            self.output_ready.emit(f"Error starting process: {e}")
        finally:
            self.finished.emit()

    def stop(self):
        if self.process:
            self.process.terminate()

class HashcatGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hashcat Professional GUI")
        self.setMinimumSize(800, 650)

        # Support PyInstaller path or normal script path
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.hashcat_path = os.path.join(base_dir, "hashcat_core", "hashcat.exe")
        
        self.worker = None
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("Hashcat Password Cracker")
        title.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #00FF00;")
        main_layout.addWidget(title)

        # Hash Type
        hash_layout = QHBoxLayout()
        hash_layout.addWidget(QLabel("Hash Type (m):"))
        self.hash_type_combo = QComboBox()
        self.hash_type_combo.addItems([
            "0 - MD5", 
            "100 - SHA1", 
            "1400 - SHA256", 
            "1000 - NTLM", 
            "22000 - WPA-PBKDF2-PMKID+EAPOL (Wi-Fi)"
        ])
        hash_layout.addWidget(self.hash_type_combo)
        main_layout.addLayout(hash_layout)

        # Attack Mode
        attack_layout = QHBoxLayout()
        attack_layout.addWidget(QLabel("Attack Mode (a):"))
        self.attack_mode_combo = QComboBox()
        self.attack_mode_combo.addItems([
            "0 - Straight (Dictionary)",
            "3 - Brute-force"
        ])
        attack_layout.addWidget(self.attack_mode_combo)
        main_layout.addLayout(attack_layout)

        # Target Hash/File
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Target Hash / File:"))
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter hash here or browse for a file (.hc22000)...")
        target_layout.addWidget(self.target_input)
        
        target_btn = QPushButton("Browse")
        target_btn.clicked.connect(self.browse_target)
        target_layout.addWidget(target_btn)
        main_layout.addLayout(target_layout)

        # Wordlist
        wordlist_layout = QHBoxLayout()
        wordlist_layout.addWidget(QLabel("Wordlist(s):"))
        self.wordlist_input = QLineEdit()
        self.wordlist_input.setPlaceholderText("Select wordlists for dictionary attack...")
        wordlist_layout.addWidget(self.wordlist_input)
        
        wordlist_btn = QPushButton("Browse")
        wordlist_btn.clicked.connect(self.browse_wordlists)
        wordlist_layout.addWidget(wordlist_btn)
        main_layout.addLayout(wordlist_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("START ATTACK")
        self.start_btn.setStyleSheet("background-color: #005500; color: #00FF00; font-weight: bold; padding: 10px;")
        self.start_btn.clicked.connect(self.start_attack)
        
        self.stop_btn = QPushButton("STOP")
        self.stop_btn.setStyleSheet("background-color: #550000; color: #FF0000; font-weight: bold; padding: 10px;")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_attack)
        
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        main_layout.addLayout(btn_layout)

        # Log Output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Consolas", 10))
        self.log_output.setStyleSheet("background-color: #1E1E1E; color: #CCCCCC;")
        main_layout.addWidget(self.log_output)

        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #FFFFFF; }
            QLineEdit, QComboBox { background-color: #2D2D2D; color: #FFFFFF; border: 1px solid #555555; padding: 5px; }
            QPushButton { background-color: #333333; color: #FFFFFF; border: 1px solid #555; padding: 5px; }
            QPushButton:hover { background-color: #444444; }
        """)

    def browse_target(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Hash File", "", "All Files (*)")
        if filename:
            self.target_input.setText(filename)

    def browse_wordlists(self):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
        wordlist_dir = os.path.join(base_dir, "wordlists")
        if not os.path.exists(wordlist_dir):
            wordlist_dir = base_dir

        filenames, _ = QFileDialog.getOpenFileNames(self, "Select Wordlists", wordlist_dir, "Text Files (*.txt);;All Files (*)")
        if filenames:
            self.wordlist_input.setText(" ".join([f'"{f}"' for f in filenames]))

    def start_attack(self):
        if not os.path.exists(self.hashcat_path):
            QMessageBox.critical(self, "Error", f"Hashcat core not found at: {self.hashcat_path}\\nPlease make sure the hashcat_core folder is present.")
            return

        hash_type = self.hash_type_combo.currentText().split(" - ")[0]
        attack_mode = self.attack_mode_combo.currentText().split(" - ")[0]
        target = self.target_input.text().strip()
        wordlists = self.wordlist_input.text().strip()

        if not target:
            QMessageBox.warning(self, "Warning", "Please specify a target hash or file.")
            return

        command = [self.hashcat_path, "-m", hash_type, "-a", attack_mode, target]
        if attack_mode == "0":
            if not wordlists:
                QMessageBox.warning(self, "Warning", "Dictionary attack requires a wordlist.")
                return
            
            import shlex
            command.extend(shlex.split(wordlists))

        self.log_output.clear()
        self.append_log(f"[*] Starting attack with command: {' '.join(command)}\\n", "#00FFFF")
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        self.worker = WorkerSignals(command)
        self.worker.output_ready.connect(self.handle_output)
        self.worker.finished.connect(self.attack_finished)
        self.worker.start()

    def handle_output(self, line):
        color = "#CCCCCC"
        if "Status" in line:
            if "Cracked" in line:
                self.append_log("\\n[!!!] SUCCESS! PASSWORD CRACKED:\\n", "#00FF00")
                color = "#00FF00"
            elif "Exhausted" in line:
                color = "#FFA500"
        
        self.append_log(line, color)

    def append_log(self, text, color):
        cursor = self.log_output.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_output.setTextCursor(cursor)

        format = QTextCharFormat()
        format.setForeground(QColor(color))
        
        if color == "#00FF00":
            format.setFontWeight(QFont.Weight.Bold)

        cursor.insertText(text, format)
        self.log_output.ensureCursorVisible()

    def stop_attack(self):
        if self.worker:
            self.worker.stop()
            self.append_log("\\n[*] Attack stopped by user.\\n", "#FF0000")

    def attack_finished(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.append_log("\\n[*] Process finished.\\n", "#00FFFF")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set icon if available
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        
    window = HashcatGUI()
    window.show()
    sys.exit(app.exec())
