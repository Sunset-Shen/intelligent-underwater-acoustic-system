from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap
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
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ImagePreviewLabel(QLabel):
    def __init__(self, image_path: str, fallback: str, target_width: int = 420, target_height: int = 220) -> None:
        super().__init__()
        raw_path = Path(image_path)
        project_root = Path(__file__).resolve().parents[2]
        self.image_path = raw_path if raw_path.is_absolute() else (project_root / raw_path)
        self.fallback = fallback
        self.target_width = target_width
        self.target_height = target_height

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("ImagePreview")
        self.setMinimumHeight(target_height)
        self.setMaximumHeight(target_height)

        self._load_once()

    def _load_once(self) -> None:
        if self.image_path.exists():
            pixmap = QPixmap(str(self.image_path))
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    self.target_width,
                    self.target_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self.setPixmap(scaled)
                self.setText("")
                return

        self.setPixmap(QPixmap())
        self.setText(self.fallback)


class GenerationPage(QWidget):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data
        self.progress = data["execution"]["progress"]
        self.task_running = False
        self._build_ui()

    def _build_ui(self) -> None:
        wrapper = QVBoxLayout(self)
        wrapper.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        root = QVBoxLayout(content)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        root.addWidget(self._build_header())

        top = QHBoxLayout()
        top.setSpacing(12)
        top.addWidget(self._build_task_config(), 1)
        top.addWidget(self._build_physical_priors(), 1)
        root.addLayout(top)

        middle = QHBoxLayout()
        middle.setSpacing(12)
        middle.addWidget(self._build_param_config(), 1)
        middle.addWidget(self._build_execution_panel(), 1)
        root.addLayout(middle)

        root.addWidget(self._build_result_preview())
        root.addWidget(self._build_physical_consistency())
        root.addWidget(self._build_guidance_curve())
        root.addWidget(self._build_dataset_build())

        scroll.setWidget(content)
        wrapper.addWidget(scroll)

        self._refresh_task_info()

    def _build_header(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(18, 14, 18, 14)
        title = QLabel("可解释生成与数据增强")
        title.setObjectName("SectionTitle")
        desc = QLabel("围绕类别条件与物理先验约束完成增强样本生成，并构建可供后续识别训练使用的增强数据集。")
        desc.setObjectName("SectionSub")
        desc.setWordWrap(True)
        col.addWidget(title)
        col.addWidget(desc)
        return panel

    def _build_task_config(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("生成任务配置")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        form = QGridLayout()
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(8)

        self.dataset_combo = QComboBox()
        self.dataset_combo.setObjectName("InputControl")
        self.dataset_combo.addItems(self.data["task_config"]["datasets"])

        self.class_combo = QComboBox()
        self.class_combo.setObjectName("InputControl")
        self.class_combo.addItems(self.data["task_config"]["target_classes"])

        self.task_name = QLineEdit(self.data["task_config"]["task_name"])
        self.task_name.setObjectName("InputControl")
        self.output_dir = QLineEdit(self.data["task_config"]["output_dir"])
        self.output_dir.setObjectName("InputControl")
        self.target_count = QLineEdit(str(self.data["task_config"]["target_samples"]))
        self.target_count.setObjectName("InputControl")

        fields = [
            ("数据集", self.dataset_combo),
            ("目标类别", self.class_combo),
            ("任务名称", self.task_name),
            ("输出目录", self.output_dir),
            ("目标生成数量", self.target_count),
        ]

        for row, (name, widget) in enumerate(fields):
            key = QLabel(name)
            key.setObjectName("KeyLabel")
            form.addWidget(key, row, 0)
            form.addWidget(widget, row, 1)

        col.addLayout(form)

        actions = QHBoxLayout()
        create_btn = QPushButton("创建任务")
        create_btn.setObjectName("EnterButton")
        load_btn = QPushButton("加载任务")
        load_btn.setObjectName("EnterButton")
        create_btn.clicked.connect(lambda: self._append_log("已创建新生成任务，等待执行。"))
        load_btn.clicked.connect(lambda: self._append_log("已加载上一次生成任务配置。"))
        actions.addWidget(create_btn)
        actions.addWidget(load_btn)
        actions.addStretch(1)
        col.addLayout(actions)

        return panel

    def _build_physical_priors(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)
        col.setSpacing(8)

        title = QLabel("物理先验约束")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        row = QHBoxLayout()
        row.setSpacing(8)

        for prior in self.data["physical_priors"]:
            card = QFrame()
            card.setObjectName("FlowItem")
            inner = QVBoxLayout(card)
            inner.setContentsMargins(10, 8, 10, 8)

            head = QHBoxLayout()
            t = QLabel(prior["name"])
            t.setObjectName("RecentTitle")
            st = QLabel(prior["status"])
            st.setObjectName("MetricBadge")
            head.addWidget(t)
            head.addStretch(1)
            head.addWidget(st)

            preview = QLabel(prior["preview"])
            preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
            preview.setStyleSheet("font-size: 13px; color: #2f638f;")
            desc = QLabel(prior["desc"])
            desc.setObjectName("RecentDesc")
            desc.setWordWrap(True)

            inner.addLayout(head)
            inner.addWidget(preview)
            inner.addWidget(desc)
            row.addWidget(card, 1)

        col.addLayout(row)
        return panel

    def _build_param_config(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("生成参数配置")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        defaults = self.data["generation_params"]
        form = QGridLayout()
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(8)

        self.param_controls: dict[str, QWidget] = {}

        self._line_param(form, 0, "采样步数", str(defaults["sampling_steps"]), "sampling_steps")
        self._line_param(form, 1, "引导强度", str(defaults["guidance_scale"]), "guidance_scale")
        self._line_param(form, 2, "批次大小", str(defaults["batch_size"]), "batch_size")
        self._line_param(form, 3, "随机噪声输入", defaults["noise_input"], "noise_input")
        self._line_param(form, 4, "输出样本数", str(defaults["output_samples"]), "output_samples")

        cond = QCheckBox("类条件生成")
        cond.setObjectName("InputCheck")
        cond.setChecked(defaults["class_conditioned"])
        prior = QCheckBox("启用物理先验约束")
        prior.setObjectName("InputCheck")
        prior.setChecked(defaults["enable_physical_prior"])
        self.param_controls["class_conditioned"] = cond
        self.param_controls["enable_physical_prior"] = prior

        form.addWidget(QLabel("条件控制"), 5, 0)
        form.itemAtPosition(5, 0).widget().setObjectName("KeyLabel")
        cond_row = QHBoxLayout()
        cond_row.addWidget(cond)
        cond_row.addWidget(prior)
        cond_row.addStretch(1)
        form.addLayout(cond_row, 5, 1)

        col.addLayout(form)

        btn_row = QHBoxLayout()
        reset_btn = QPushButton("恢复参数")
        reset_btn.setObjectName("EnterButton")
        save_btn = QPushButton("保存配置")
        save_btn.setObjectName("EnterButton")
        reset_btn.clicked.connect(self._reset_params)
        save_btn.clicked.connect(lambda: self._append_log("已保存生成参数配置。"))
        btn_row.addWidget(reset_btn)
        btn_row.addWidget(save_btn)
        btn_row.addStretch(1)
        col.addLayout(btn_row)

        return panel

    def _build_execution_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("生成任务执行")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        self.state_label = QLabel()
        self.state_label.setObjectName("KeyValue")
        self.stage_label = QLabel()
        self.stage_label.setObjectName("SectionSub")

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("TaskProgress")
        self.progress_bar.setValue(self.progress)
        self.progress_text = QLabel()
        self.progress_text.setObjectName("SectionSub")

        self.output_info = QLabel(f"输出目录：{self.data['task_config']['output_dir']}")
        self.output_info.setObjectName("SectionSub")
        self.last_time = QLabel(f"最近执行：{self.data['execution']['last_run']}")
        self.last_time.setObjectName("SectionSub")

        col.addWidget(self.state_label)
        col.addWidget(self.stage_label)
        col.addWidget(self.progress_bar)
        col.addWidget(self.progress_text)
        col.addWidget(self.output_info)
        col.addWidget(self.last_time)

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("开始生成")
        self.start_btn.setObjectName("HeroAction")
        stop_btn = QPushButton("标记完成")
        stop_btn.setObjectName("HeroGhostAction")
        self.start_btn.clicked.connect(self._start_generation)
        stop_btn.clicked.connect(self._finish_generation)
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(stop_btn)
        btn_row.addStretch(1)
        col.addLayout(btn_row)

        self.log_box = QTextEdit()
        self.log_box.setObjectName("TaskLog")
        self.log_box.setReadOnly(True)
        self.log_box.setFixedHeight(110)
        self.log_box.setText("运行日志：\n- 任务初始化完成。\n- 先验模板加载完成。\n- 等待执行生成任务。")
        col.addWidget(self.log_box)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)

        return panel

    def _build_result_preview(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("生成结果预览")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        row = QHBoxLayout()
        row.setSpacing(8)
        for item in self.data["result_preview"]:
            card = QFrame()
            card.setObjectName("FlowItem")
            inner = QVBoxLayout(card)
            inner.setContentsMargins(10, 8, 10, 8)
            lab = QLabel(item["title"])
            lab.setObjectName("RecentTitle")
            preview = QLabel(item["preview"])
            preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
            preview.setStyleSheet("font-size: 13px; color: #34658f;")
            tag = QLabel(f"{item['sample_id']} ｜ {item['label']} ｜ {item['quality']}")
            tag.setObjectName("RecentDesc")
            summary = QLabel(item["summary"])
            summary.setObjectName("SectionSub")
            summary.setWordWrap(True)
            inner.addWidget(lab)
            inner.addWidget(preview)
            inner.addWidget(tag)
            inner.addWidget(summary)
            row.addWidget(card, 1)

        col.addLayout(row)
        return panel

    def _build_physical_consistency(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("物理一致性对比结果")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(8)

        for idx, item in enumerate(self.data["physical_consistency_images"]):
            card = QFrame()
            card.setObjectName("FlowItem")
            inner = QVBoxLayout(card)
            inner.setContentsMargins(8, 8, 8, 8)
            image = ImagePreviewLabel(item["path"], f"未找到图像\n{item['path']}", target_width=360, target_height=200)
            caption = QLabel(item["title"])
            caption.setObjectName("RecentDesc")
            caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inner.addWidget(image)
            inner.addWidget(caption)
            grid.addWidget(card, 0, idx)

        col.addLayout(grid)
        return panel

    def _build_guidance_curve(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("引导约束损失曲线")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        image = ImagePreviewLabel(
            self.data["guidance_curve"]["path"],
            f"未找到图像\n{self.data['guidance_curve']['path']}",
            target_width=980,
            target_height=420,
        )
        col.addWidget(image)

        desc = QLabel(self.data["guidance_curve"]["desc"])
        desc.setObjectName("SectionSub")
        desc.setWordWrap(True)
        col.addWidget(desc)
        return panel

    def _build_dataset_build(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("增强数据集构建")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        for item in self.data["dataset_build"]["summary"]:
            row = QHBoxLayout()
            k = QLabel(item["label"])
            k.setObjectName("KeyLabel")
            v = QLabel(item["value"])
            v.setObjectName("KeyValue")
            row.addWidget(k)
            row.addStretch(1)
            row.addWidget(v)
            col.addLayout(row)

        shift = QLabel(self.data["dataset_build"]["distribution_change"])
        shift.setObjectName("SectionSub")
        shift.setWordWrap(True)
        col.addWidget(shift)

        out_dir = QLabel(f"输出位置：{self.data['dataset_build']['output_dir']}")
        out_dir.setObjectName("SectionSub")
        out_dir.setWordWrap(True)
        col.addWidget(out_dir)

        btn_row = QHBoxLayout()
        merge_btn = QPushButton("纳入训练集")
        merge_btn.setObjectName("EnterButton")
        export_btn = QPushButton("导出增强集")
        export_btn.setObjectName("EnterButton")
        merge_btn.clicked.connect(lambda: self._append_log("增强样本已纳入训练集。"))
        export_btn.clicked.connect(lambda: self._append_log("增强数据集导出完成。"))
        btn_row.addWidget(merge_btn)
        btn_row.addWidget(export_btn)
        btn_row.addStretch(1)
        col.addLayout(btn_row)

        return panel

    def _line_param(self, layout: QGridLayout, row: int, name: str, value: str, key: str) -> None:
        label = QLabel(name)
        label.setObjectName("KeyLabel")
        edit = QLineEdit(value)
        edit.setObjectName("InputControl")
        self.param_controls[key] = edit
        layout.addWidget(label, row, 0)
        layout.addWidget(edit, row, 1)

    def _reset_params(self) -> None:
        defaults = self.data["generation_params"]
        self.param_controls["sampling_steps"].setText(str(defaults["sampling_steps"]))
        self.param_controls["guidance_scale"].setText(str(defaults["guidance_scale"]))
        self.param_controls["batch_size"].setText(str(defaults["batch_size"]))
        self.param_controls["noise_input"].setText(defaults["noise_input"])
        self.param_controls["output_samples"].setText(str(defaults["output_samples"]))
        self.param_controls["class_conditioned"].setChecked(defaults["class_conditioned"])
        self.param_controls["enable_physical_prior"].setChecked(defaults["enable_physical_prior"])
        self._append_log("参数已恢复默认。")

    def _start_generation(self) -> None:
        if self.task_running:
            return
        self.task_running = True
        self.data["execution"]["status"] = "生成中"
        self.start_btn.setText("生成中...")
        self.timer.start(350)
        self._append_log("任务启动：进入类条件扩散采样阶段。")
        self._refresh_task_info()

    def _tick(self) -> None:
        if self.progress >= 100:
            self._finish_generation()
            return
        self.progress += 5
        self._refresh_task_info()

    def _finish_generation(self) -> None:
        self.timer.stop()
        self.task_running = False
        self.progress = 100
        self.data["execution"]["status"] = "已完成"
        self.start_btn.setText("开始生成")
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.last_time.setText(f"最近执行：{now}")
        self._append_log("任务完成：样本保存完成，结果汇总完成。")
        self._refresh_task_info()

    def _refresh_task_info(self) -> None:
        total = int(self.param_controls["output_samples"].text()) if "output_samples" in self.param_controls else self.data["generation_params"]["output_samples"]
        done = int(total * self.progress / 100)
        self.state_label.setText(f"当前任务状态：{self.data['execution']['status']}")
        self.stage_label.setText(f"当前阶段：{self._current_stage()}")
        self.progress_bar.setValue(self.progress)
        self.progress_text.setText(f"已生成样本：{done} / {total}")

    def _current_stage(self) -> str:
        if self.progress >= 100:
            return "样本保存完成 / 结果汇总完成"
        stages = self.data["execution"]["stages"]
        idx = min(self.progress // 25, len(stages) - 1)
        return stages[idx]

    def _append_log(self, text: str) -> None:
        self.log_box.setText(f"{self.log_box.toPlainText()}\n- {text}")
