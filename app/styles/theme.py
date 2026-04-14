APP_STYLE = """
QWidget {
    background: #f4f8fc;
    color: #1f3347;
    font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
    font-size: 13px;
}

QFrame#AppShell {
    background: transparent;
}

QFrame#TopHeader {
    background: #ffffff;
    border: 1px solid #d9e5f2;
    border-radius: 14px;
}

QLabel#SystemTitle {
    font-size: 20px;
    font-weight: 600;
    color: #1a3652;
}

QLabel#SystemSubtitle {
    color: #607b97;
    font-size: 12px;
}

QLabel#HeaderTag {
    background: #eef5fd;
    border: 1px solid #d2e3f7;
    border-radius: 12px;
    padding: 4px 10px;
    color: #2e5378;
    font-size: 12px;
}

QLabel#StatusBadge {
    background: #edf8f3;
    border: 1px solid #cfe9db;
    border-radius: 12px;
    padding: 4px 10px;
    color: #2f6b50;
    font-size: 12px;
}

QFrame#Sidebar {
    background: #ffffff;
    border: 1px solid #d9e5f2;
    border-radius: 14px;
}

QLabel#NavTitle {
    color: #486683;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 8px;
}

QPushButton#NavButton {
    text-align: left;
    background: #ffffff;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 9px 10px;
    color: #2f4964;
}

QPushButton#NavButton:hover {
    background: #f2f8ff;
    border: 1px solid #d6e5f7;
}

QPushButton#NavButton:checked {
    background: #edf5ff;
    border: 1px solid #cfe1f8;
    color: #214f82;
    font-weight: 600;
}

QFrame#NavIndicator {
    background: #2c6fb2;
    border-radius: 2px;
}

QLabel#SidebarHint {
    color: #6f879f;
    font-size: 12px;
    border-top: 1px solid #ebf1f7;
    padding-top: 10px;
}

QFrame#CardPanel,
QFrame#HeroPanel,
QFrame#ModuleCard,
QFrame#StatusCard,
QFrame#RecentCard,
QFrame#FlowItem {
    background: #ffffff;
    border: 1px solid #d9e5f2;
    border-radius: 14px;
}

QLabel#HeroTitle {
    font-size: 26px;
    font-weight: 600;
    color: #173959;
}

QLabel#HeroDesc {
    color: #5f7b95;
    font-size: 13px;
}

QPushButton#HeroAction {
    background: #2b66a3;
    border: none;
    border-radius: 10px;
    color: #ffffff;
    padding: 8px 16px;
}

QPushButton#HeroAction:hover {
    background: #22598f;
}

QPushButton#HeroGhostAction {
    background: #eef5fd;
    border: 1px solid #d2e3f7;
    border-radius: 10px;
    color: #2c5680;
    padding: 8px 16px;
}

QPushButton#HeroGhostAction:hover {
    background: #e4effc;
}

QFrame#WavePanel {
    background: #f8fbff;
    border: 1px solid #e2ecf8;
    border-radius: 12px;
}

QLabel#SectionTitle {
    font-size: 17px;
    font-weight: 600;
    color: #1c3f63;
    margin-bottom: 6px;
}

QLabel#SectionSub {
    font-size: 12px;
    color: #6b849e;
}

QLabel#FlowIndex {
    background: #e7f1ff;
    color: #2a6299;
    border-radius: 9px;
    min-width: 18px;
    min-height: 18px;
    max-width: 18px;
    max-height: 18px;
    font-size: 11px;
    qproperty-alignment: AlignCenter;
}

QLabel#FlowTitle {
    font-size: 13px;
    font-weight: 600;
    color: #214a70;
}

QLabel#FlowDesc {
    font-size: 12px;
    color: #6b849e;
}

QPushButton#EnterButton {
    background: #edf5ff;
    border: 1px solid #d2e3f7;
    border-radius: 8px;
    color: #295881;
    padding: 6px 10px;
}

QPushButton#EnterButton:hover {
    background: #e3effd;
}

QLabel#ModuleTitle {
    font-size: 15px;
    font-weight: 600;
    color: #1f4568;
}

QLabel#ModuleDesc {
    color: #67819a;
    font-size: 12px;
}

QLabel#ModuleStatusReady,
QLabel#ModuleStatusPending,
QLabel#ModuleStatusRunnable {
    border-radius: 10px;
    padding: 2px 8px;
    font-size: 11px;
}

QLabel#ModuleStatusReady {
    background: #eaf7f1;
    color: #2d7454;
    border: 1px solid #c9e8d8;
}

QLabel#ModuleStatusPending {
    background: #fff8e8;
    color: #8b6724;
    border: 1px solid #f0dfb4;
}

QLabel#ModuleStatusRunnable {
    background: #edf5ff;
    color: #2b5f94;
    border: 1px solid #d2e3f7;
}

QLabel#KeyLabel {
    color: #6f879f;
    font-size: 12px;
}

QLabel#KeyValue {
    color: #1f4568;
    font-size: 14px;
    font-weight: 600;
}

QLabel#RecentTitle {
    color: #1f4568;
    font-size: 13px;
    font-weight: 600;
}

QLabel#RecentDesc {
    color: #668099;
    font-size: 12px;
}

QLabel#MetricBadge {
    background: #eef5fd;
    border: 1px solid #d2e3f7;
    border-radius: 10px;
    padding: 2px 8px;
    color: #2a6298;
    font-size: 11px;
}



QScrollArea {
    border: none;
    background: transparent;
}

QLabel#ImagePreview {
    border: 1px dashed #c6d8eb;
    border-radius: 8px;
    background: #f7fbff;
    color: #6b839d;
    padding: 10px;
}

QLineEdit#InputControl,
QComboBox#InputControl {
    background: #ffffff;
    border: 1px solid #d2e3f4;
    border-radius: 8px;
    padding: 6px 8px;
    color: #264761;
}

QComboBox#InputControl::drop-down {
    border: none;
}

QCheckBox#InputCheck {
    color: #365a77;
}

QProgressBar#TaskProgress {
    border: 1px solid #d2e3f4;
    border-radius: 8px;
    background: #f5f9fe;
    text-align: center;
    color: #2a4f70;
}

QProgressBar#TaskProgress::chunk {
    background: #5f9bd8;
    border-radius: 6px;
}

QTableWidget#DataTable {
    background: #ffffff;
    border: 1px solid #d9e5f2;
    border-radius: 10px;
    gridline-color: #e8eef6;
}

QTableWidget#DataTable::item {
    padding: 4px;
}

QHeaderView::section {
    background: #f0f6fd;
    color: #365a77;
    border: 0;
    border-bottom: 1px solid #d9e5f2;
    padding: 6px;
    font-weight: 600;
}

QTextEdit#TaskLog {
    background: #f8fbff;
    border: 1px solid #d9e5f2;
    border-radius: 10px;
    color: #54708a;
    padding: 6px;
}

QFrame#PlaceholderPanel {
    background: #ffffff;
    border: 1px dashed #c9d8e8;
    border-radius: 14px;
}

QLabel#PlaceholderTitle {
    color: #1f4668;
    font-size: 16px;
    font-weight: 600;
}

QLabel#PlaceholderDesc {
    color: #6e879f;
    font-size: 12px;
}
"""
