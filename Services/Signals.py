from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QPixmap
class WorkerSignals(QObject):

    finished = Signal(bool,object)  # Signal to emit when the task is finished
    finished = Signal(object)
    error = Signal(str)        # Signal to emit when an error occurs
    progress = Signal(int)     # Signal to emit progress updates
    quality_selector = Signal(object)  # Signal to update quality selector
    channel_name = Signal(str)        # Signal to update channel name
    title = Signal(str)               # Signal to update title
    duration = Signal(int)            # Signal to update duration
    max_quality = Signal(int)         # Signal to update max quality
    video_data = Signal(object)       # Signal to update video data
    thumbnail = Signal(object)  # Signal to update thumbnail
    update_Ui = Signal(object)
    add_SqureWidget = Signal(object)