import maya.cmds as cmds
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

try:
    from shiboken2 import wrapInstance
except ImportError:
    from shiboken import wrapInstance

# get Maya's main window
def getMayaMainWindow():
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)

mayaMainWindow = getMayaMainWindow()


class ToolboxMainWindow(QMainWindow):


    def __init__(self, parent=None):
        super(ToolboxMainWindow, self).__init__(parent)

        self.main_widget = QWidget()

        # Rig Window setup
        self.setWindowTitle('WAGNER TOOLBOX')
        self.main_layout = QVBoxLayout(self.main_widget)
        self.setLayout(self.main_layout)

        ## Label Layout
        self.toolbox_label = QLabel('WAGNER TOOLBOX              V - 1.0')
        self.toolbox_label.setAlignment(QtCore.Qt.AlignCenter)
        self.toolbox_label.setStyleSheet('font: 14pt')

        ## Toolbox Tools Button Layout
        self.button_box_label = QLabel('Character Setup Tools')
        self.button_box_layout = QHBoxLayout()

        self.procedural_button = QPushButton('Procedural Character Setup')
        self.procedural_button.setMinimumHeight(35)
        self.procedural_button.setStyleSheet('background-color: rgb(50, 50, 50)')
        self.procedural_button.clicked.connect(self.procedural_button_clicked)

        self.modular_button = QPushButton('Modular Character Setup')
        self.modular_button.setMinimumHeight(35)
        self.modular_button.setStyleSheet('background-color: rgb(50, 50, 50)')
        self.modular_button.clicked.connect(self.modular_button_clicked)

        ## Muscle System Manager

        ## Weights Exporter/Importer
        self.weights_manager_label = QLabel('Weights Manager')
        self.weights_manager_layout = QHBoxLayout()

        self.weights_manager_button = QPushButton('Weights Export/Import')
        self.weights_manager_button.setStyleSheet('background-color: rgb(50, 50, 50)')
        self.weights_manager_button.setMinimumHeight(40)
        self.weights_manager_button.clicked.connect(self.weights_button_clicked)


        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)


        ## Rig Window Layout
        self.main_layout.addWidget(self.toolbox_label)
        self.main_layout.addWidget(self.button_box_label)
        self.main_layout.addLayout(self.button_box_layout)
        self.button_box_layout.addWidget(self.procedural_button)
        self.button_box_layout.addWidget(self.modular_button)
        self.main_layout.addWidget(self.weights_manager_label)
        self.main_layout.addLayout(self.weights_manager_layout)
        self.weights_manager_layout.addWidget(self.weights_manager_button)


    def procedural_button_clicked(self):
        print('Procedural Charcter Setup Window')


    def modular_button_clicked(self):
        print('Modular Charcter Setup Window')
        m_rigging_window.setWindowModality(ToolboxMainWindow)
        m_rigging_window.show()

    def weights_button_clicked(self):
        print('Weights Export/Import Window')


main_window = ToolboxMainWindow()
main_window.show()
