from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QToolBar, QListWidget,
    QGraphicsView, QLabel, QLineEdit, QPushButton, QStatusBar, QMenu,
    QSplitter, QListView, QToolBox, QComboBox, QAbstractItemView, QTreeWidget
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QAction, QActionGroup, QPainter


class FormatSelectorWidget(QWidget):
    format_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        self.label = QLabel("标注格式")
        self.label.setObjectName("toolbarFieldLabel")
        self.btn = QPushButton("YOLO ▾")
        self.btn.setObjectName("toolbarSelectButton")
        self.menu = QMenu(self)
        self.act_json = QAction("JSON", self)
        self.act_yolo = QAction("YOLO", self)
        self.act_xml = QAction("XML", self)
        self.menu.addAction(self.act_json)
        self.menu.addAction(self.act_yolo)
        self.menu.addAction(self.act_xml)
        self.btn.setMenu(self.menu)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)
        self.act_json.triggered.connect(lambda: self._on_format_selected("json", "JSON ▾"))
        self.act_yolo.triggered.connect(lambda: self._on_format_selected("yolo", "YOLO ▾"))
        self.act_xml.triggered.connect(lambda: self._on_format_selected("xml", "XML ▾"))

    def _on_format_selected(self, fmt, text):
        self.btn.setText(text)
        self.format_changed.emit(fmt)

    def set_format(self, fmt):
        text_map = {"json": "JSON ▾", "yolo": "YOLO ▾", "xml": "XML ▾"}
        self.btn.setText(text_map.get(fmt, "YOLO ▾"))


class ThemeSelectorWidget(QWidget):
    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        self.label = QLabel("主题")
        self.label.setObjectName("toolbarFieldLabel")
        self.combo = QComboBox()
        self.combo.setObjectName("toolbarThemeCombo")
        self.combo.addItem("跟随系统", "system")
        self.combo.addItem("浅色", "light")
        self.combo.addItem("深色", "dark")
        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        self.combo.currentIndexChanged.connect(lambda _: self.theme_changed.emit(self.combo.currentData()))

    def set_theme(self, theme_key):
        for i in range(self.combo.count()):
            if self.combo.itemData(i) == theme_key:
                self.combo.setCurrentIndex(i)
                return


class SwitchControl(QWidget):
    toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 26)
        self._checked = False

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        if self._checked != checked:
            self._checked = checked
            self.toggled.emit(checked)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setChecked(not self._checked)
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.darkGreen if self._checked else Qt.gray)
        painter.drawRoundedRect(self.rect(), 13, 13)
        painter.setBrush(Qt.white)
        x = self.width() - 24 if self._checked else 2
        painter.drawEllipse(x, 2, 22, 22)


