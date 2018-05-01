import maya.cmds as cmds
from PySide2 import QtCore, QtWidgets, QtGui
import maya.OpenMayaUI as omui

# import wrapInstance
try:
    from shiboken2 import wrapInstance
except ImportError:
    from shiboken import wrapInstance

class PyQtBaseWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(PyQtBaseWindow, self).__init__(parent)

        self.main_widget = QtWidgets.QWidget()

        # Rig Window setup
        self.setWindowTitle('Wagner ToolBox')
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.setLayout(self.main_layout)

        ## Label Layout
        self.toolbox_label = QtWidgets.QLabel('Wagner ToolBox              V - 1.0')
        self.toolbox_label.setAlignment(QtCore.Qt.AlignCenter)

        ## Character Rig Setting
        self.character_box_label = QtWidgets.QLabel('CHARACTER')
        self.character_box_layout = QtWidgets.QHBoxLayout()
        # Character Name Line Edit
        self.character_lineEdit_label = QtWidgets.QLabel('Character Name:')
        self.character_lineEdit = QtWidgets.QLineEdit()
        #self.character_lineEdit.textChanged.connect(self.character_lineEdit_changed)

        self.character_lineEdit.editingFinished.connect(self.character_lineEdit_changed)

        ## Joint Setup Buttons
        self.button_box_label = QtWidgets.QLabel('MODULAR JOINT CREATION')
        self.button_box_layout = QtWidgets.QHBoxLayout()

        self.arm_button = QtWidgets.QPushButton('Arm')
        self.arm_button.setMinimumHeight(35)
        self.arm_button.setMinimumWidth(60)
        self.arm_button.setStyleSheet('background-color: rgb(50, 50, 50)')
        self.arm_button.clicked.connect(self.arm_button_clicked)
        
        self.hand_button = QtWidgets.QPushButton('Hand')
        self.hand_button.setMinimumHeight(35)
        self.hand_button.setMinimumWidth(60)
        self.hand_button.setStyleSheet('background-color: rgb(50, 50, 50)')
        self.hand_button.clicked.connect(self.hand_button_clicked)
        
        self.leg_button = QtWidgets.QPushButton('Leg')
        self.leg_button.setMinimumHeight(35)
        self.leg_button.setMinimumWidth(60)
        self.leg_button.setStyleSheet('background-color: rgb(50, 50, 50)')
        self.leg_button.clicked.connect(self.leg_button_clicked)
        
        self.spine_button = QtWidgets.QPushButton('Spine')
        self.spine_button.setMinimumHeight(35)
        self.spine_button.setMinimumWidth(60)
        self.spine_button.clicked.connect(self.spine_button_clicked)
        self.spine_button.setStyleSheet('background-color: rgb(50, 50, 50)')
        
        self.head_button = QtWidgets.QPushButton('Head')
        self.head_button.setMinimumHeight(35)
        self.head_button.setMinimumWidth(60)
        self.head_button.setStyleSheet('background-color: rgb(50, 50, 50)')        
        self.head_button.clicked.connect(self.head_button_clicked)


        ## Stretchy joint options check boxes
        self.checkbox_label = QtWidgets.QLabel('STRETCHY JOINTS')
        self.checkbox_layout = QtWidgets.QHBoxLayout()

        self.stretchy_arm_checkbox = QtWidgets.QCheckBox('Arm')
        self.stretchy_arm_checkbox.stateChanged.connect(self.str_arm_state_changed)
        self.stretchy_leg_checkbox = QtWidgets.QCheckBox('Leg')
        self.stretchy_leg_checkbox.stateChanged.connect(self.str_leg_state_changed)
        self.stretchy_spine_checkbox = QtWidgets.QCheckBox('Spine')
        self.stretchy_spine_checkbox.stateChanged.connect(self.str_spine_state_changed)
        self.stretchy_neck_checkbox = QtWidgets.QCheckBox('Neck')
        self.stretchy_neck_checkbox.stateChanged.connect(self.str_neck_state_changed)

        ## Number of Joints Spinbox
        # Spinbox HBox Layout Label
        self.spinbox_label = QtWidgets.QLabel('NUMBER OF JOINTS')
        self.spinbox_layout = QtWidgets.QHBoxLayout()

        # Spinbox Spine joint number
        self.spine_spinbox_label = QtWidgets.QLabel('Spine:')
        self.spine_num_spinbox = QtWidgets.QSpinBox()
        self.spine_num_spinbox.valueChanged.connect(self.spine_spinbox_valueChanged)
        self.neck_spinbox_label = QtWidgets.QLabel('Neck:')
        self.neck_num_spinbox = QtWidgets.QSpinBox()
        self.neck_num_spinbox.valueChanged.connect(self.neck_spinbox_valueChanged)

        # QFrame Practice

        self.test_frame = QtWidgets.QFrame()
        self.test_frame.setFrameStyle(QtWidgets.QFrame.Box)
        self.test_frame.setLineWidth(3)
        self.test_frame.setStyleSheet('background-color: rgb(50, 50, 50)')
        self.test_button = QtWidgets.QPushButton('Test')


        ## Rig Window Layout
        self.main_layout.addWidget(self.toolbox_label)

        self.main_layout.addWidget(self.character_box_label)
        self.main_layout.addLayout(self.character_box_layout)
        self.character_box_layout.addWidget(self.character_lineEdit_label)
        self.character_box_layout.addWidget(self.character_lineEdit)

        self.main_layout.addWidget(self.button_box_label)
        self.main_layout.addLayout(self.button_box_layout)

        self.button_box_layout.addWidget(self.arm_button)
        self.button_box_layout.addWidget(self.hand_button)
        self.button_box_layout.addWidget(self.leg_button)
        self.button_box_layout.addWidget(self.spine_button)
        self.button_box_layout.addWidget(self.head_button)

        self.main_layout.addWidget(self.checkbox_label)
        self.main_layout.addLayout(self.checkbox_layout)

        self.checkbox_layout.addWidget(self.stretchy_arm_checkbox)
        self.checkbox_layout.addWidget(self.stretchy_leg_checkbox)
        self.checkbox_layout.addWidget(self.stretchy_spine_checkbox)
        self.checkbox_layout.addWidget(self.stretchy_neck_checkbox)

        self.main_layout.addWidget(self.spinbox_label)
        self.main_layout.addLayout(self.spinbox_layout)
        self.spinbox_layout.addWidget(self.spine_spinbox_label)
        self.spinbox_layout.addWidget(self.spine_num_spinbox)
        self.spinbox_layout.addWidget(self.neck_spinbox_label)
        self.spinbox_layout.addWidget(self.neck_num_spinbox)

        #self.spinbox_layout.addWidget(self.test_frame)
        #self.spinbox_layout.addWidget(self.test_button)

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    #GUI Class Functions
    def character_lineEdit_changed(self):
        print(self.character_lineEdit.text())

    def arm_button_clicked(self):
        print('Creating Arm joints')

    def hand_button_clicked(self):
        print('Creating Hand joints')
        testJoints.hand_joint_creation()

    def leg_button_clicked(self):
        print('Creating Leg joints')
        testJoints.Leg_joint_creation()

    def spine_button_clicked(self):
        print('Creating Spine joints')

    def head_button_clicked(self):
        print('Creating Head joints')

    def str_arm_state_changed(self):
        if self.stretchy_arm_checkbox.isChecked() == True:
            print('Stretchy Arm Checked')
        else:
            print('Stretchy Arm Unchecked')

    def str_leg_state_changed(self):
        if self.stretchy_leg_checkbox.isChecked() == True:
            print('Stretchy Leg Checked')
        else:
            print('Stretchy Leg Unchecked')

    def str_spine_state_changed(self):
        if self.stretchy_spine_checkbox.isChecked() == True:
            print('Stretchy Spine Checked')
        else:
            print('Stretchy Spine Unchecked')

    def str_neck_state_changed(self):
        if self.stretchy_neck_checkbox.isChecked() == True:
            print('Stretchy Neck Checked')
        else:
            print('Stretchy Neck Unchecked')

    def spine_spinbox_valueChanged(self):
        self.spine_jnt_num = self.spine_num_spinbox.value()
        print(self.spine_jnt_num)

    def neck_spinbox_valueChanged(self):
        self.neck_jnt_num = self.neck_num_spinbox.value()
        return self.neck_jnt_num


m_rigging_window = PyQtBaseWindow()
m_rigging_window.show()
