import maya.cmds as mc
import maya.OpenMaya as om

def create_meta_ctrl(cubeScale):
    """
    Function creates custom Cube Control using one shape node.
    """
    selection_list = mc.ls(sl=True)
    
    cS=(float(cubeScale)/2)
    box = mc.curve(
                   d=1,
                   p=((cS, cS, cS), 
                   (cS, cS, -cS),
                   (cS, -cS, -cS), 
                   (cS, -cS, cS), 
                   (cS, cS, cS), 
                   (-cS, cS, cS), 
                   (-cS, -cS, cS), 
                   (cS, -cS, cS), 
                   (cS, -cS, -cS), 
                   (-cS, -cS, -cS), 
                   (-cS, cS, -cS), 
                   (cS, cS, -cS), 
                   (-cS, cS, -cS),
                   (-cS, cS, cS), 
                   (-cS, -cS, cS), 
                   (-cS, -cS, -cS)),
                   k=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
                   )
    return box


def get_metacarpal_vector_pos(root_pos, mid_pos, end_pos,v_scale):
    """
    Function Gets position for pole vector.
    """
    # Declare MVectors to variables 
    root_vector = om.MVector(root_pos[0],root_pos[1],root_pos[2])
    mid_vector = om.MVector(mid_pos[0],mid_pos[1],mid_pos[2])
    end_vector = om.MVector(end_pos[0],end_pos[1],end_pos[2])
    
    displacement = (end_vector - root_vector)
    point = (mid_vector - root_vector)    
    scale_value = (displacement * point) / ( displacement * displacement) 
    
    projected_vector = displacement * scale_value + root_vector
    
    limb_length = ((mid_vector - root_vector).length()) + ((end_vector - mid_vector).length())
    
    pole_vector_pos = (mid_vector - projected_vector).normal() * ((end_vector - mid_vector).length()*v_scale) + mid_vector
    
    return pole_vector_pos
  
  
def get_joint_pos(joint_list):
        
    vector_a_pos = mc.xform(joint_list[0],q=True,t=True,ws=True)
    vector_b_pos = mc.xform(joint_list[1],q=True,t=True,ws=True)
    vector_c_pos = mc.xform(joint_list[2],q=True,t=True,ws=True)
    
    return [vector_a_pos,vector_b_pos,vector_c_pos]


def create_locator(pos):
    """
    Function creates in locator in based on position vector.s
    """
    loc = mc.spaceLocator()
    mc.move(pos.x, pos.y, pos.z, loc)

def get_hand_joint_lists():
    root_joint = mc.ls(sl=True)
    hand_joint_list = mc.listRelatives(root_joint[0],ad=True,type='joint')
    hand_joint_list.append(root_joint[0])
    hand_joint_list.reverse()
    
    I_list = []
    II_list = []
    III_list = []
    IV_list = []
    V_list = []
    
    for jnt in hand_joint_list:
        if '_I_' in jnt:
            I_list.append(jnt)
        elif '_II_' in jnt:
            II_list.append(jnt)
        elif '_III_' in jnt:
            III_list.append(jnt)        
        elif '_IV_' in jnt:
            IV_list.append(jnt)
        elif '_V_' in jnt:
            V_list.append(jnt) 
        else:
            pass            

    return root_joint,I_list,II_list,III_list,IV_list,V_list

hand = get_hand_joint_lists()
print(hand)

