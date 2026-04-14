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
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class RecognitionPage(QWidget):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data
        self.train_progress = data["training_execution"]["progress"]
        self.train_running = False
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        root.addWidget(self._build_header())

        top = QHBoxLayout()
        top.setSpacing(12)
        top.addWidget(self._build_task_config(), 1)
        top.addWidget(self._build_model_config(), 1)
        root.addLayout(top)

        middle = QHBoxLayout()
        middle.setSpacing(12)
        middle.addWidget(self._build_training_execution(), 1)
        middle.addWidget(self._build_inference_panel(), 1)
        root.addLayout(middle)

        bottom = QHBoxLayout()
        bottom.setSpacing(12)
        bottom.addWidget(self._build_metrics_panel(), 1)
        bottom.addWidget(self._build_preview_panel(), 1)
        root.addLayout(bottom)

        self._refresh_train_view()

    def _build_header(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(18, 14, 18, 14)
        title = QLabel("轻量识别训练与推理")
        title.setObjectName("SectionTitle")
        desc = QLabel("围绕增强数据接入、UT-EAT 模型训练与待测样本推理，完成轻量识别任务执行与结果输出。")
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

        title = QLabel("识别任务配置")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        form = QGridLayout()
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(8)

        cfg = self.data["task_config"]

        self.dataset_combo = QComboBox()
        self.dataset_combo.setObjectName("InputControl")
        self.dataset_combo.addItems(cfg["datasets"])

        self.source_combo = QComboBox()
        self.source_combo.setObjectName("InputControl")
        self.source_combo.addItems(cfg["data_sources"])

        self.mode_combo = QComboBox()
        self.mode_combo.setObjectName("InputControl")
        self.mode_combo.addItems(cfg["run_modes"])

        self.task_name = QLineEdit(cfg["task_name"])
        self.task_name.setObjectName("InputControl")
        self.output_dir = QLineEdit(cfg["output_dir"])
        self.output_dir.setObjectName("InputControl")

        rows = [
            ("数据集", self.dataset_combo),
            ("数据来源", self.source_combo),
            ("任务名称", self.task_name),
            ("输出目录", self.output_dir),
            ("运行模式", self.mode_combo),
        ]

        for i, (name, widget) in enumerate(rows):
            label = QLabel(name)
            label.setObjectName("KeyLabel")
            form.addWidget(label, i, 0)
            form.addWidget(widget, i, 1)

        col.addLayout(form)

        classes = QLabel(f"类别体系：{cfg['class_schema']}")
        classes.setObjectName("SectionSub")
        classes.setWordWrap(True)
        col.addWidget(classes)

        return panel

    def _build_model_config(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("模型与训练参数配置")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        cfg = self.data["model_config"]
        form = QGridLayout()
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(8)

        self.model_controls: dict[str, QWidget] = {}

        self._line_setting(form, 0, "模型名称", cfg["model_name"], "model_name", readonly=True)
        self._line_setting(form, 1, "版本/骨干", cfg["backbone"], "backbone", readonly=True)
        self._line_setting(form, 2, "Batch Size", str(cfg["batch_size"]), "batch_size")
        self._line_setting(form, 3, "学习率", str(cfg["learning_rate"]), "learning_rate")
        self._line_setting(form, 4, "训练轮数", str(cfg["epochs"]), "epochs")
        self._line_setting(form, 5, "优化器", cfg["optimizer"], "optimizer")
        self._line_setting(form, 6, "Checkpoint 输出", cfg["checkpoint_dir"], "checkpoint_dir")

        pretrain = QCheckBox("加载预训练权重")
        pretrain.setObjectName("InputCheck")
        pretrain.setChecked(cfg["use_pretrained"])
        aug = QCheckBox("启用增强数据训练")
        aug.setObjectName("InputCheck")
        aug.setChecked(cfg["use_augmented_data"])
        self.model_controls["use_pretrained"] = pretrain
        self.model_controls["use_augmented_data"] = aug

        form.addWidget(QLabel("训练策略"), 7, 0)
        form.itemAtPosition(7, 0).widget().setObjectName("KeyLabel")
        strategy_row = QHBoxLayout()
        strategy_row.addWidget(pretrain)
        strategy_row.addWidget(aug)
        strategy_row.addStretch(1)
        form.addLayout(strategy_row, 7, 1)

        col.addLayout(form)

        action_row = QHBoxLayout()
        reset_btn = QPushButton("恢复参数")
        reset_btn.setObjectName("EnterButton")
        save_btn = QPushButton("保存配置")
        save_btn.setObjectName("EnterButton")
        reset_btn.clicked.connect(self._reset_model_config)
        save_btn.clicked.connect(lambda: self._append_train_log("模型配置已保存。"))
        action_row.addWidget(reset_btn)
        action_row.addWidget(save_btn)
        action_row.addStretch(1)
        col.addLayout(action_row)

        return panel

    def _build_training_execution(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("训练任务执行")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        self.train_state = QLabel()
        self.train_state.setObjectName("KeyValue")
        self.epoch_state = QLabel()
        self.epoch_state.setObjectName("SectionSub")
        self.loss_state = QLabel()
        self.loss_state.setObjectName("SectionSub")
        self.acc_state = QLabel()
        self.acc_state.setObjectName("SectionSub")

        self.train_bar = QProgressBar()
        self.train_bar.setObjectName("TaskProgress")
        self.train_bar.setValue(self.train_progress)

        self.checkpoint_time = QLabel(f"最近保存：{self.data['training_execution']['last_checkpoint_time']}")
        self.checkpoint_time.setObjectName("SectionSub")

        col.addWidget(self.train_state)
        col.addWidget(self.epoch_state)
        col.addWidget(self.train_bar)
        col.addWidget(self.loss_state)
        col.addWidget(self.acc_state)
        col.addWidget(self.checkpoint_time)

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("开始训练")
        self.start_btn.setObjectName("HeroAction")
        stop_btn = QPushButton("标记完成")
        stop_btn.setObjectName("HeroGhostAction")
        self.start_btn.clicked.connect(self._start_training)
        stop_btn.clicked.connect(self._finish_training)
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(stop_btn)
        btn_row.addStretch(1)
        col.addLayout(btn_row)

        self.train_log = QTextEdit()
        self.train_log.setObjectName("TaskLog")
        self.train_log.setReadOnly(True)
        self.train_log.setFixedHeight(96)
        self.train_log.setText("训练日志：\n- 任务待执行。")
        col.addWidget(self.train_log)

        self.train_timer = QTimer(self)
        self.train_timer.timeout.connect(self._tick_training)

        return panel

    def _build_inference_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("推理任务")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        inf = self.data["inference"]

        form = QGridLayout()
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(8)

        self.sample_path = QLineEdit(inf["sample_path"])
        self.sample_path.setObjectName("InputControl")
        self.model_select = QComboBox()
        self.model_select.setObjectName("InputControl")
        self.model_select.addItems(inf["model_options"])

        form.addWidget(QLabel("待测样本路径"), 0, 0)
        form.itemAtPosition(0, 0).widget().setObjectName("KeyLabel")
        form.addWidget(self.sample_path, 0, 1)
        form.addWidget(QLabel("推理模型"), 1, 0)
        form.itemAtPosition(1, 0).widget().setObjectName("KeyLabel")
        form.addWidget(self.model_select, 1, 1)
        col.addLayout(form)

        run_btn = QPushButton("开始推理")
        run_btn.setObjectName("EnterButton")
        run_btn.clicked.connect(self._run_inference)
        col.addWidget(run_btn, 0, Qt.AlignmentFlag.AlignLeft)

        self.infer_state = QLabel(f"当前状态：{inf['status']}")
        self.infer_state.setObjectName("KeyValue")
        self.pred_state = QLabel(f"预测类别：{inf['prediction']}")
        self.pred_state.setObjectName("SectionSub")
        self.conf_state = QLabel(f"置信度：{inf['confidence']}")
        self.conf_state.setObjectName("SectionSub")
        self.latency_state = QLabel(f"推理时延：{inf['latency']}")
        self.latency_state.setObjectName("SectionSub")

        col.addWidget(self.infer_state)
        col.addWidget(self.pred_state)
        col.addWidget(self.conf_state)
        col.addWidget(self.latency_state)

        return panel

    def _build_metrics_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("识别结果与性能指标")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(8)

        for i, item in enumerate(self.data["metrics"]):
            card = QFrame()
            card.setObjectName("FlowItem")
            inner = QVBoxLayout(card)
            inner.setContentsMargins(10, 8, 10, 8)
            key = QLabel(item["name"])
            key.setObjectName("KeyLabel")
            value = QLabel(item["value"])
            value.setObjectName("KeyValue")
            inner.addWidget(key)
            inner.addWidget(value)
            grid.addWidget(card, i // 3, i % 3)

        col.addLayout(grid)

        status = QLabel(f"模型状态：{self.data['model_status']}｜最近测试：{self.data['latest_test']} ")
        status.setObjectName("SectionSub")
        col.addWidget(status)

        return panel

    def _build_preview_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CardPanel")
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 14, 16, 14)

        title = QLabel("结果预览")
        title.setObjectName("SectionTitle")
        col.addWidget(title)

        for block in self.data["preview_blocks"]:
            card = QFrame()
            card.setObjectName("FlowItem")
            inner = QVBoxLayout(card)
            inner.setContentsMargins(10, 8, 10, 8)
            t = QLabel(block["title"])
            t.setObjectName("RecentTitle")
            p = QLabel(block["preview"])
            p.setAlignment(Qt.AlignmentFlag.AlignCenter)
            p.setStyleSheet("font-size: 13px; color: #34658f;")
            d = QLabel(block["desc"])
            d.setObjectName("RecentDesc")
            d.setWordWrap(True)
            inner.addWidget(t)
            inner.addWidget(p)
            inner.addWidget(d)
            col.addWidget(card)

        return panel

    def _line_setting(self, layout: QGridLayout, row: int, name: str, value: str, key: str, readonly: bool = False) -> None:
        k = QLabel(name)
        k.setObjectName("KeyLabel")
        edit = QLineEdit(value)
        edit.setObjectName("InputControl")
        edit.setReadOnly(readonly)
        self.model_controls[key] = edit
        layout.addWidget(k, row, 0)
        layout.addWidget(edit, row, 1)

    def _reset_model_config(self) -> None:
        cfg = self.data["model_config"]
        self.model_controls["batch_size"].setText(str(cfg["batch_size"]))
        self.model_controls["learning_rate"].setText(str(cfg["learning_rate"]))
        self.model_controls["epochs"].setText(str(cfg["epochs"]))
        self.model_controls["optimizer"].setText(cfg["optimizer"])
        self.model_controls["checkpoint_dir"].setText(cfg["checkpoint_dir"])
        self.model_controls["use_pretrained"].setChecked(cfg["use_pretrained"])
        self.model_controls["use_augmented_data"].setChecked(cfg["use_augmented_data"])
        self._append_train_log("已恢复默认训练参数。")

    def _start_training(self) -> None:
        if self.train_running:
            return
        self.train_running = True
        self.data["training_execution"]["status"] = "训练中"
        self.start_btn.setText("训练中...")
        self.train_timer.start(400)
        self._append_train_log("UT-EAT 训练任务已启动。")
        self._refresh_train_view()

    def _tick_training(self) -> None:
        if self.train_progress >= 100:
            self._finish_training()
            return
        self.train_progress += 5
        self._refresh_train_view()

    def _finish_training(self) -> None:
        self.train_timer.stop()
        self.train_running = False
        self.train_progress = 100
        self.data["training_execution"]["status"] = "已完成"
        self.start_btn.setText("开始训练")
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.checkpoint_time.setText(f"最近保存：{now}")
        self._append_train_log("训练完成：已输出 checkpoint 与评估摘要。")
        self._refresh_train_view()

    def _refresh_train_view(self) -> None:
        cfg = self.data["training_execution"]
        total_epochs = self.data["model_config"]["epochs"]
        current_epoch = max(1, int(total_epochs * self.train_progress / 100))
        loss = 1.2 - 0.9 * (self.train_progress / 100)
        acc = 0.65 + 0.29 * (self.train_progress / 100)
        f1 = 0.61 + 0.31 * (self.train_progress / 100)

        self.train_state.setText(f"当前任务状态：{cfg['status']}")
        self.epoch_state.setText(f"当前 Epoch：{current_epoch} / {total_epochs}｜阶段：{cfg['stages'][min(self.train_progress // 34, len(cfg['stages']) - 1)]}")
        self.train_bar.setValue(self.train_progress)
        self.loss_state.setText(f"当前 Loss：{loss:.4f}")
        self.acc_state.setText(f"当前 Accuracy / Macro-F1：{acc:.3f} / {f1:.3f}")

    def _run_inference(self) -> None:
        info = self.data["inference"]
        info["status"] = "已完成"
        self.infer_state.setText(f"当前状态：{info['status']}")
        self.pred_state.setText(f"预测类别：{info['prediction']}")
        self.conf_state.setText(f"置信度：{info['confidence']}")
        self.latency_state.setText(f"推理时延：{info['latency']}")
        self._append_train_log("推理完成：已输出 Top-1 结果与时延。")

    def _append_train_log(self, text: str) -> None:
        self.train_log.setText(f"{self.train_log.toPlainText()}\n- {text}")
