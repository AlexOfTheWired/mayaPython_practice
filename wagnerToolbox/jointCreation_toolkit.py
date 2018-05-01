import maya.cmds as mc

class JointCreation():

    def __init__(
                 self,
                 jnt_num = 3,
                 ):


        self.test_jnt_list = []


    def hand_joint_creation(self, f_num=5, f_jnt_num=3):
        mc.select(clear=True)

        base_joint = mc.joint(
                              name='%s_%s_jnt_%s'%(m_rigging_window.character_lineEdit.text(),'wrist','1'),
                              p=(0,0,0,),
                              sym=True,
                              sa='x')

        finger_spacing = 2
        palm_length = 4
        joint_length = 2
        jnt_name = ['thumb', 'index', 'middle', 'ring', 'pinky']



        for idx in range(f_num):

            mc.select(base_joint, replace=True)
            pos = [0, palm_length, 0]
            f_idx = (idx+1)

            pos[0] = (idx * finger_spacing) - ((f_num-1)* finger_spacing) / 2

            mc.joint(
                     n='%s_%s_jnt_%s'%(m_rigging_window.character_lineEdit.text(),jnt_name[idx],f_idx),
                     p=pos,
                     sym=True,
                     sa='x'
                     )

            for jnt in range(f_jnt_num):
                f_jnt_idx = (jnt+1)
                mc.joint(
                         n='%s_%s_jnt_%s'%(m_rigging_window.character_lineEdit.text(),jnt_name[idx],f_jnt_idx),
                         relative=True,
                         p=(0,joint_length,0),
                         sym=True,
                         sa='x'
                         )

            mc.select(base_joint,replace=True)

    def Leg_joint_creation(self):
        
        mc.select(cl=True)
            
        leg_pos = [0,23,0]
        leg_jnt_name = ['hip','knee','ankle','ball','toe']
        leg_jnt_list = []
        
        for idx in range(len(leg_jnt_name)):
            l_jnt_idx = (idx + 1)
            leg_jnt = mc.joint(
                               n='%s_%s_jnt_%s'%(m_rigging_window.character_lineEdit.text(),leg_jnt_name[idx],l_jnt_idx),
                               p=(leg_pos[0],leg_pos[1],leg_pos[2]),
                               sym = True,
                               sa = 'x')
            leg_jnt_list.append(leg_jnt)         
            leg_pos[1] -= 10.0
            print(leg_jnt_list)
            
        mc.move(0, 8, 1.5, leg_jnt_list[-2], r=True)
        mc.move(0, 9, 6, leg_jnt_list[-1], r=True) 


    def spine_joint_creation(s_jnt_num):
        

testJoints = JointCreation()

testJoints.hand_joint_creation()
testJoints.Leg_joint_creation()
