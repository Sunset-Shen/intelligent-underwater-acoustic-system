from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ResultThumbLabel(QLabel):
    def __init__(self, image_path: str, fallback: str, width: int = 520, height: int = 260) -> None:
        super().__init__()
        raw_path = Path(image_path)
        project_root = Path(__file__).resolve().parents[2]
        self.image_path = raw_path if raw_path.is_absolute() else (project_root / raw_path)
        self.fallback = fallback
        self.width = width
        self.height = height

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("ImagePreview")
        self.setMinimumHeight(height)
        self._load()

    def _load(self) -> None:
        if self.image_path.exists():
            pix = QPixmap(str(self.image_path))
            if not pix.isNull():
                self.setPixmap(
                    pix.scaled(
                        self.width,
                        self.height,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
                self.setText("")
                return
        self.setPixmap(QPixmap())
        self.setText(self.fallback)


class ResultsPage(QWidget):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        col = QVBoxLayout(content)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(12)

        col.addWidget(self._build_header())
        col.addWidget(self._build_task_overview())
        col.addWidget(self._build_pipeline_chain())
        col.addWidget(self._build_intermediate_summary())
        col.addWidget(self._build_output_summary())
        col.addWidget(self._build_logs())
        col.addWidget(self._build_preview())

        scroll.setWidget(content)
        root.addWidget(scroll)

    def _build_header(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(18, 14, 18, 14)
        title = QLabel("系统联调测试与结果中心")
        title.setObjectName("SectionTitle")
        desc = QLabel("统一展示数据接入、生成增强、轻量识别与结果输出的联调测试过程和汇总结果。")
        desc.setObjectName("SectionSub")
        desc.setWordWrap(True)
        col.addWidget(title)
        col.addWidget(desc)
        return panel

    def _build_task_overview(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)
        title = QLabel("联调任务总览")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        info = self.data["task_overview"]
        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)
        rows = [
            ("联调任务名称", info["task_name"]),
            ("测试数据集", info["dataset"]),
            ("运行模式", info["mode"]),
            ("当前状态", info["status"]),
            ("开始时间", info["start_time"]),
            ("结束时间", info["end_time"]),
            ("输出目录", info["output_dir"]),
        ]
        for idx, (k, v) in enumerate(rows):
            key = QLabel(k)
            key.setObjectName("KeyLabel")
            val = QLabel(v)
            val.setObjectName("KeyValue" if k == "当前状态" else "SectionSub")
            grid.addWidget(key, idx, 0)
            grid.addWidget(val, idx, 1)
        col.addLayout(grid)
        return panel

    def _build_pipeline_chain(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)
        title = QLabel("全流程状态链")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        row = QHBoxLayout()
        row.setSpacing(8)
        status_map = {"已完成": "ModuleStatusReady", "运行中": "ModuleStatusRunnable", "待执行": "ModuleStatusPending"}
        for idx, item in enumerate(self.data["pipeline_steps"]):
            card = QFrame()
            card.setObjectName("FlowItem")
            inner = QVBoxLayout(card)
            inner.setContentsMargins(10, 8, 10, 8)
            name = QLabel(item["name"])
            name.setObjectName("RecentTitle")
            state = QLabel(item["status"])
            state.setObjectName(status_map.get(item["status"], "ModuleStatusPending"))
            inner.addWidget(name)
            inner.addWidget(state, 0, Qt.AlignmentFlag.AlignLeft)
            row.addWidget(card, 1)
            if idx < len(self.data["pipeline_steps"]) - 1:
                arrow = QLabel("→")
                arrow.setObjectName("SectionSub")
                row.addWidget(arrow)
        col.addLayout(row)
        return panel

    def _build_intermediate_summary(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)
        title = QLabel("中间结果汇总")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(8)
        for idx, item in enumerate(self.data["handoff_summary"]):
            card = QFrame()
            card.setObjectName("FlowItem")
            inner = QVBoxLayout(card)
            inner.setContentsMargins(10, 8, 10, 8)
            k = QLabel(item["name"])
            k.setObjectName("KeyLabel")
            v = QLabel(item["value"])
            v.setObjectName("KeyValue")
            inner.addWidget(k)
            inner.addWidget(v)
            grid.addWidget(card, idx // 4, idx % 4)
        col.addLayout(grid)
        desc = QLabel(self.data["handoff_desc"])
        desc.setObjectName("SectionSub")
        desc.setWordWrap(True)
        col.addWidget(desc)
        return panel

    def _build_output_summary(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)
        title = QLabel("结果输出与性能摘要")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(8)
        for idx, item in enumerate(self.data["final_summary"]):
            card = QFrame()
            card.setObjectName("FlowItem")
            inner = QVBoxLayout(card)
            inner.setContentsMargins(10, 8, 10, 8)
            k = QLabel(item["name"])
            k.setObjectName("KeyLabel")
            v = QLabel(item["value"])
            v.setObjectName("KeyValue")
            inner.addWidget(k)
            inner.addWidget(v)
            grid.addWidget(card, idx // 4, idx % 4)
        col.addLayout(grid)
        return panel

    def _build_logs(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)
        title = QLabel("联调日志")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        log = QTextEdit()
        log.setObjectName("TaskLog")
        log.setReadOnly(True)
        log.setFixedHeight(150)
        log.setText("联调运行日志：\n" + "\n".join(f"- {line}" for line in self.data["logs"]))
        col.addWidget(log)
        return panel

    def _build_preview(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)
        title = QLabel("结果预览缩略图")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        row = QHBoxLayout()
        row.setSpacing(8)
        for item in self.data["preview_images"]:
            card = QFrame()
            card.setObjectName("FlowItem")
            inner = QVBoxLayout(card)
            inner.setContentsMargins(8, 8, 8, 8)
            img = ResultThumbLabel(item["path"], f"未找到图像\n{item['path']}", width=520, height=220)
            caption = QLabel(item["title"])
            caption.setObjectName("SectionSub")
            inner.addWidget(img)
            inner.addWidget(caption)
            row.addWidget(card, 1)
        col.addLayout(row)
        return panel
