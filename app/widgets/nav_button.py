from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton


class NavButton(QPushButton):
    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        self.setObjectName("NavButton")

    def set_active(self, active: bool) -> None:
        self.setChecked(active)
