import maya.cmds as mc
from PySide import QtCore, QtGui

class StretchySplineIK(QtGui.QDialog):
    """
    GUI wrapper for create "createStretchyIkSpline()"
    """
    
    def __init__(self, parent=None):
	    super(StretchySplineIK, self).__init__(parent)
	    
	    # Window Setup
	    self.setWindowTitle( 'Stretchy Spline Ik Tool' )
	    self.main_layout = QtGui.QVBoxLayout()
	    self.setLayout(self.main_layout)
	    
	    # Label Setup
	    joint_number_label = QtGui.QLabel( 'Number of Joints' )
	    joint_number_HBox = QtGui.QHBoxLayout()
	    
	    # SpinBox
	    self.joint_number_spin = QtGui.QSpinBox()
	    
	    # Button setup
	    button_box = QtGui.QHBoxLayout()
	    self.setup_button = QtGui.QPushButton('setup')
	    self.setup_button.clicked.connect(self.setup_button_clicked)
	    
	    # Layout
	    self.main_layout.addWidget(joint_number_label)
	    self.main_layout.addLayout(joint_number_HBox)
	    self.main_layout.addWidget(self.joint_number_spin)
	    self.main_layout.addLayout(button_box)
	    self.main_layout.addWidget(self.setup_button)
	
	
    def setup_button_clicked(self):
        createStretchyIkSpline(s_curve=mc.ls(sl=True), jnt_num=self.joint_number_spin.value())
        

#test_ui = StretchySplineIK()
#test_ui.show()  
