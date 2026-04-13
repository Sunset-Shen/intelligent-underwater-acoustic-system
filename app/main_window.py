from __future__ import annotations

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from app.pages.data_page import DataPage
from app.pages.generation_page import GenerationPage
from app.pages.home_page import HomePage
from app.pages.recognition_page import RecognitionPage
from app.services.mock_data_service import MockDataService
from app.styles.theme import APP_STYLE
from app.widgets.nav_button import NavButton


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("智能水声数据生成及轻量化识别系统")
        self.resize(1340, 860)

        self.mock_data = MockDataService().load()
        self.setStyleSheet(APP_STYLE)
        self._setup_ui()

    def _setup_ui(self) -> None:
        app_shell = QFrame()
        app_shell.setObjectName("AppShell")

        layout = QVBoxLayout(app_shell)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        layout.addWidget(self._build_top_header())

        body = QHBoxLayout()
        body.setSpacing(12)

        body.addWidget(self._build_sidebar(), 0)

        self.page_stack = QStackedWidget()
        self.home_page = HomePage(self.mock_data, self._show_placeholder_message)
        self.page_stack.addWidget(self.home_page)
        self.data_page = DataPage(self.mock_data["data_page"])
        self.page_stack.addWidget(self.data_page)
        self.generation_page = GenerationPage(self.mock_data["generation_page"])
        self.page_stack.addWidget(self.generation_page)
        self.recognition_page = RecognitionPage(self.mock_data["recognition_page"])
        self.page_stack.addWidget(self.recognition_page)
        self.page_stack.addWidget(self._build_placeholder_page("结果中心模块即将完善"))
        body.addWidget(self.page_stack, 1)

        layout.addLayout(body, 1)
        self.setCentralWidget(app_shell)

    def _build_top_header(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("TopHeader")

        row = QHBoxLayout(frame)
        row.setContentsMargins(18, 14, 18, 14)
        row.setSpacing(12)

        left = QVBoxLayout()
        title = QLabel("智能水声数据生成及轻量化识别系统")
        title.setObjectName("SystemTitle")
        subtitle = QLabel("面向水声目标识别的生成增强与轻量识别一体化原型系统")
        subtitle.setObjectName("SystemSubtitle")
        left.addWidget(title)
        left.addWidget(subtitle)
        row.addLayout(left, 4)

        middle = QHBoxLayout()
        middle.setSpacing(8)
        for text in self.mock_data["header_tags"]:
            tag = QLabel(text)
            tag.setObjectName("HeaderTag")
            middle.addWidget(tag)
        row.addLayout(middle, 3)

        right = QHBoxLayout()
        right.setSpacing(8)
        self.status_badges: dict[str, QLabel] = {}
        for label in self.mock_data["status_badges"]:
            badge = QLabel(label)
            badge.setObjectName("StatusBadge")
            self.status_badges[label.split("：")[0]] = badge
            right.addWidget(badge)

        row.addLayout(right, 3)
        return frame

    def _build_sidebar(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("Sidebar")
        frame.setFixedWidth(188)

        col = QVBoxLayout(frame)
        col.setContentsMargins(12, 14, 12, 14)
        col.setSpacing(8)

        title = QLabel("导航")
        title.setObjectName("NavTitle")
        col.addWidget(title)

        self.nav_buttons: list[NavButton] = []
        nav_items = [
            ("首页总览", "⌂", 0),
            ("数据管理", "🗂", 1),
            ("可解释生成", "✦", 2),
            ("轻量识别", "◍", 3),
            ("结果中心", "☍", 4),
        ]

        for text, icon, idx in nav_items:
            nav = NavButton(text, icon)
            nav.clicked.connect(lambda i=idx: self._switch_page(i))
            self.nav_buttons.append(nav)
            col.addWidget(nav)

        col.addStretch(1)
        hint = QLabel("论文演示首页\n建议在 125% 缩放下截图")
        hint.setObjectName("SidebarHint")
        hint.setWordWrap(True)
        col.addWidget(hint)

        self._set_active_nav(0)
        return frame

    def _build_placeholder_page(self, text: str) -> QWidget:
        page = QWidget()
        col = QVBoxLayout(page)
        col.setContentsMargins(24, 24, 24, 24)

        box = QFrame()
        box.setObjectName("PlaceholderPanel")

        inner = QVBoxLayout(box)
        inner.setContentsMargins(18, 16, 18, 16)
        inner.setSpacing(8)
        title = QLabel(text)
        title.setObjectName("PlaceholderTitle")
        desc = QLabel("该模块将在后续迭代中接入真实流程，当前保留为论文展示占位页面。")
        desc.setObjectName("PlaceholderDesc")
        desc.setWordWrap(True)

        inner.addWidget(title)
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
        if "系统状态" in self.status_badges:
            self.status_badges["系统状态"].setText(f"系统状态：{text}")
        self._switch_page(target_index)