class CanvasView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setAlignment(Qt.AlignCenter)
        self.setFocusPolicy(Qt.StrongFocus)
        self._is_panning = False
        self._pan_start_pos = None

    def wheelEvent(self, event):
        factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
        self.scale(factor, factor)

    def mousePressEvent(self, event):
        self.setFocus()
        if event.button() == Qt.MiddleButton:
            self._is_panning = True
            self._pan_start_pos = event.position().toPoint()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        scene = self.scene()
        if scene is not None:
            scene.keyPressEvent(event)
            if event.isAccepted():
                return
        super().keyPressEvent(event)

    def mouseMoveEvent(self, event):
        if self._is_panning:
            delta = event.position().toPoint() - self._pan_start_pos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self._pan_start_pos = event.position().toPoint()
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self._is_panning = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("LuoHuaLabel")
        MainWindow.resize(1500, 900)

        self.centralWidget = QWidget(MainWindow)
        self.mainLayout = QHBoxLayout(self.centralWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        MainWindow.setCentralWidget(self.centralWidget)

        self.toolBar = QToolBar("工具栏")
        self.toolBar.setOrientation(Qt.Vertical)
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextOnly)
        MainWindow.addToolBar(Qt.LeftToolBarArea, self.toolBar)

        self.actionOpen = QAction("打开目录", MainWindow)
        self.actionRect = QAction("矩形 (R)", MainWindow)
        self.actionPoly = QAction("多边形 (P)", MainWindow)
        self.actionPoint = QAction("点 (T)", MainWindow)
        self.actionRBox = QAction("旋转框 (O)", MainWindow)
        self.actionToggleRightPanel = QAction("右侧面板", MainWindow)
        self.actionToggleRightPanel.setCheckable(True)
        self.actionToggleRightPanel.setChecked(True)

        self.modeGroup = QActionGroup(MainWindow)
        for action in [self.actionRect, self.actionPoly, self.actionPoint, self.actionRBox]:
            action.setCheckable(True)
            self.modeGroup.addAction(action)
        self.actionRect.setChecked(True)

        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.formatWidget = FormatSelectorWidget()
        self.toolBar.addWidget(self.formatWidget)
        self.themeWidget = ThemeSelectorWidget()
        self.toolBar.addWidget(self.themeWidget)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRect)
        self.toolBar.addAction(self.actionPoly)
        self.toolBar.addAction(self.actionPoint)
        self.toolBar.addAction(self.actionRBox)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionToggleRightPanel)

        self.splitter = QSplitter(Qt.Horizontal)
        self.mainLayout.addWidget(self.splitter)

        self.leftPanel = QWidget()
        self.leftLayout = QVBoxLayout(self.leftPanel)
        self.leftLayout.addWidget(QLabel("图集"))
        self.listFiles = QListWidget()
        self.listFiles.setObjectName("fileGrid")
        self.listFiles.setViewMode(QListView.IconMode)
        self.listFiles.setResizeMode(QListView.Adjust)
        self.listFiles.setMovement(QListView.Static)
        self.listFiles.setWrapping(True)
        self.listFiles.setIconSize(QSize(132, 132))
        self.listFiles.setGridSize(QSize(148, 172))
        self.listFiles.setWordWrap(True)
        self.leftLayout.addWidget(self.listFiles)

        self.centerPanel = QWidget()
        self.centerLayout = QVBoxLayout(self.centerPanel)
        self.centerLayout.addWidget(QLabel("标注画布"))
        self.view = CanvasView()
        self.centerLayout.addWidget(self.view, 1)

        self.samRow = QWidget()
        self.samRowLayout = QHBoxLayout(self.samRow)
        self.samRowLayout.setContentsMargins(0, 0, 0, 0)
        self.samRowLayout.addWidget(QLabel("SAM"))
        self.samSwitch = SwitchControl()
        self.samRowLayout.addWidget(self.samSwitch)
        self.samRowLayout.addWidget(QLabel("提示词"))
        self.samPromptInput = QComboBox()
        self.samPromptInput.setEditable(True)
        self.samPromptInput.setInsertPolicy(QComboBox.NoInsert)
        self.samPromptInput.lineEdit().setPlaceholderText("输入或选择提示词，如 dog")
        self.samRowLayout.addWidget(self.samPromptInput, 1)
        self.samPromptBtn = QPushButton("提交")
        self.samRowLayout.addWidget(self.samPromptBtn)
        self.samRefBtn = QPushButton("参考查找")
        self.samRowLayout.addWidget(self.samRefBtn)
        self.btnHelp = QPushButton("帮助")
        self.samRowLayout.addWidget(self.btnHelp)
        self.centerLayout.addWidget(self.samRow)

        self.rightPanel = QWidget()
        self.rightLayout = QVBoxLayout(self.rightPanel)
        self.annotationTitle = QLabel("标注")
        self.annotationTitle.setObjectName("rightSectionTitle")
        self.labelTitle = QLabel("标签")
        self.labelTitle.setObjectName("rightSectionTitle")
        self.annotationListTitle = QLabel("标注列表")
        self.annotationListTitle.setObjectName("rightSectionTitle")

        self.rightLayout.addWidget(self.annotationTitle)
        self.rightInnerSplitter = QSplitter(Qt.Vertical)
        self.rightInnerSplitter.setObjectName("rightInnerSplitter")

        self.labelPanel = QWidget()
        self.labelPanelLayout = QVBoxLayout(self.labelPanel)
        self.labelPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.labelPanelLayout.setSpacing(6)
        self.labelPanelLayout.addWidget(self.labelTitle)
        self.listClasses = QTreeWidget()
        self.listClasses.setHeaderHidden(True)
        self.listClasses.setContextMenuPolicy(Qt.CustomContextMenu)
        self.labelPanelLayout.addWidget(self.listClasses)

        self.annotationPanel = QWidget()
        self.annotationPanelLayout = QVBoxLayout(self.annotationPanel)
        self.annotationPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.annotationPanelLayout.setSpacing(6)
        self.annotationPanelLayout.addWidget(self.annotationListTitle)
        self.annotationToolBox = QToolBox()
        self.annotationToolBox.setObjectName("annotationToolBox")
        self.rectStatsList = QListWidget()
        self.polyStatsList = QListWidget()
        self.pointStatsList = QListWidget()
        self.rboxStatsList = QListWidget()
        for widget in (self.rectStatsList, self.polyStatsList, self.pointStatsList, self.rboxStatsList):
            widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.rectStatsIndex = self.annotationToolBox.addItem(self.rectStatsList, "矩形标注")
        self.polyStatsIndex = self.annotationToolBox.addItem(self.polyStatsList, "多边形标注")
        self.pointStatsIndex = self.annotationToolBox.addItem(self.pointStatsList, "点标注")
        self.rboxStatsIndex = self.annotationToolBox.addItem(self.rboxStatsList, "旋转框标注")
        self.annotationPanelLayout.addWidget(self.annotationToolBox)

        self.rightInnerSplitter.addWidget(self.labelPanel)
        self.rightInnerSplitter.addWidget(self.annotationPanel)
        self.rightInnerSplitter.setCollapsible(0, True)
        self.rightInnerSplitter.setCollapsible(1, True)
        self.rightInnerSplitter.setSizes([260, 420])
        self.rightLayout.addWidget(self.rightInnerSplitter, 1)
        self.btnDatasetTool = QPushButton("数据集处理")
        self.rightLayout.addWidget(self.btnDatasetTool)

        self.splitter.addWidget(self.leftPanel)
        self.splitter.addWidget(self.centerPanel)
        self.splitter.addWidget(self.rightPanel)
        self.splitter.setCollapsible(2, True)
        self.splitter.setSizes([320, 860, 320])

        self.statusBar = QStatusBar()
        MainWindow.setStatusBar(self.statusBar)
        self.coordLabel = QLabel("坐标: X: 0, Y: 0")
        self.statusBar.addPermanentWidget(self.coordLabel)
