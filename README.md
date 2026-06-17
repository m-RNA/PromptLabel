# PromptLabel

PromptLabel 是基于 [luohuabuxiema/LabelPaw](https://github.com/luohuabuxiema/LabelPaw) 改造的图像标注工作台。这个分支不是原作者官方版本，重点也不是新增一种标注格式，而是按个人习惯修改界面&小功能。

当前版本是 beta。功能可用，但打包体积、模型加载体验和部分边界交互还会继续优化。

## 核心卖点

### 一个类别，多个提示词

这是 PromptLabel 最重要的改动。

原工具里，类别和提示词的关系不够适合“用不同说法找同一类目标”的工作流。PromptLabel 允许一个 YOLO 类别绑定多个提示词别名，例如：

```text
helmet
├─ helmet
├─ hard hat
└─ safety helmet
```

使用 SAM 文本提示时，可以用任意别名去找目标；保存和导出时仍然只写入同一个 YOLO 类别 `helmet`。这样既能保留提示词的灵活性，也不会把训练集类别搞乱。

### 左侧图集预览

打开目录后，当前目录下的图片会作为“图片队列”显示在左侧：缩略图、文件名、已标注/未标注状态都能直接看到。连续标注时不用反复打开文件选择器，也更容易发现漏标图片。

### 紧凑标注工作台

界面重新组织为左侧图片队列、中央画布、右侧类别/标注管理、底部 SAM 工作流。相比原界面，PromptLabel 更强调画布空间、信息密度和少打断操作。

![PromptLabel 主界面](assets/readme_main_ui.png)

### 更少打扰的小优化

- 提示词下拉框滚动只切换内容，不会误提交 SAM 提示词。
- 标注框支持可关闭的呼吸高亮，方便快速识别已有标注。
- 类别树里直接管理提示词别名、颜色、显示/隐藏状态。
- 标注列表按矩形、多边形、点、旋转框分组，支持选择、改标签、删除。
- 减少吐司消息，更多信息放到状态栏，避免遮挡画布。
- 下拉框和树形控件的小三角样式已统一，深色/浅色主题都可见。

## 功能保留

- 标注格式：`JSON` / `YOLO` / `XML`
- 标注类型：矩形、多边形、点、旋转框
- SAM3 辅助：点选、文本提示词、参考查找
- 类别管理：新增、编辑、删除、颜色、显示/隐藏、提示词别名
- 图片目录：缩略图队列、上一张/下一张、已标注状态、右键删除图片及标注
- 常用操作：撤销、重做、删除、保存、坐标显示、当前模式和当前类别提示
- 数据集处理：划分训练/验证/测试集，JSON/XML 转 YOLO，JSON 转 U-Net Mask

## 模型说明

Release 不内置 `models/sam3.pt`。缺少模型时，主界面仍可打开，手动标注和数据集处理可以继续使用，SAM 智能辅助不可用。启动时也可以点“我已下载”直接选择已有的 `sam3.pt` 文件，程序会记住路径，不要求复制到项目目录。

建议优先从官方来源下载：

- [facebook/sam3 on Hugging Face](https://huggingface.co/facebook/sam3/tree/main)
- [facebookresearch/sam3](https://github.com/facebookresearch/sam3)

备用下载：

- [百度网盘 sam3.pt](https://pan.baidu.com/s/11rKzO6W5b_i8aOFcd9xOzA?pwd=6666)，提取码：`6666`

`sam3.pt` 属于 SAM Materials，受 `SAM_LICENSE.txt` 约束。备用网盘只是为了方便下载，使用和再分发前请确认遵守 Meta 的 SAM License。

下载后可以在弹窗里直接选择文件，或放到默认路径：

```text
models/sam3.pt
```

## 运行方式

### Beta 便携包

1. 从 Release 页面下载 `PromptLabel-v0.1.0-beta.1` 便携包。
2. 解压到同一个目录。
3. 将 `sam3.pt` 放到 `models/sam3.pt`。
4. 双击 `PromptLabel.exe` 启动。

### 源码运行

推荐 Windows + Python 3.11 + NVIDIA CUDA 环境。

```powershell
python -m venv .venv311
.\.venv311\Scripts\pip install -r requirements.txt
.\.venv311\Scripts\python main.py
```

### 本地打包

仓库已提供 `PromptLabel.spec`。打包前确认 `.venv311` 中已安装依赖和 PyInstaller：

```powershell
.\.venv311\Scripts\pip install pyinstaller
.\.venv311\Scripts\pyinstaller.exe --clean --noconfirm PromptLabel.spec
```

输出目录为 `dist\PromptLabel\`。Release 包不应内置 `models\sam3.pt`、`.sam3_tmp\`、日志、缓存或本地测试图片；用户可在首次启动时选择已有模型文件，或放到 `models\sam3.pt`。

## 快捷键

| 快捷键 | 功能 |
| ------ | ---- |
| `A` / `←` | 上一张图片 |
| `D` / `→` | 下一张图片 |
| `Ctrl + S` | 保存当前标注 |
| `R` / `P` / `T` / `O` | 矩形 / 多边形 / 点 / 旋转框 |
| `Q` / `Space` | 开启/关闭 SAM |
| `Del` / `Backspace` | 删除选中标注 |
| `Ctrl + Z` | 撤销 |
| `Ctrl + Y` / `Ctrl + Shift + Z` | 重做 |
| `1` - `9` | 切换当前类别 |
| `E` | 修改选中标注标签 |
| `F1` | 打开帮助 |

## License

本项目沿用原项目许可，并保留 `SAM_LICENSE.txt` 用于说明 SAM3 相关许可信息。
