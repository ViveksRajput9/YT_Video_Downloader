from PySide6.QtWidgets import QMessageBox, QInputDialog, QWidget
import os
from config.config_manager import Config_Manager

class CheckDuplicates:
    def __init__(self, parent: QWidget, ydl_opts: dict, video_data: dict):
        self.parent = parent
        self.ydl_opts = ydl_opts
        self.video_data = video_data

        self.output_folder = os.path.normpath(Config_Manager().get_download_path())
        filename, ext = os.path.splitext(video_data.get('filename', ''))

        existing_file = self.check_duplicate(filename)
        print(existing_file)
        if existing_file:
            choice = self.ask_user(existing_file)
            if choice == "auto":
                new_filename = self.get_unique_filename(filename, ext)
                self.set_output_path(new_filename)
            elif choice == "manual":
                self.prompt_manual_rename(filename, ext)
            else:
                self.parent.status = False
        else:
            self.set_output_path(filename + ext)

    def check_duplicate(self, filename: str) -> str:
        """Checks for duplicate files with common extensions."""
        possible_exts = ['.mp4', '.webm', '.mkv', '.mp3']
        return next(
            (os.path.join(self.output_folder, filename + e) 
             for e in possible_exts if os.path.exists(os.path.join(self.output_folder, filename + e))),
            None
        )

    def ask_user(self, existing_file: str) -> str:
        box = QMessageBox(self.parent.parent)
        box.setWindowTitle("File Exists")
        box.setText(f"'{os.path.basename(existing_file)}' already exists.\nDownload with a different name?")
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        box.setButtonText(QMessageBox.Yes, "Auto Rename")
        box.setButtonText(QMessageBox.No, "Manual Rename")
        result = box.exec()

        if result == QMessageBox.Yes:
            return "auto"
        elif result == QMessageBox.No:
            return "manual"
        else:
            return "cancel"

    def prompt_manual_rename(self, base: str, ext: str):
        name, ok = QInputDialog.getText(self.parent.parent, "Rename File", "Enter new filename (without extension):")
        if ok and name:
            new_filename = self.get_unique_filename(name, ext)
            self.set_output_path(new_filename)
        else:
            self.parent.status = False

    def get_unique_filename(self, base: str, ext: str) -> str:

        counter = 1
        candidate = f"{base}"
        while self.check_duplicate(candidate):
            candidate = f"{base}_{counter}"
            counter += 1
        return candidate

    def set_output_path(self, final_filename: str):
        full_path = os.path.join(self.output_folder, final_filename)
        self.ydl_opts['outtmpl'] = full_path  # Set full path
        self.video_data['filename'] = final_filename  # Save it for reference
        print(f"Using filename: {final_filename}")