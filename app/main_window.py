from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.pages.home_page import HomePage
from app.services.mock_data_service import MockDataService
from app.styles.theme import APP_STYLE
from app.widgets.nav_button import NavButton


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("智能水声数据生成及轻量化识别系统")
        self.resize(1360, 860)

        self.mock_data = MockDataService().load()
        self.setStyleSheet(APP_STYLE)

        self._setup_ui()

    def _setup_ui(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        layout.addWidget(self._build_top_header())

        body_row = QHBoxLayout()
        body_row.setSpacing(12)
        body_row.addWidget(self._build_sidebar(), 0)

        self.page_stack = QStackedWidget()
        self.home_page = HomePage(self.mock_data, self._show_placeholder_message)
        body_row.addWidget(self.page_stack, 1)

        self.page_stack.addWidget(self.home_page)
        self.page_stack.addWidget(self._build_placeholder_page("数据管理模块即将完善"))
        self.page_stack.addWidget(self._build_placeholder_page("可解释生成模块即将完善"))
        self.page_stack.addWidget(self._build_placeholder_page("轻量识别模块即将完善"))
        self.page_stack.addWidget(self._build_placeholder_page("结果中心模块即将完善"))

        layout.addLayout(body_row, 1)
        self.setCentralWidget(root)

    def _build_top_header(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("TopHeader")

        row = QHBoxLayout(frame)
        row.setContentsMargins(20, 16, 20, 16)

        title_col = QVBoxLayout()
        title = QLabel("智能水声数据生成及轻量化识别系统")
        title.setObjectName("SystemTitle")
        subtitle = QLabel("面向水声目标识别的生成增强与轻量识别一体化原型系统")
        subtitle.setObjectName("SystemSubtitle")
        title_col.addWidget(title)
        title_col.addWidget(subtitle)

        row.addLayout(title_col)
        row.addStretch(1)

        self.status_label = QLabel("系统状态：稳定")
        self.status_label.setObjectName("StatusBadge")
        row.addWidget(self.status_label, 0, Qt.AlignmentFlag.AlignTop)

        return frame

    def _build_sidebar(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("Sidebar")
        frame.setFixedWidth(230)

        col = QVBoxLayout(frame)
        col.setContentsMargins(14, 18, 14, 18)
        col.setSpacing(10)

        section_title = QLabel("功能导航")
        section_title.setObjectName("NavTitle")
        col.addWidget(section_title)

        self.nav_buttons: list[NavButton] = []
        nav_items = [
            ("首页总览", 0),
            ("数据管理", 1),
            ("可解释生成", 2),
            ("轻量识别", 3),
            ("结果中心", 4),
        ]

        for text, idx in nav_items:
            button = NavButton(text)
            button.clicked.connect(lambda _, i=idx: self._switch_page(i))
            self.nav_buttons.append(button)
            col.addWidget(button)

        col.addStretch(1)

        tip = QLabel("当前任务：主界面原型联调")
        tip.setWordWrap(True)
        tip.setObjectName("SidebarTip")
        col.addWidget(tip)

        self._set_active_nav(0)
        return frame

    def _build_placeholder_page(self, text: str) -> QWidget:
        page = QWidget()
        col = QVBoxLayout(page)
        col.setContentsMargins(24, 24, 24, 24)

        box = QFrame()
        box.setObjectName("PlaceholderPanel")
        inner = QVBoxLayout(box)
        label = QLabel(text)
        label.setObjectName("PlaceholderTitle")
        desc = QLabel("该模块正在设计中，本轮优先完成主界面视觉与交互框架。")
        desc.setWordWrap(True)
        desc.setObjectName("PlaceholderDesc")
        inner.addWidget(label)
        inner.addWidget(desc)

        col.addWidget(box)
        col.addStretch(1)
        return page

    def _switch_page(self, index: int) -> None:
        self.page_stack.setCurrentIndex(index)
        self._set_active_nav(index)

    def _set_active_nav(self, active_idx: int) -> None:
        for idx, button in enumerate(self.nav_buttons):
            button.set_active(idx == active_idx)

    def _show_placeholder_message(self, text: str, target_index: int) -> None:
        self.status_label.setText(f"当前任务：{text}")
        self._switch_page(target_index)