def place_metacarpal_controls(hand_joints):
    
    metacarpal_pos_list = []
    
    # Get position of metacarpal joints
    for idx in xrange(len(hand_joints)-1):
        new_idx = (idx + 1)
        jnt_pos = mc.xform(hand_joints[new_idx][0],q=True,t=True,ws=True)
        metacarpal_pos_list.append(jnt_pos)   
    
    # Create control offset groups
    offset_list = []
    
    for idx in xrange(len(hand_joints)-1):
        new_idx = (idx + 1)
        joint_name = hand_joints[new_idx][0]
        offset_name = joint_name.replace('_jnt_','_offset_')
        meta_offset = mc.group(n=offset_name,em=True)
        offset_list.append(meta_offset)
           
    # Create controls metacarpal joints
    ctrl_list = []
    
    for idx in xrange(len(offset_list)):
        offset_name = offset_list[idx]
        control_name = offset_name.replace('_offset_','_ctrl_')
        meta_ctrl = create_meta_ctrl(1)
        meta_ctrl_re = mc.rename(meta_ctrl,control_name,ignoreShape=False)
        ctrl_list.append(meta_ctrl_re)
        mc.parent(meta_ctrl_re,offset_list[idx])
        
    # Orient controls to follow metalcarpals then reparent to worldspace
    for idx in xrange(len(offset_list)):
        new_idx = (idx + 1)
        
        if idx == 0:
            scale_value = (0.50)
        elif idx == 3:
            scale_value = (0.65)            
        elif idx == 4:
            scale_value = (0.80)
        else:
            scale_scale = (0.90)
                        
        print(hand_joints[new_idx][0])

        mc.parent(offset_list[idx],hand_joints[new_idx][0])          
        mc.xform(offset_list[idx],t=[0,0,0],os=True)
        mc.xform(offset_list[idx],ro=[0,0,0],os=True)
        mc.parent(offset_list[idx],w=True)
        print(hand_joints[new_idx][0]) 
               
    # Place controls at predefined position
        jnt_pos = get_joint_pos(hand_joints[new_idx])
        ctrl_pos = get_metacarpal_vector_pos(
                                             jnt_pos[0],
                                             jnt_pos[1],
                                             jnt_pos[2],
                                             scale_value
                                             )
        
        mc.move(ctrl_pos.x,ctrl_pos.y,ctrl_pos.z)
    # Place control rotation and scale pivots at metacarpal joint position
        mc.xform('%s.rotatePivot'%(offset_list[idx]),t=metacarpal_pos_list[idx],ws=True,a=True)
        mc.xform('%s.scalePivot'%(offset_list[idx]),t=metacarpal_pos_list[idx],ws=True,a=True)
        mc.xform('%s.rotatePivot'%(ctrl_list[idx]),t=metacarpal_pos_list[idx],ws=True,a=True)
        mc.xform('%s.scalePivot'%(ctrl_list[idx]),t=metacarpal_pos_list[idx],ws=True,a=True)                 
    # Orient constrain controls to metacarpal joints
        mc.orientConstraint(ctrl_list[idx],hand_joints[new_idx][0],mo=True)
    
    return ctrl_list
        
meta_ctrls = place_metacarpal_controls(hand)

