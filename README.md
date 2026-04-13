# intelligent-underwater-acoustic-system

智能水声数据生成及轻量化识别系统（PyQt6 桌面版原型）。

## 本地运行

```bash
python -m venv .venv
source .venv/bin/activate  # Windows 使用 .venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

## 当前版本（首页重构）

- 首页重构为浅色、科研风工作台界面，适合论文展示截图。
- 主布局：顶部总栏（标题/副标题/状态标签）+ 左侧轻量导航 + 右侧首页内容。
- 首页板块：Hero 主视觉、流程区、2×2 模块入口卡片、系统状态概览、最近任务与结果。
- 支持基础交互：导航切换、模块卡片按钮点击、占位页面跳转。
- Mock 数据统一由 `configs/mock_data.json` 管理，便于后续替换真实业务接口。

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
