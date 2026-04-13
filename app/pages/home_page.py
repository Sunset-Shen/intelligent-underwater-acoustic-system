from __future__ import annotations

from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class HomePage(QWidget):
    def __init__(self, data: dict, on_feature_click: Callable[[str, int], None]) -> None:
        super().__init__()
        self.data = data
        self.on_feature_click = on_feature_click
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        root.addWidget(self._build_hero_section())
        root.addWidget(self._build_feature_cards())
        root.addWidget(self._build_overview_section())
        root.addWidget(self._build_recent_results())
        root.addStretch(1)

    def _build_hero_section(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(22, 20, 22, 20)
        col.setSpacing(14)

        title = QLabel("水声智能处理一体化工作台")
        title.setObjectName("HeroTitle")
        desc = QLabel("围绕“数据-生成-识别-管理”全流程，提供清晰、可扩展、面向研究落地的统一界面。")
        desc.setWordWrap(True)
        desc.setObjectName("HeroDesc")
        col.addWidget(title)
        col.addWidget(desc)

        flow_row = QHBoxLayout()
        flow_row.setSpacing(8)
        for idx, item in enumerate(self.data["flow_steps"], start=1):
            flow_row.addWidget(self._flow_card(idx, item), 1)
        col.addLayout(flow_row)

        return panel

    def _flow_card(self, idx: int, text: str) -> QFrame:
        card = QFrame()
        card.setObjectName("FlowCard")
        row = QHBoxLayout(card)
        row.setContentsMargins(10, 10, 10, 10)
        row.setSpacing(8)

        num = QLabel(str(idx))
        num.setObjectName("FlowNumber")
        label = QLabel(text)
        label.setWordWrap(True)
        label.setObjectName("FlowLabel")

        row.addWidget(num, 0, Qt.AlignmentFlag.AlignTop)
        row.addWidget(label, 1)
        return card

    def _build_feature_cards(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        grid = QGridLayout(panel)
        grid.setContentsMargins(16, 16, 16, 16)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        mapping = {
            "数据管理": 1,
            "可解释生成": 2,
            "轻量识别": 3,
            "结果中心": 4,
        }

        for i, card in enumerate(self.data["feature_cards"]):
            btn = QPushButton()
            btn.setObjectName("FeatureCard")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(118)
            btn.setText(f"{card['icon']}  {card['title']}\n{card['description']}")
            btn.clicked.connect(lambda _, c=card: self.on_feature_click(f"{c['title']}模块即将完善", mapping[c['title']]))
            grid.addWidget(btn, i // 2, i % 2)

        return panel

    def _build_overview_section(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 16, 16, 16)

        title = QLabel("系统概览")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        for i, item in enumerate(self.data["overview_items"]):
            box = QFrame()
            box.setObjectName("OverviewItem")
            inner = QVBoxLayout(box)
            inner.setContentsMargins(12, 10, 12, 10)
            label = QLabel(item["label"])
            label.setObjectName("OverviewLabel")
            value = QLabel(item["value"])
            value.setObjectName("OverviewValue")
            sub = QLabel(item["sub"])
            sub.setObjectName("OverviewSub")
            sub.setWordWrap(True)
            inner.addWidget(label)
            inner.addWidget(value)
            inner.addWidget(sub)
            grid.addWidget(box, i // 2, i % 2)

        col.addLayout(grid)
        return panel

    def _build_recent_results(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 16, 16, 16)

        title = QLabel("最近结果预览")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        for item in self.data["recent_results"]:
            row = QFrame()
            row.setObjectName("ResultItem")
            inner = QVBoxLayout(row)
            inner.setContentsMargins(12, 10, 12, 10)
            heading = QLabel(item["title"])
            heading.setObjectName("ResultTitle")
            summary = QLabel(item["summary"])
            summary.setWordWrap(True)
            summary.setObjectName("ResultSummary")
            tag = QLabel(item["tag"])
            tag.setObjectName("ResultTag")
            inner.addWidget(heading)
            inner.addWidget(summary)
            inner.addWidget(tag)
            col.addWidget(row)

        return panel
