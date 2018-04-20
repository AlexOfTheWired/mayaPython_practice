import maya.cmds as mc

def hand_joint_creation(f_num=5-1, f_jnt_num=4):
    mc.select(clear=True)
    
    base_joint = mc.joint(name='wrist',p=(0,0,0,))
    
    finger_spacing = 2
    palm_length = 4
    joint_length = 2
    
    for i in range(f_num):
        mc.select(base_joint, replace=True)
        pos = [0, palm_length, 0]
        
        pos[0] = (i * finger_spacing) - ((f_num-1)* finger_spacing) / 2
        
        mc.joint(p= pos)
        
        for j in range(f_num):
            mc.joint(relative=True, p=(0,joint_length,0))
            
        mc.select(base_joint,replace=True)

hand_joint_creation(f_num=5-1, f_jnt_num=4)