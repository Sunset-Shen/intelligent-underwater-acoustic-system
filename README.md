# intelligent-underwater-acoustic-system

智能水声数据生成及轻量化识别系统（PyQt6 桌面版原型）。

## 本地运行

```bash
python -m venv .venv
source .venv/bin/activate  # Windows 使用 .venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

## 当前版本（首页 + 数据管理页）

- 首页：浅色科研风总览工作台，展示完整链路与模块入口。
- 数据管理页：围绕“数据接入与预处理”构建，包含：
  - 页面标题区
  - 数据集接入区
  - 数据集概览区
  - 预处理参数配置区
  - 预处理任务执行区
  - 预处理结果预览区
- 左侧导航点击“数据管理”可进入该页面。
- 所有展示内容采用 `configs/mock_data.json`，便于后续替换为真实业务接口。

## 目录结构

```text
main.py
app/
  main_window.py
  pages/
    home_page.py
    data_page.py
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
