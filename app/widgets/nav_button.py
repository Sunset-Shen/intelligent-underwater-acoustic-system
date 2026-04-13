from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton


class NavButton(QFrame):
    clicked = pyqtSignal()

    def __init__(self, text: str, icon: str) -> None:
        super().__init__()
        self._active = False

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)

        self.indicator = QFrame()
        self.indicator.setObjectName("NavIndicator")
        self.indicator.setFixedWidth(4)
        self.indicator.setVisible(False)

        self.button = QPushButton(f"{icon}  {text}")
        self.button.setCheckable(True)
        self.button.setObjectName("NavButton")
        self.button.clicked.connect(self.clicked.emit)

        row.addWidget(self.indicator)
        row.addWidget(self.button, 1)

    def set_active(self, active: bool) -> None:
        self._active = active
        self.indicator.setVisible(active)
        self.button.setChecked(active)

    def setEnabled(self, enabled: bool) -> None:  # noqa: N802
        self.button.setEnabled(enabled)
        super().setEnabled(enabled)
