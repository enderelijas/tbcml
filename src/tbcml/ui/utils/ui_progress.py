from typing import Callable, Optional

from PyQt5 import QtWidgets

from tbcml.core import io


class ProgressBar(QtWidgets.QWidget):
    def __init__(
        self,
        title: str,
        on_progress: Optional[Callable[[int, int], None]] = None,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super(ProgressBar, self).__init__(parent)
        self.title = title
        self.on_progress = on_progress
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("ProgressBar")
        self.resize(400, 100)

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setObjectName("vertical_layout")

        self.title_label = QtWidgets.QLabel(self)
        self.title_label.setObjectName("title_label")
        self.title_label.setText(self.title)
        self.vertical_layout.addWidget(self.title_label)

        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setTextVisible(False)
        self.vertical_layout.addWidget(self.progress_bar)

        self.progress_label = QtWidgets.QLabel(self)
        self.progress_label.setObjectName("progress_label")
        self.vertical_layout.addWidget(self.progress_label)

    def set_progress(self, current: int, total: int):
        if total <= 0:
            total = 1
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        percent_str = f"{int(current / total * 100)}%"
        self.progress_label.setText(f"{current}/{total} ({percent_str})")
        if self.on_progress:
            self.on_progress(current, total)

    def set_progress_str(self, text: str, current: int, total: int = 100):
        if total <= 0:
            total = 1
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        percent_str = f"{int(current / total * 100)}%"
        self.progress_label.setText(f"{text} ({percent_str})")
        if self.on_progress:
            self.on_progress(current, total)

    def set_progress_full_no_text(self, current: int, total: int):
        if total <= 0:
            total = 1
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(int(current / total * 100))
        if self.on_progress:
            self.on_progress(current, total)

    def set_progress_no_bar(self, current: int, total: int):
        if total <= 0:
            total = 1
        percent_str = f"{int(current / total * 100)}%"
        self.progress_label.setText(f"{current}/{total} ({percent_str})")
        if self.on_progress:
            self.on_progress(current, total)

    def set_progress_file_size(self, current: int, total: int):
        if total <= 0:
            total = 1
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        current_str = io.file_handler.FileSize(current).format()
        total_str = io.file_handler.FileSize(total).format()
        percent_str = f"{int(current / total * 100)}%"
        self.progress_label.setText(f"{current_str}/{total_str} ({percent_str})")
        if self.on_progress:
            self.on_progress(current, total)
