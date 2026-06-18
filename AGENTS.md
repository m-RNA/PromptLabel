# AGENTS.md

- 面向用户的结论用中文。
- 修改后要提交 Git；提交信息用中文，主题行带 `fix/feat/refactor/docs/test` 等前缀，正文说明改了什么。
- 项目核心卖点：一个 YOLO 类别可对应多个提示词别名；README 要突出这个点、左侧图集预览和紧凑工作台。
- 软件记忆保存到软件根目录 `PromptLabel.ini`，不要再用注册表；该文件不提交。
- 不要把 `models/sam3.pt`、`.sam3_tmp/`、日志、缓存、本地测试图片打进仓库或 release。
- 常用检查：`.\.venv311\Scripts\python.exe -m py_compile main.py main_dataset_tool.py ui\main_window.py core\sam_client.py`
- 打包命令：`.\.venv311\Scripts\pyinstaller.exe --clean --noconfirm PromptLabel.spec`
