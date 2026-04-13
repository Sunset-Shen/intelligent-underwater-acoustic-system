from __future__ import annotations

from datetime import datetime

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class DataPage(QWidget):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data
        self.task_running = False
        self.progress_value = data["task_execution"]["progress"]
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        root.addWidget(self._build_header())

        top_row = QHBoxLayout()
        top_row.setSpacing(12)
        top_row.addWidget(self._build_dataset_access(), 1)
        top_row.addWidget(self._build_dataset_overview(), 1)
        root.addLayout(top_row)

        middle_row = QHBoxLayout()
        middle_row.setSpacing(12)
        middle_row.addWidget(self._build_preprocess_config(), 1)
        middle_row.addWidget(self._build_task_execution(), 1)
        root.addLayout(middle_row)

        root.addWidget(self._build_result_preview())

        self._apply_selected_dataset(self.dataset_selector.currentText())

    def _build_header(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(18, 14, 18, 14)

        title = QLabel("数据接入与预处理")
        title.setObjectName("SectionTitle")
        desc = QLabel("统一完成水声数据集接入、组织管理、预处理配置与结果预览，为后续生成增强和轻量识别提供标准化输入。")
        desc.setObjectName("SectionSub")
        desc.setWordWrap(True)

        col.addWidget(title)
        col.addWidget(desc)
        return panel

    def _build_dataset_access(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)
        col.setSpacing(10)

        title = QLabel("数据集接入")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        source_row = QHBoxLayout()
        source_label = QLabel("数据集来源")
        source_label.setObjectName("KeyLabel")
        self.dataset_selector = QComboBox()
        self.dataset_selector.setObjectName("InputControl")
        self.dataset_selector.addItems(self.data["source_options"])
        self.dataset_selector.currentTextChanged.connect(self._apply_selected_dataset)
        source_row.addWidget(source_label)
        source_row.addWidget(self.dataset_selector, 1)
        col.addLayout(source_row)

        path_row = QHBoxLayout()
        path_label = QLabel("数据目录")
        path_label.setObjectName("KeyLabel")
        self.path_input = QLineEdit()
        self.path_input.setObjectName("InputControl")
        self.path_input.setReadOnly(True)
        path_row.addWidget(path_label)
        path_row.addWidget(self.path_input, 1)
        col.addLayout(path_row)

        btn_row = QHBoxLayout()
        self.scan_btn = QPushButton("扫描数据")
        self.scan_btn.setObjectName("EnterButton")
        self.import_btn = QPushButton("导入数据")
        self.import_btn.setObjectName("EnterButton")
        self.scan_btn.clicked.connect(lambda: self._set_access_status("扫描完成：已识别数据结构"))
        self.import_btn.clicked.connect(lambda: self._set_access_status("导入完成：已建立索引"))
        btn_row.addWidget(self.scan_btn)
        btn_row.addWidget(self.import_btn)
        btn_row.addStretch(1)
        col.addLayout(btn_row)

        summary = QFrame()
        summary.setObjectName("FlowItem")
        grid = QGridLayout(summary)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)

        self.dataset_fields: dict[str, QLabel] = {}
        for i, key in enumerate(["dataset_name", "class_count", "sample_count", "sample_rate", "status"]):
            k_label = QLabel(self.data["labels"][key])
            k_label.setObjectName("KeyLabel")
            v_label = QLabel("")
            v_label.setObjectName("KeyValue")
            self.dataset_fields[key] = v_label
            grid.addWidget(k_label, i, 0)
            grid.addWidget(v_label, i, 1)

        col.addWidget(summary)

        self.access_status = QLabel("接入状态：待执行")
        self.access_status.setObjectName("SectionSub")
        col.addWidget(self.access_status)

        return panel

    def _build_dataset_overview(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("数据集概览")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        self.class_table = QTableWidget(0, 4)
        self.class_table.setObjectName("DataTable")
        self.class_table.setHorizontalHeaderLabels(["类别编号", "类别名称", "中文类别名", "样本数"])
        self.class_table.verticalHeader().setVisible(False)
        self.class_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.class_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.class_table.horizontalHeader().setStretchLastSection(True)
        col.addWidget(self.class_table)

        split_card = QFrame()
        split_card.setObjectName("FlowItem")
        split_layout = QVBoxLayout(split_card)
        split_layout.setContentsMargins(10, 8, 10, 8)

        self.split_info = QLabel()
        self.split_info.setObjectName("KeyValue")
        split_layout.addWidget(self.split_info)

        split_tip = QLabel("数据说明：按船舶类别进行分层划分，确保训练/验证/测试分布一致。")
        split_tip.setObjectName("SectionSub")
        split_tip.setWordWrap(True)
        split_layout.addWidget(split_tip)

        col.addWidget(split_card)
        return panel

    def _build_preprocess_config(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("预处理参数配置")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        form = QGridLayout()
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(8)

        self.config_controls: dict[str, QWidget] = {}
        defaults = self.data["preprocess_defaults"]

        self._add_line_edit(form, 0, "重采样频率", defaults["resample_rate"], "resample_rate")
        self._add_line_edit(form, 1, "切片长度", defaults["slice_length"], "slice_length")
        self._add_combo(form, 2, "切片方式", defaults["slice_method"], ["无重叠切分", "50% 重叠切分"], "slice_method")
        self._add_combo(form, 3, "尾段处理策略", defaults["tail_policy"], ["小于 5 s 丢弃，5–10 s 保留", "统一补零到 10 s"], "tail_policy")
        self._add_combo(form, 4, "输出格式", defaults["output_format"], ["spec.npy", "cache.bin"], "output_format")

        cache_label = QLabel("生成频谱缓存")
        cache_label.setObjectName("KeyLabel")
        cache_check = QCheckBox("启用")
        cache_check.setObjectName("InputCheck")
        cache_check.setChecked(defaults["generate_cache"])
        self.config_controls["generate_cache"] = cache_check
        form.addWidget(cache_label, 5, 0)
        form.addWidget(cache_check, 5, 1)

        col.addLayout(form)

        btn_row = QHBoxLayout()
        reset_btn = QPushButton("恢复默认参数")
        reset_btn.setObjectName("EnterButton")
        save_btn = QPushButton("保存当前配置")
        save_btn.setObjectName("EnterButton")
        reset_btn.clicked.connect(self._reset_defaults)
        save_btn.clicked.connect(lambda: self._set_task_log("配置已保存：预处理参数已更新。"))

        btn_row.addWidget(reset_btn)
        btn_row.addWidget(save_btn)
        btn_row.addStretch(1)
        col.addLayout(btn_row)

        return panel

    def _build_task_execution(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("预处理任务执行")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        self.task_status = QLabel(f"当前任务状态：{self.data['task_execution']['status']}")
        self.task_status.setObjectName("KeyValue")
        col.addWidget(self.task_status)

        self.task_dataset = QLabel(f"当前数据集：{self.dataset_selector.currentText()}")
        self.task_dataset.setObjectName("SectionSub")
        col.addWidget(self.task_dataset)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("TaskProgress")
        self.progress_bar.setValue(self.progress_value)
        col.addWidget(self.progress_bar)

        self.progress_label = QLabel(self._progress_text())
        self.progress_label.setObjectName("SectionSub")
        col.addWidget(self.progress_label)

        self.output_info = QLabel(f"输出目录：{self.data['task_execution']['output_dir']}")
        self.output_info.setObjectName("SectionSub")
        col.addWidget(self.output_info)

        self.last_run = QLabel(f"最近一次执行：{self.data['task_execution']['last_run']}")
        self.last_run.setObjectName("SectionSub")
        col.addWidget(self.last_run)

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("开始预处理")
        self.start_btn.setObjectName("HeroAction")
        self.start_btn.clicked.connect(self._start_task)

        finish_btn = QPushButton("标记完成")
        finish_btn.setObjectName("HeroGhostAction")
        finish_btn.clicked.connect(self._finish_task)

        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(finish_btn)
        btn_row.addStretch(1)
        col.addLayout(btn_row)

        self.task_log = QTextEdit()
        self.task_log.setObjectName("TaskLog")
        self.task_log.setReadOnly(True)
        self.task_log.setFixedHeight(106)
        self.task_log.setText("任务日志：\n- 等待执行预处理任务。")
        col.addWidget(self.task_log)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick_progress)

        return panel

    def _build_result_preview(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("预处理结果预览")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        row = QHBoxLayout()
        row.setSpacing(10)

        for block in self.data["preview_blocks"]:
            card = QFrame()
            card.setObjectName("FlowItem")
            inner = QVBoxLayout(card)
            inner.setContentsMargins(10, 8, 10, 8)
            h = QLabel(block["title"])
            h.setObjectName("RecentTitle")
            preview = QLabel(block["preview"])
            preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
            preview.setStyleSheet("font-size: 13px; color: #335f88;")
            preview.setMinimumHeight(48)
            d = QLabel(block["desc"])
            d.setObjectName("RecentDesc")
            d.setWordWrap(True)

            inner.addWidget(h)
            inner.addWidget(preview)
            inner.addWidget(d)
            row.addWidget(card, 1)

        col.addLayout(row)
        return panel

    def _add_line_edit(self, layout: QGridLayout, row: int, label_text: str, value: str, key: str) -> None:
        label = QLabel(label_text)
        label.setObjectName("KeyLabel")
        edit = QLineEdit(value)
        edit.setObjectName("InputControl")
        self.config_controls[key] = edit
        layout.addWidget(label, row, 0)
        layout.addWidget(edit, row, 1)

    def _add_combo(self, layout: QGridLayout, row: int, label_text: str, value: str, options: list[str], key: str) -> None:
        label = QLabel(label_text)
        label.setObjectName("KeyLabel")
        combo = QComboBox()
        combo.setObjectName("InputControl")
        combo.addItems(options)
        combo.setCurrentText(value)
        self.config_controls[key] = combo
        layout.addWidget(label, row, 0)
        layout.addWidget(combo, row, 1)

    def _apply_selected_dataset(self, name: str) -> None:
        info = self.data["datasets"][name]
        self.path_input.setText(info["path"])
        self.dataset_fields["dataset_name"].setText(info["name"])
        self.dataset_fields["class_count"].setText(info["class_count"])
        self.dataset_fields["sample_count"].setText(info["sample_count"])
        self.dataset_fields["sample_rate"].setText(info["sample_rate"])
        self.dataset_fields["status"].setText(info["status"])
        if hasattr(self, "task_dataset"):
            self.task_dataset.setText(f"当前数据集：{name}")
        self._refresh_overview(name)

    def _refresh_overview(self, name: str) -> None:
        dataset = self.data["datasets"][name]
        classes = dataset["classes"]

        self.class_table.setRowCount(len(classes))
        for row, item in enumerate(classes):
            self.class_table.setItem(row, 0, QTableWidgetItem(item["id"]))
            self.class_table.setItem(row, 1, QTableWidgetItem(item["en_name"]))
            self.class_table.setItem(row, 2, QTableWidgetItem(item["cn_name"]))
            self.class_table.setItem(row, 3, QTableWidgetItem(item["count"]))

        split = dataset["split"]
        total = dataset.get("total_samples", "-")
        self.split_info.setText(f"总样本：{total}｜训练 / 验证 / 测试：{split['train']} / {split['val']} / {split['test']}")

    def _set_access_status(self, text: str) -> None:
        self.access_status.setText(f"接入状态：{text}")

    def _reset_defaults(self) -> None:
        defaults = self.data["preprocess_defaults"]
        cast = self.config_controls
        cast["resample_rate"].setText(defaults["resample_rate"])
        cast["slice_length"].setText(defaults["slice_length"])
        cast["slice_method"].setCurrentText(defaults["slice_method"])
        cast["tail_policy"].setCurrentText(defaults["tail_policy"])
        cast["output_format"].setCurrentText(defaults["output_format"])
        cast["generate_cache"].setChecked(defaults["generate_cache"])
        self._set_task_log("配置已恢复默认参数。")

    def _start_task(self) -> None:
        if self.task_running:
            return
        self.task_running = True
        self.task_status.setText("当前任务状态：处理中")
        self.start_btn.setText("处理中...")
        self.timer.start(350)
        self._set_task_log("预处理任务已启动。")

    def _tick_progress(self) -> None:
        if self.progress_value >= 100:
            self._finish_task()
            return
        self.progress_value += 5
        self.progress_bar.setValue(self.progress_value)
        self.progress_label.setText(self._progress_text())

    def _finish_task(self) -> None:
        self.timer.stop()
        self.task_running = False
        self.progress_value = 100
        self.progress_bar.setValue(100)
        self.task_status.setText("当前任务状态：已完成")
        self.start_btn.setText("开始预处理")
        self.progress_label.setText(self._progress_text())
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.last_run.setText(f"最近一次执行：{now}")
        self._set_task_log("预处理任务已完成，输出缓存可用于后续生成增强与识别训练。")

    def _set_task_log(self, text: str) -> None:
        current = self.task_log.toPlainText()
        self.task_log.setText(f"{current}\n- {text}")

    def _progress_text(self) -> str:
        total = self.data["task_execution"]["total_samples"]
        done = int(total * self.progress_value / 100)
        return f"进度：{done} / {total} 样本"
