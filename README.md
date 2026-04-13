# intelligent-underwater-acoustic-system

智能水声数据生成及轻量化识别系统（PyQt6 桌面版主界面原型）。

## 本地运行

```bash
python -m venv .venv
source .venv/bin/activate  # Windows 使用 .venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

## 当前实现（第一轮仅主界面）

- 基于 **Python + PyQt6** 的本地桌面应用入口与工程结构。
- 主窗口布局：顶部信息区 + 左侧导航区 + 右侧主内容区。
- 首页包含：欢迎主视觉、流程概览、4 个核心功能卡片、系统概览、最近结果预览。
- 导航按钮与功能卡片均可点击，点击后切换到占位页面（即将完善）。
- 所有展示数据通过 `configs/mock_data.json` 管理，便于后续替换为真实接口数据。

## 目录结构

```text
main.py
app/
  main_window.py
  pages/
    home_page.py
  widgets/
    nav_button.py
  styles/
    theme.py
  services/
    mock_data_service.py
configs/
  mock_data.json
requirements.txt
```

## 后续扩展建议

- 新增 `app/pages/data_page.py`、`generation_page.py`、`recognition_page.py`、`results_page.py` 逐步替换占位页面。
- 在 `app/services` 中增加任务服务层，对接真实算法模块、日志与模型推理结果。
- 将 QSS 主题继续拆分为配色/组件样式文件，并引入资源图标与字体包。
- 在不暴露调试入口的前提下，持续使用 `configs/` 或资源目录维护演示数据版本。
