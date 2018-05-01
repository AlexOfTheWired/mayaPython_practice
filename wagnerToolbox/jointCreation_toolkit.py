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
        
        mc.move(0,0,2, leg_jnt_list[1],r=True)
        mc.move(0,0,-2, leg_jnt_list[2],r=True)                    
        mc.move(0, 7, 1.5, leg_jnt_list[-2], r=True)
        mc.move(0, 10, 6, leg_jnt_list[-1], r=True) 


    def arm_joint_creation(self, a_jnt_num = 4):
        
        mc.select(cl=True)
        
        arm_jnt_name = ['clavicle','shoulder','elbow','wrist']
        a_jnt_list = []
        a_pos = [2,0,0]
        arm_length = 25
        arm_average = (arm_length/a_jnt_num)
        
        for idx in range(a_jnt_num):
            a_idx = (idx + 1)
            arm_jnt = mc.joint(
                                 n='%s_%s_jnt_1'%(m_rigging_window.character_lineEdit.text(),arm_jnt_name[idx]),
                                 p=(a_pos),
                                 sym=True,
                                 sa='x')
            a_jnt_list.append(arm_jnt)
            print(a_jnt_list)
            
        for jnt in range(1,len(a_jnt_list)):
            mc.setAttr('%s.translateX'%(a_jnt_list[jnt]),arm_average)
        
        mc.move(-3,0,0, a_jnt_list[1],r=True)



    def spine_joint_creation(self, s_jnt_num = 6):
        
        mc.select(cl=True)
        
        s_jnt_list = []
        s_pos = [0,0,0]
        spine_length = 25
        spine_average = (spine_length/s_jnt_num)
        
        for idx in range(s_jnt_num):
            s_idx = (idx + 1)
            spine_jnt = mc.joint(
                                 n='%s_spine_jnt_%s'%(m_rigging_window.character_lineEdit.text(),s_idx),
                                 )
            s_jnt_list.append(spine_jnt)
            print(s_jnt_list)
            
        for jnt in range(1,len(s_jnt_list)):
            mc.setAttr('%s.translateY'%(s_jnt_list[jnt]),spine_average)


    def head_joint_creation(self, n_jnt_num = 3):
          
        mc.select(cl=True)
        n_pos = [0,0,0]
        neck_average = (8/n_jnt_num)
        
        for jnt in range(n_jnt_num):
            n_idx = (jnt +1)
            neck_jnt = mc.joint(
                                n='%s_neck_jnt_%s'%(m_rigging_window.character_lineEdit.text(),n_idx),
                                p=(n_pos[0],n_pos[1],n_pos[2])
                                )
            n_pos[1] += neck_average 
            
        head_jnt = mc.joint(n='%s_head_jnt_1'%(m_rigging_window.character_lineEdit.text()))
        
        mc.move(0,8,0,head_jnt,r=True)
        mc.pickWalk(direction='up')
        
        eye_jnt = mc.joint(n='%s_eye_jnt_1'%(m_rigging_window.character_lineEdit.text()),sym=True,sa='x')  
        mc.move(2,3,4,eye_jnt,r=True)

testJoints = JointCreation()

testJoints.hand_joint_creation()
testJoints.Leg_joint_creation()
testJoints.spine_joint_creation()
testJoints.arm_joint_creation()
testJoints.head_joint_creation()
