from PySide6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QHBoxLayout)
import threading
import sqlite3
class HistoryDialog(QDialog):
    _instance = None
    _lock = threading.Lock()
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if not hasattr(self, "_initialized"):  # Prevent reinitialization
            super().__init__(parent)
            self._initialized = True
            self.setWindowTitle("Download History")
            self.setMinimumSize(600, 400)
            
            layout = QVBoxLayout()
            
            # Create table
            self.table = QTableWidget()
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(["Title", "URL", "Format", "Output Path", "Date"])
            self.table.horizontalHeader().setStretchLastSection(True)
            layout.addWidget(self.table)
            
            # Buttons
            button_layout = QHBoxLayout()
            self.clear_button = QPushButton("Clear History")
            self.close_button = QPushButton("Close")
            button_layout.addWidget(self.clear_button)
            button_layout.addWidget(self.close_button)
            layout.addLayout(button_layout)
            
            self.setLayout(layout)
            
            # Connect signals
            self.close_button.clicked.connect(self.accept)
        
    def populate_table(self, history_data):
        if not history_data:
            self.table.setRowCount(0)
            return

        # Dynamically adjust the table to the number of columns in the data
        column_count = len(history_data[0])
        self.table.setColumnCount(column_count)
        self.table.setRowCount(len(history_data))

        # Set headers dynamically based on the number of columns
        headers = ["Title", "URL", "Format", "Quality", "Output Path", "Date", "Status", "Download Count"]
        self.table.setHorizontalHeaderLabels(headers[:column_count])

        for row, record in enumerate(history_data):
            for col, value in enumerate(record[1:]):  # Skip the first column
               self.table.setItem(row, col, QTableWidgetItem(str(value)))
