from __future__ import annotations

from functools import partial
from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


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
        root.addWidget(self._build_process_section())
        root.addWidget(self._build_module_section())
        root.addWidget(self._build_status_recent_section())

    def _build_hero_section(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("HeroPanel")

        row = QHBoxLayout(panel)
        row.setContentsMargins(20, 18, 20, 18)
        row.setSpacing(18)

        left = QVBoxLayout()
        title = QLabel("水声智能处理一体化工作台")
        title.setObjectName("HeroTitle")
        desc = QLabel(
            "围绕“数据接入—生成增强—识别推理—结果管理”全流程，"
            "提供统一、清晰、可扩展的科研原型界面。"
        )
        desc.setWordWrap(True)
        desc.setObjectName("HeroDesc")

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        data_btn = QPushButton("进入数据管理")
        data_btn.setObjectName("HeroAction")
        data_btn.clicked.connect(partial(self.on_feature_click, "数据管理模块即将完善", 1))

        result_btn = QPushButton("查看结果中心")
        result_btn.setObjectName("HeroGhostAction")
        result_btn.clicked.connect(partial(self.on_feature_click, "结果中心模块即将完善", 4))

        btn_row.addWidget(data_btn)
        btn_row.addWidget(result_btn)
        btn_row.addStretch(1)

        left.addWidget(title)
        left.addWidget(desc)
        left.addLayout(btn_row)
        left.addStretch(1)

        wave = self._build_wave_panel()

        row.addLayout(left, 3)
        row.addWidget(wave, 2)

        return panel

    def _build_wave_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("WavePanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(12, 10, 12, 10)

        title = QLabel("水声流程示意")
        title.setObjectName("SectionTitle")
        sub = QLabel("波形特征 → 频谱增强 → UT-EAT 识别")
        sub.setObjectName("SectionSub")

        waveform = QLabel("~∿~~∿∿~  ···  ≋≋≋  ···  █▆▄▂▂▄▆█")
        waveform.setAlignment(Qt.AlignmentFlag.AlignCenter)
        waveform.setStyleSheet("font-size: 16px; color: #2f628f; letter-spacing: 1px;")

        mel = QLabel("Mel 频谱占位：▁▂▃▄▅▆▇█  →  条件增强  →  分类输出")
        mel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mel.setStyleSheet("color: #5f7b95; font-size: 12px;")

        col.addWidget(title)
        col.addWidget(sub)
        col.addStretch(1)
        col.addWidget(waveform)
        col.addWidget(mel)
        col.addStretch(1)
        return panel

    def _build_process_section(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 16)
        col.setSpacing(10)

        title = QLabel("系统流程")
        title.setObjectName("SectionTitle")
        subtitle = QLabel("数据接入与预处理 → 可解释生成与增强 → 轻量识别训练 / 推理 → 结果输出与管理")
        subtitle.setObjectName("SectionSub")

        row = QHBoxLayout()
        row.setSpacing(8)
        for idx, step in enumerate(self.data["process_items"], start=1):
            row.addWidget(self._build_process_item(idx, step), 1)

        col.addWidget(title)
        col.addWidget(subtitle)
        col.addLayout(row)
        return panel

    def _build_process_item(self, idx: int, step: dict) -> QFrame:
        item = QFrame()
        item.setObjectName("FlowItem")

        col = QVBoxLayout(item)
        col.setContentsMargins(10, 10, 10, 10)
        col.setSpacing(4)

        top = QHBoxLayout()
        top.setSpacing(6)
        index = QLabel(str(idx))
        index.setObjectName("FlowIndex")
        icon = QLabel(step["icon"])
        icon.setStyleSheet("font-size: 14px; color: #2a6299;")
        top.addWidget(index)
        top.addWidget(icon)
        top.addStretch(1)

        title = QLabel(step["title"])
        title.setObjectName("FlowTitle")
        desc = QLabel(step["desc"])
        desc.setWordWrap(True)
        desc.setObjectName("FlowDesc")

        col.addLayout(top)
        col.addWidget(title)
        col.addWidget(desc)
        return item

    def _build_module_section(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")

        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 16)
        col.setSpacing(10)

        title = QLabel("核心模块入口")
        title.setObjectName("SectionTitle")
        subtitle = QLabel("四大模块统一入口，支持后续扩展为完整业务页面")
        subtitle.setObjectName("SectionSub")
        col.addWidget(title)
        col.addWidget(subtitle)

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        for i, card in enumerate(self.data["module_cards"]):
            widget = self._build_module_card(card)
            grid.addWidget(widget, i // 2, i % 2)

        col.addLayout(grid)
        return panel

    def _build_module_card(self, card: dict) -> QFrame:
        panel = QFrame()
        panel.setObjectName("ModuleCard")
        col = QVBoxLayout(panel)
        col.setContentsMargins(14, 12, 14, 12)

        top = QHBoxLayout()
        icon = QLabel(card["icon"])
        icon.setStyleSheet("font-size: 16px; color: #2a6299;")

        title = QLabel(card["title"])
        title.setObjectName("ModuleTitle")

        status = QLabel(card["status"])
        status.setObjectName(card["status_style"])

        top.addWidget(icon)
        top.addWidget(title)
        top.addStretch(1)
        top.addWidget(status)

        desc = QLabel(card["description"])
        desc.setObjectName("ModuleDesc")
        desc.setWordWrap(True)

        enter_btn = QPushButton("进入模块")
        enter_btn.setObjectName("EnterButton")
        enter_btn.clicked.connect(partial(self.on_feature_click, f"{card['title']}模块即将完善", card["target_index"]))

        col.addLayout(top)
        col.addWidget(desc)
        col.addStretch(1)
        col.addWidget(enter_btn, 0, Qt.AlignmentFlag.AlignLeft)
        return panel

    def _build_status_recent_section(self) -> QWidget:
        wrapper = QWidget()
        row = QHBoxLayout(wrapper)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(12)

        row.addWidget(self._build_system_status(), 1)
        row.addWidget(self._build_recent_results(), 1)
        return wrapper

    def _build_system_status(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("StatusCard")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("系统状态概览")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        for item in self.data["system_status"]:
            line = QHBoxLayout()
            key = QLabel(item["label"])
            key.setObjectName("KeyLabel")
            value = QLabel(item["value"])
            value.setObjectName("KeyValue")
            line.addWidget(key)
            line.addStretch(1)
            line.addWidget(value)
            col.addLayout(line)

        return panel

    def _build_recent_results(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("RecentCard")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("最近任务 / 最近结果")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        for item in self.data["recent_records"]:
            card = QFrame()
            card.setObjectName("FlowItem")
            inner = QVBoxLayout(card)
            inner.setContentsMargins(10, 8, 10, 8)
            inner.setSpacing(4)

            row = QHBoxLayout()
            heading = QLabel(item["title"])
            heading.setObjectName("RecentTitle")
            metric = QLabel(item["metric"])
            metric.setObjectName("MetricBadge")
            row.addWidget(heading)
            row.addStretch(1)
            row.addWidget(metric)

            desc = QLabel(item["desc"])
            desc.setObjectName("RecentDesc")
            desc.setWordWrap(True)

            inner.addLayout(row)
            inner.addWidget(desc)
            col.addWidget(card)

        return panel