def finger_controls_setup(finger_joints,meta_ctrls):

    I_list = []
    II_list = []
    III_list = []
    IV_list = []
    V_list = []

    for finger in xrange(len(finger_joints)-1):
        f_idx = (finger+1)
        print('Base Finger joint:   ',finger_joints[f_idx][1])
        for jnt in xrange(len(finger_joints[f_idx])-1):
            new_idx = (jnt+1)
            prev_idx = (new_idx-1)
           
            if new_idx == 1:
                print('Finger Segments:    ',finger_joints[f_idx][new_idx])
            elif new_idx > 1:
                print('current Segments:    ',finger_joints[f_idx][new_idx])
                cur_jnt_pos = mc.xform(finger_joints[f_idx][new_idx],q=True,t=True,ws=True)
                print('previous Segments:   ',finger_joints[f_idx][prev_idx])
                pre_jnt_pos = mc.xform(finger_joints[f_idx][prev_idx],q=True,t=True,ws=True)
                
                ##------ Vector math for placing finger joint controls ------##
                vector_a = om.MVector(cur_jnt_pos[0],cur_jnt_pos[1],cur_jnt_pos[2])
                vector_b = om.MVector(pre_jnt_pos[0],pre_jnt_pos[1],pre_jnt_pos[2])                
                mid_vector = (vector_a - vector_b) * 0.5 + vector_b
                ##----- End of Vector Math -----##
                
                mc.select(cl=True)
                
                jnt_name = finger_joints[f_idx][jnt]
                offset_name = jnt_name.replace('_jnt_','_offset_')
                ctrl_name = offset_name.replace('_offset_','_ctrl_')
                offset_grp = mc.group(n=offset_name,em=True)
                
                if '_pPhalanx_' in jnt_name:
                    finger_ctrl = mc.circle(nr=[1,0,0],r=2.0)[0]
                else:
                    finger_ctrl = mc.circle(nr=[1,0,0],r=1.65)[0]
                    
                finger_ctrl_re = mc.rename(finger_ctrl,ctrl_name)
                mc.parent(finger_ctrl_re,offset_grp)
                ctrl_cons = mc.orientConstraint(finger_joints[f_idx][prev_idx],offset_grp)
                mc.delete(ctrl_cons)
                mc.move(mid_vector.x,mid_vector.y,mid_vector.z,offset_grp)
                mc.xform('%s.rotatePivot'%(offset_grp),t=pre_jnt_pos,ws=True)
                mc.xform('%s.scalePivot'%(offset_grp),t=pre_jnt_pos,ws=True)
                mc.xform('%s.rotatePivot'%(finger_ctrl_re),t=pre_jnt_pos,ws=True)
                mc.xform('%s.scalePivot'%(finger_ctrl_re),t=pre_jnt_pos,ws=True)                

                if '_I_' in offset_grp:
                    I_list.append(offset_grp)
                elif '_II_' in offset_grp:
                    II_list.append(offset_grp)
                elif '_III_' in offset_grp:
                    III_list.append(offset_grp)        
                elif '_IV_' in offset_grp:
                    IV_list.append(offset_grp)
                elif '_V_' in offset_grp:
                    V_list.append(offset_grp) 
                else:
                    pass
                    
    return I_list,II_list,III_list,IV_list,V_list
    
finger_ctrls = finger_controls_setup(hand,meta_ctrls)


def parent_finger_controls(finger_jnts,finger_ctrls,meta_ctrls,prefix,side):
    
    mc.parentConstraint('%s_%s_wrist_jnt_01'%(prefix,side),'%s_%s_palm_jnt_01'%(prefix,side),mo=True)
    finger_ctrl_grp = mc.group(n='%s_%s_fingerControls_grp_01'%(prefix,side),em=True)
    mc.parent(finger_ctrl_grp,'%s_%s_wrist_jnt_01'%(prefix,side))
    mc.xform(finger_ctrl_grp,t=[0,0,0],os=True)
    mc.xform(finger_ctrl_grp,ro=[0,0,0],ws=True)
    mc.parent(finger_ctrl_grp,w=True)
    
    for idx in xrange(len(meta_ctrls)):
        meta_ctrl = meta_ctrls[idx]
        meta_offset = meta_ctrl.replace('_ctrl_','_offset_')
        mc.parent(meta_offset,finger_ctrl_grp)
        for jdx in xrange(len(finger_ctrls[idx])):
            prev_idx = (jdx-1)
            offset_name = finger_ctrls[idx][jdx]
            jnt_name = offset_name.replace('_offset_','_jnt_')
            ctrl_name = offset_name.replace('_offset_','_ctrl_')
            pre_ctrl = finger_ctrls[idx][prev_idx].replace('_offset_','_ctrl_')
            
            if jdx == 0:
                mc.parent(finger_ctrls[idx][0],meta_ctrls[idx])
                mc.orientConstraint(ctrl_name,jnt_name)
            elif jdx > 0:
                mc.parent(finger_ctrls[idx][jdx],pre_ctrl)
                mc.orientConstraint(ctrl_name,jnt_name)

    mc.parentConstraint('%s_%s_wrist_jnt_01'%(prefix,side),finger_ctrl_grp,mo=True)

    
parent_finger_controls(hand,finger_ctrls,meta_ctrls,'EightBall','R')
                
        

joint_pos = get_joint_pos()
ctrl_pos = get_metacarpal_vector_pos(joint_pos[0], joint_pos[1], joint_pos[2],0.65)
create_locator(ctrl_pos)
    