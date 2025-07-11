from PySide6.QtCore import  Signal, QObject

class WorkerSignals(QObject):
    progress = Signal(int)
    status = Signal(str)
    finished = Signal(bool, str)
    playlist_progress = Signal(int, int)