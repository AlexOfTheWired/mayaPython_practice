"""
Module automates the arm rigging process.
Select the root arm joint as input for build function.
"""

import maya.cmds as mc
import maya.OpenMaya as om

def create_hand_control(prefix='Test',side='L',control_scale=1.0):
    """
    Function creates a custom made curve for the hand control.
    """  
   
    curve_list = []
    first_curve = mc.curve(d=1,p=[(-2,0,0,),(0,0,-4),(2,0,0),(0,0,4),(-2,0,0)],k=[0,1,2,3,4])
    curve_list.append(first_curve)
    second_curve = mc.curve(d=1,p=[(0,-2,0,),(0,0,-4),(0,2,0),(0,0,4),(0,-2,0)],k=[0,1,2,3,4])
    curve_list.append(second_curve)
    third_curve = mc.curve(d=1,p=[(-2,0,0),(0,2,0),(2,0,0),(0,-2,0),(-2,0,0)],k=[0,1,2,3,4])
    curve_list.append(third_curve)
    
    for idx in xrange(len(curve_list)):
        c_idx = (idx+1)
        curve_re = mc.rename(curve_list[idx],'%s_%s_hand_ctrl_%s'%(prefix,side,c_idx),ignoreShape=True)
        curve_list[idx] = curve_re
    
    for idx in xrange(len(curve_list)-1):
        s_idx = (idx+1)
        shape_node = mc.listRelatives(curve_list[s_idx],s=True)
        mc.makeIdentity(curve_list[s_idx],a=True,pn=True)
        mc.DeleteHistory(curve_list[s_idx])
        mc.parent(shape_node,curve_list[0],r=True,s=True)
        mc.delete(curve_list[s_idx])
        mc.select(cl=True)
    mc.xform(curve_list[0],s=[control_scale,control_scale,control_scale])
    mc.makeIdentity(curve_list[0],a=True,pn=True)    
    return curve_list[0]


def create_arm_ik_control(prefix='Test',side='L',curve_radius=5):
    """
    Function creates a custom made curves for Ik arm control.
    """  

    first_curve = mc.circle(nr=[1,0,0],r=curve_radius)[0]
    first_curve_re = mc.rename(first_curve,'%s_%s_arm_ik_ctrl_01'%(prefix,side),ignoreShape=False)
    curve_radius = mc.circle(first_curve_re,q=True,r=True)
    second_radius = (curve_radius * 1.1) 
    second_curve = mc.circle(nr=[1,0,0],r=second_radius)[0]
    second_curve_re = mc.rename(second_curve,'%s_%s_arm_ik_ctrl_02'%(prefix,side),ignoreShape=False)
    second_curve_shape = mc.listRelatives(second_curve_re,s=True)
    
    mc.makeIdentity(second_curve_re,a=True,pn=True)
    mc.DeleteHistory(second_curve_re)
    mc.parent(second_curve_shape,first_curve_re,r=True,s=True)
    mc.delete(second_curve_re)
    mc.select(first_curve_re)
    
    return first_curve_re


def create_arm_fk_control(prefix='Test',side='L',part='shoulder',curve_radius=5):
    """
    Function creates a custom made curves for fk control.
    """  
        
    curve_list = []
        
    first_curve = mc.circle(nr=[1,0,0],r=curve_radius)[0]
    curve_list.append(first_curve)
    curve_radius = mc.circle(first_curve,q=True,r=True)
    second_radius = (curve_radius * 1.1)
    
    if part == 'shoulder': 
        second_curve = mc.circle(nr=[0,0,1],r=second_radius)[0]
        curve_list.append(second_curve)
    else:
        second_curve = mc.circle(nr=[1,0,0],r=second_radius)[0]
        curve_list.append(second_curve)
                
    third_curve = mc.circle(nr=[0,1,0],r=curve_radius)[0]
    curve_list.append(third_curve)
    fourth_curve = mc.circle(nr=[0,0,1],r=curve_radius)[0]
    curve_list.append(fourth_curve)

    for idx in xrange(len(curve_list)):        
        c_idx = (idx+1)
        curve_re = mc.rename(curve_list[idx],'%s_%s_%s_fk_ctrl_%s'%(prefix,side,part,c_idx),ignoreShape=False)
        curve_list[idx] = curve_re

    for node in xrange(len(curve_list)-1):
        s_idx = (node+1)
        shape_node = mc.listRelatives(curve_list[s_idx],s=True)     
        mc.makeIdentity(curve_list[s_idx],a=True,pn=True)
        mc.DeleteHistory(curve_list[s_idx])
        mc.parent(shape_node,curve_list[0],r=True,s=True)
        mc.delete(curve_list[s_idx])
        
    mc.select(curve_list[0])
    
    return curve_list[0]
    
    
def create_pole_vector_control(prefix,side,limb):
    """
    Function creates a custom made curve for pole vector control.
    """     
    curve_list = []
    
    first_curve = mc.curve(d=1, p=[(-0.927411,0,-0.370961),(0,0,-3),(0.962167,0,-0.26898)],k=[0,1,2])
    curve_list.append(first_curve)
    second_curve = mc.curve(d=1, p=[(0,-0.927411,-0.370961),(0,0,-3),(0,0.962167,-0.26898)],k=[0,1,2])
    curve_list.append(second_curve)
    third_curve = mc.circle(nr=[1,0,0])[0]
    curve_list.append(third_curve)
    fourth_curve = mc.circle(nr=[0,1,0])[0]
    curve_list.append(fourth_curve)
    fifth_curve = mc.circle(nr=[0,0,1])[0]
    curve_list.append(fifth_curve)
    
    mc.select(cl=True)
    
    for idx in xrange(len(curve_list)):
        curve_re = mc.rename(curve_list[idx],'%s_%s_%s_ik_ctrl_01'%(prefix,side,limb),ignoreShape=False)
        curve_list[idx] = curve_re
        
    for shape in xrange(len(curve_list)-1):
        idx = (shape+1)
        curve_list[idx]
        curve_shape = mc.listRelatives(curve_list[idx],s=True)
        mc.parent(curve_shape,curve_list[0],r=True,s=True)
        mc.delete(curve_list[idx])
    
    return curve_list[0]

def ik_handle_pole_vector_setup(prefix,side):
    """
    Function Gets position for pole vector from selected IK Handle.
    """
    selection_list = mc.ls(sl=True)
    ik_joint_list = mc.ikHandle(selection_list[0], q=True, jointList=True)
    ik_joint_list.append(mc.listRelatives(ik_joint_list[-1], children=True, type='joint')[0])

    root_jnt_pos = mc.xform(ik_joint_list[0], q=True, ws=True, t=True)
    mid_jnt_pos = mc.xform(ik_joint_list[1], q=True, ws=True, t=True)
    end_jnt_pos = mc.xform(ik_joint_list[2], q=True, ws=True, t=True)
    
    pole_vector_pos = get_pole_vector_pos(root_jnt_pos,mid_jnt_pos,end_jnt_pos)
    elbow_loc = mc.spaceLocator(n='%s_%s_elbow_ctrl_01'%(prefix,side))
    mc.move(pole_vector_pos.x,pole_vector_pos.y,pole_vector_pos.z,elbow_loc)
    
    return elbow_loc

def get_pole_vector_pos(root_pos, mid_pos, end_pos):
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
    
    pole_vector_pos = (mid_vector - projected_vector).normal() * displacement.length() + mid_vector
    
    return pole_vector_pos
    

def ik_arm_setup(prefix,side):
    '''
    Sets up the ik arm rig.
    Returns two lists: [Bind arm joint],[Ik arm joints]
    '''
    
    selection_list = mc.ls(sl=True)
        
    arm_joint_list = mc.listRelatives(selection_list[0],ad=True,type='joint')
    arm_joint_list.append(selection_list[0])
    arm_joint_list.reverse()
    ik_arm_joint_list = mc.duplicate(arm_joint_list,rc=True)
        
    for idx in xrange(len(ik_arm_joint_list)):
        ik_node_name = ik_arm_joint_list[idx].replace('_jnt_02','_IK_jnt_01') 
        mc.rename(ik_arm_joint_list[idx],ik_node_name)
        ik_arm_joint_list[idx] = ik_node_name
    
    # Create empty group for ik arm joints
    ik_arm_group = mc.group(n='%s_%s_ik_arm_grp_01'%(prefix,side),em=True)
    mc.parent(ik_arm_group,ik_arm_joint_list[0])
    mc.xform(ik_arm_group,t=[0,0,0],os=True)
    mc.xform(ik_arm_group,ro=[0,0,0],os=True)
    mc.parent(ik_arm_group,w=True)
    mc.parent(ik_arm_joint_list[0],ik_arm_group)
    
    # create ik solvers for arm
    arm_ik_handle = mc.ikHandle(
                                n='%s_%s_arm_ikHandle_01'%(prefix, side),
                                sj=ik_arm_joint_list[0],
                                ee=ik_arm_joint_list[2],
                                sol='ikRPsolver'
                                )[0]
                                

    mc.select(arm_ik_handle)
    ik_elbow_loc = ik_handle_pole_vector_setup(prefix,side)
    mc.CenterPivot(ik_elbow_loc)
    mc.makeIdentity(ik_elbow_loc,a=True,pn=True)
    mc.poleVectorConstraint(ik_elbow_loc,arm_ik_handle)                                
    elbow_controller = create_pole_vector_control(prefix,side,limb='elbow')
    mc.xform(elbow_controller,s=[1,1,-1],ws=True)
    mc.pointConstraint(ik_elbow_loc,elbow_controller)
    mc.pointConstraint(ik_elbow_loc,elbow_controller,rm=True)
    mc.makeIdentity(elbow_controller,a=True,pn=True)
    mc.parent(ik_elbow_loc,elbow_controller)
    
    arm_ik_controller = create_arm_ik_control(prefix,side,curve_radius=5) 
    mc.parentConstraint(ik_arm_joint_list[2],arm_ik_controller)
    mc.parentConstraint(ik_arm_joint_list[2],arm_ik_controller,e=True,rm=True)
    mc.makeIdentity(arm_ik_controller,a=True,pn=True)
    mc.parent(arm_ik_handle,arm_ik_controller)
    mc.pointConstraint(arm_ik_controller,elbow_controller,mo=True)
    mc.orientConstraint(arm_ik_controller,ik_arm_joint_list[2],mo=True)
            
    return selection_list,ik_arm_joint_list

    
def fk_arm_setup(prefix,side,root_jnt):
    '''
    Sets up the Fk arm rig
    Returns a list of Fk joints
    '''
        
    arm_joint_list = mc.listRelatives(root_jnt[0],ad=True,type='joint')
    arm_joint_list.append(root_jnt[0])
    arm_joint_list.reverse()
    fk_arm_joint_list = mc.duplicate(arm_joint_list,rc=True)
        
    for idx in xrange(len(fk_arm_joint_list)):
        fk_node_name = fk_arm_joint_list[idx].replace('_jnt_02','_FK_jnt_01') 
        mc.rename(fk_arm_joint_list[idx],fk_node_name)
        fk_arm_joint_list[idx] = fk_node_name
    print('FK JOINT LIST:',fk_arm_joint_list)

    # Create empty group for ik arm joints
    fk_arm_group = mc.group(n='%s_%s_fk_arm_grp_01'%(prefix,side),em=True)
    mc.parent(fk_arm_group,fk_arm_joint_list[0])
    mc.xform(fk_arm_group,t=[0,0,0],os=True)
    mc.xform(fk_arm_group,ro=[0,0,0],os=True)
    mc.parent(fk_arm_group,w=True)
    mc.parent(fk_arm_joint_list[0],fk_arm_group)

    # Create shoulder controller
    shoulder_offset = mc.group(n='%s_%s_shoulder_offset_01'%(prefix,side),em=True)
    shoulder_ctrl = create_arm_fk_control(prefix,side,'shoulder',10)
    mc.parent(shoulder_ctrl,shoulder_offset)
    mc.parent(shoulder_offset,fk_arm_joint_list[0])
    mc.xform(shoulder_offset,t=[0,0,0],os=True)
    mc.xform(shoulder_offset,ro=[0,0,0],os=True)
    mc.parent(shoulder_offset,w=True)
    
    # Create elbow controller
    elbow_offset = mc.group(n='%s_%s_elbow_offset_01'%(prefix,side),em=True)
    elbow_ctrl = create_arm_fk_control(prefix,side,'elbow',8)
    mc.parent(elbow_ctrl,elbow_offset)
    mc.parent(elbow_offset,fk_arm_joint_list[1])
    mc.xform(elbow_offset,t=[0,0,0],os=True)
    mc.xform(elbow_offset,ro=[0,0,0],os=True)
    mc.parent(elbow_offset,shoulder_ctrl)
    
    # Create wrist controller
    wrist_offset = mc.group(n='%s_%s_wrist_offset_01'%(prefix,side),em=True)
    wrist_ctrl = create_arm_fk_control(prefix,side,'wrist',6)
    mc.parent(wrist_ctrl,wrist_offset)
    mc.parent(wrist_offset,fk_arm_joint_list[2])
    mc.xform(wrist_offset,t=[0,0,0],os=True)
    mc.xform(wrist_offset,ro=[0,0,0],os=True)
    mc.parent(wrist_offset,elbow_ctrl)
    
    # Constarin FK arm joints to FK controls
    mc.orientConstraint(shoulder_ctrl,fk_arm_joint_list[0],mo=True)
    mc.orientConstraint(elbow_ctrl,fk_arm_joint_list[1],mo=True)
    mc.orientConstraint(wrist_ctrl,fk_arm_joint_list[2],mo=True) 

    return fk_arm_joint_list
    
def twist_joint_setup(root_joint=mc.ls(sl=True),prefix='Test', side='L',limb='Arm', upperTwistNum=4, lowerTwistNum=3):
    '''
    Creates properly placed twist joints for a twist dispersion arm rig.
    '''
    if len(root_joint) < 1:
        mc.error('Select ONE Joint!!!!')
        
    else:
        pass
        
    # Generate joint list with descendent joint nodes
    arm_joint_list = mc.listRelatives(root_joint[0],ad=True,type='joint')
    arm_joint_list.append(root_joint[0])
    arm_joint_list.reverse()
    # Create empty list for upper twist joints.
    upper_twist_list = []
    # Create empty list for lower twist joints.
    lower_twist_list = []

        
    root_joint_pos =mc.xform(arm_joint_list[0],q=True,t=True,ws=True,a=True)
    root_joint_rot =mc.xform(arm_joint_list[0],q=True,ro=True,ws=True,a=True)
    # Create twist joints group
    twist_joints_group = mc.createNode('transform',n='%s_%s_twistJoint_grp_01'%(prefix,side))
    mc.xform(twist_joints_group,t=root_joint_pos,ro=root_joint_rot,ws=True,a=True)
    # Clear active selection.
    mc.select(cl=True)    
    # Get distance from Shoulder/Hip to Elbow/Knee joints.
    upper_length = mc.getAttr('%s.translateX'%(arm_joint_list[1]))    
    # Divide upperArmDistance by upperArmTwistJoint number.
    upper_length_average = ((upper_length) / upperTwistNum)   
    # Add Shoulder/Hip joint to active selection list.
    mc.select(arm_joint_list[0],tgl=True)
    
    # Use for Loop
    for idx in range(upperTwistNum):
        u_idx    = (idx + 1)       
        # Create distributed twist joint for upper arm.
        twist_joint  = mc.joint(n='%s_%s_upper%sTwist_jnt_0%s'%(prefix, side, limb, u_idx))
        joint_orient = mc.joint(twist_joint, query=True, o=True)
        joint_pos    = mc.xform(twist_joint, query=True, t=True, ws=True, a=True)
        mc.select(cl=True)
        upper_twist_list.append(twist_joint)
        mc.select(twist_joint)
        
    for jnt in range(len(upper_twist_list)-1):
        # Set new idx to begin operating on second element in upper_twist_list
        new_idx = (jnt + 1)
        # Set twist joint to length average.
        mc.setAttr('%s.translateX'%(upper_twist_list[new_idx]),upper_length_average)
    
    # replace first joint with second joint in active selection.
    mc.select(arm_joint_list[1])    
    # Get distance from Elbow/Knee to Wrist/Ankle joints.
    lower_length = mc.getAttr('%s.translateX'%(arm_joint_list[2]))
    # Divide lowerArmDistance by lowerArmTwistJoint number.
    lower_length_average = ((lower_length) / lowerTwistNum)

    for idx in range(lowerTwistNum):
        l_idx = (idx + 1)       
        # Create distributed twist joint for lower twist joints.
        twist_joint = mc.joint(n='%s_%s_lower%sTwist_jnt_0%s'%(prefix, side, limb, l_idx))
        # Add upperArmTwistJoints to a list.
        lower_twist_list.append(twist_joint)
        print(lower_twist_list)
    
    for jnt in range(len(lower_twist_list)-1):
        # Set new idx to begin operating on second element in lower_twist_list
        new_idx = (jnt + 1)
        # Set twist joint to length average.
        mc.setAttr('%s.translateX'%(lower_twist_list[new_idx]),lower_length_average)
    
    wrist_length = mc.getAttr('%s.translateX'%(arm_joint_list[-1]))

    mc.select(arm_joint_list[2])
    wrist_joint = mc.joint(n='%s_%s_twist_wrist_jnt_01'%(prefix, side))
    lower_twist_list.append(wrist_joint)
    wrist_end_joint = mc.joint(n='%s_%s_twist_wristEnd_jnt_01'%(prefix, side))
    lower_twist_list.append(wrist_end_joint)
    mc.setAttr('%s.translateX'%(wrist_end_joint),wrist_length)
    mc.select(cl=True)
    mc.parent([upper_twist_list[0],lower_twist_list[0],wrist_joint],w=True)
    print(lower_twist_list)
    mc.parent(wrist_joint, lower_twist_list[-3])
    mc.parent(lower_twist_list[0], upper_twist_list[-1])
    mc.parent(upper_twist_list[0],twist_joints_group)
    
    return upper_twist_list,lower_twist_list
    
def setup_fk_ik_blend(prefix,side,fk_arm,ik_arm,bind_arm,ctrl_scale):
    '''
    Sets up the blending between Ik and Fk rigs
    '''
    arm_joint_list = mc.listRelatives(bind_arm[0],ad=True,type='joint')
    arm_joint_list.append(bind_arm[0])
    arm_joint_list.reverse()
            
    # OrientConstraint FK and IK arms to the Bind arm joints
    shoulder_constraint = mc.orientConstraint(fk_arm[0],ik_arm[0],arm_joint_list[0])[0]
    elbow_constraint = mc.orientConstraint(fk_arm[1],ik_arm[1],arm_joint_list[1])[0]
    wrist_constraint = mc.orientConstraint(fk_arm[2],ik_arm[2],arm_joint_list[2])[0]
    
    # Create and place hand controller
    hand_offset = mc.group(n='%s_%s_hand_offset_01'%(prefix,side),em=True)
    hand_ctrl = create_hand_control(prefix,side,ctrl_scale)
    mc.parent(hand_ctrl,hand_offset)
    mc.parent(hand_offset,fk_arm[-1])
    mc.xform(hand_offset,t=[0,0,0],os=True,wd=True)
    
    if side == 'L':
        mc.xform(hand_offset,ro=[90,0,0],os=True)
        mc.setAttr('%s.ty'%(hand_offset),(15*ctrl_scale))
    else:
        mc.setAttr('%s.ty'%(hand_offset),(-15*ctrl_scale))
        mc.xform(hand_offset,ro=[90,0,0],os=True)
        
    mc.parent(hand_offset,w=True)
    mc.parentConstraint(arm_joint_list[2],hand_offset,mo=True)
    mc.select(hand_ctrl)
    
    # Add FK IK Blend attribute
    mc.addAttr(ln='FK_IK_Blend',dv=0,min=0,max=10,at='double',k=True)
    
    # Lock and Hide uneeded channels so ANIMATORS DONT BREAK MY RIG!!!!!
    
    # FK IK SDK's
    # Set shoulder blend
    mc.setAttr('%s.FK_IK_Blend'%(hand_ctrl),10)
    mc.setAttr('%s.%sW0'%(shoulder_constraint,fk_arm[0]),0)
    mc.setAttr('%s.%sW1'%(shoulder_constraint,ik_arm[0]),1)       
    mc.setDrivenKeyframe('%s.%sW0'%(shoulder_constraint,fk_arm[0]),cd='%s.FK_IK_Blend'%(hand_ctrl))
    mc.setDrivenKeyframe('%s.%sW1'%(shoulder_constraint,ik_arm[0]),cd='%s.FK_IK_Blend'%(hand_ctrl))

    mc.setAttr('%s.FK_IK_Blend'%(hand_ctrl),0)
    mc.setAttr('%s.%sW0'%(shoulder_constraint,fk_arm[0]),1)
    mc.setAttr('%s.%sW1'%(shoulder_constraint,ik_arm[0]),0)       
    mc.setDrivenKeyframe('%s.%sW0'%(shoulder_constraint,fk_arm[0]),cd='%s.FK_IK_Blend'%(hand_ctrl))
    mc.setDrivenKeyframe('%s.%sW1'%(shoulder_constraint,ik_arm[0]),cd='%s.FK_IK_Blend'%(hand_ctrl))
    
    # Set elbow blend
    mc.setAttr('%s.FK_IK_Blend'%(hand_ctrl),10)
    mc.setAttr('%s.%sW0'%(elbow_constraint,fk_arm[1]),0)
    mc.setAttr('%s.%sW1'%(elbow_constraint,ik_arm[1]),1)       
    mc.setDrivenKeyframe('%s.%sW0'%(elbow_constraint,fk_arm[1]),cd='%s.FK_IK_Blend'%(hand_ctrl))
    mc.setDrivenKeyframe('%s.%sW1'%(elbow_constraint,ik_arm[1]),cd='%s.FK_IK_Blend'%(hand_ctrl))

    mc.setAttr('%s.FK_IK_Blend'%(hand_ctrl),0)
    mc.setAttr('%s.%sW0'%(elbow_constraint,fk_arm[1]),1)
    mc.setAttr('%s.%sW1'%(elbow_constraint,ik_arm[1]),0)       
    mc.setDrivenKeyframe('%s.%sW0'%(elbow_constraint,fk_arm[1]),cd='%s.FK_IK_Blend'%(hand_ctrl))
    mc.setDrivenKeyframe('%s.%sW1'%(elbow_constraint,ik_arm[1]),cd='%s.FK_IK_Blend'%(hand_ctrl))

    # Set wrist blend
    mc.setAttr('%s.FK_IK_Blend'%(hand_ctrl),10)
    mc.setAttr('%s.%sW0'%(wrist_constraint,fk_arm[2]),0)
    mc.setAttr('%s.%sW1'%(wrist_constraint,ik_arm[2]),1)       
    mc.setDrivenKeyframe('%s.%sW0'%(wrist_constraint,fk_arm[2]),cd='%s.FK_IK_Blend'%(hand_ctrl))
    mc.setDrivenKeyframe('%s.%sW1'%(wrist_constraint,ik_arm[2]),cd='%s.FK_IK_Blend'%(hand_ctrl))

    mc.setAttr('%s.FK_IK_Blend'%(hand_ctrl),0)
    mc.setAttr('%s.%sW0'%(wrist_constraint,fk_arm[2]),1)
    mc.setAttr('%s.%sW1'%(wrist_constraint,ik_arm[2]),0)       
    mc.setDrivenKeyframe('%s.%sW0'%(wrist_constraint,fk_arm[2]),cd='%s.FK_IK_Blend'%(hand_ctrl))
    mc.setDrivenKeyframe('%s.%sW1'%(wrist_constraint,ik_arm[2]),cd='%s.FK_IK_Blend'%(hand_ctrl))

    # Set arm controls visibility SDK's
    # FK STATE ON
    mc.setAttr('%s.FK_IK_Blend'%(hand_ctrl),0)
    mc.setAttr('%s_%s_shoulder_fk_ctrl_1.v'%(prefix,side),1)
    mc.setDrivenKeyframe('%s_%s_shoulder_fk_ctrl_1.v'%(prefix,side),cd='%s.FK_IK_Blend'%(hand_ctrl))    
    mc.setAttr('%s_%s_elbow_fk_ctrl_1.v'%(prefix,side),1)
    mc.setDrivenKeyframe('%s_%s_elbow_fk_ctrl_1.v'%(prefix,side),cd='%s.FK_IK_Blend'%(hand_ctrl)) 
    mc.setAttr('%s_%s_wrist_fk_ctrl_1.v'%(prefix,side),1)
    mc.setDrivenKeyframe('%s_%s_wrist_fk_ctrl_1.v'%(prefix,side),cd='%s.FK_IK_Blend'%(hand_ctrl))     
    mc.setAttr('%s_%s_arm_ik_ctrl_01.v'%(prefix,side),0)
    mc.setDrivenKeyframe('%s_%s_arm_ik_ctrl_01.v'%(prefix,side),cd='%s.FK_IK_Blend'%(hand_ctrl))
    mc.setAttr('%s_%s_elbow_ctrl_01.v'%(prefix,side),0)
    mc.setDrivenKeyframe('%s_%s_elbow_ctrl_01.v'%(prefix,side),cd='%s.FK_IK_Blend'%(hand_ctrl))
    
    # IK STATE ON
    mc.setAttr('%s.FK_IK_Blend'%(hand_ctrl),10)
    mc.setAttr('%s_%s_shoulder_fk_ctrl_1.v'%(prefix,side),0)
    mc.setDrivenKeyframe('%s_%s_shoulder_fk_ctrl_1.v'%(prefix,side),cd='%s.FK_IK_Blend'%(hand_ctrl))    
    mc.setAttr('%s_%s_elbow_fk_ctrl_1.v'%(prefix,side),0)
    mc.setDrivenKeyframe('%s_%s_elbow_fk_ctrl_1.v'%(prefix,side),cd='%s.FK_IK_Blend'%(hand_ctrl)) 
    mc.setAttr('%s_%s_wrist_fk_ctrl_1.v'%(prefix,side),0)
    mc.setDrivenKeyframe('%s_%s_wrist_fk_ctrl_1.v'%(prefix,side),cd='%s.FK_IK_Blend'%(hand_ctrl))     
    mc.setAttr('%s_%s_arm_ik_ctrl_01.v'%(prefix,side),1)
    mc.setDrivenKeyframe('%s_%s_arm_ik_ctrl_01.v'%(prefix,side),cd='%s.FK_IK_Blend'%(hand_ctrl))
    mc.setAttr('%s_%s_elbow_ctrl_01.v'%(prefix,side),1)
    mc.setDrivenKeyframe('%s_%s_elbow_ctrl_01.v'%(prefix,side),cd='%s.FK_IK_Blend'%(hand_ctrl))    

   # Lock and Hide T, R, and S Attributes.
    lock_channels = ['t','r','s']
    lock_attr = ['x','y','z']
    for ch in lock_channels:
        for attr in lock_attr:
            mc.setAttr('%s.%s%s'%(hand_ctrl,ch,attr),l=True,k=False)
    mc.setAttr('%s.v'%(hand_ctrl),l=True,k=False)
    

def setup_twist_dispersion(input_joints,twist_joints,prefix,side,limb):
    '''
    Connects joint rotation values to twist Node to extract and apply twist values 
    for proper twist dispersion.
    '''
    print('INPUT JOINTS:' ,input_joints)
    print('Twist Joints:', twist_joints)
    arm_joint_list = mc.listRelatives(input_joints[0],ad=True,type='joint')
    arm_joint_list.append(input_joints[0])
    arm_joint_list.reverse()
    
    node_list = []    
        

    Lower_twist_node = mc.createNode('multiplyDivide',n='%s_%s_%sLower_twistNode_01'%(prefix,side,limb))
    upper_twist_list = twist_joints[0]
    lower_twist_list = twist_joints[1]
    upper_twist_num = len(upper_twist_list)
    lower_twist_num = len(lower_twist_list)
        
    # Connect distributed twist joints to twist node
    upper_twist_node = mc.createNode('multiplyDivide',n='%s_%s_%sUpper_twistNode_01'%(prefix,side,limb))
    mc.setAttr('%s.operation'%(upper_twist_node), 2)
    mc.connectAttr('%s.rotateX'%(arm_joint_list[0]),'%s.input1X'%(upper_twist_node))
    mc.connectAttr('%s.rotateX'%(arm_joint_list[0]),'%s.input1Y'%(upper_twist_node))
    mc.setAttr('%s.input2X'%(upper_twist_node),-1)
    mc.setAttr('%s.input2Y'%(upper_twist_node),upper_twist_num)
    
    mc.connectAttr('%s.outputX'%(upper_twist_node),'%s.rotateX'%(upper_twist_list[0]))
    
    for jnt in xrange((upper_twist_num)-1):
        mc.connectAttr('%s.outputY'%(upper_twist_node),'%s.rotateX'%(upper_twist_list[jnt+1]))
        
    lower_twist_node = mc.createNode('multiplyDivide',n='%s_%s_lower%s_twist_01'%(prefix,side,limb))
    mc.setAttr('%s.operation'%(lower_twist_node), 2)
    mc.connectAttr('%s.rotateX'%(arm_joint_list[2]),'%s.input1X'%(lower_twist_node))
    mc.connectAttr('%s.rotateX'%(arm_joint_list[2]),'%s.input1Y'%(lower_twist_node))
    mc.setAttr('%s.input2X'%(lower_twist_node),-1)
    mc.setAttr('%s.input2Y'%(lower_twist_node),lower_twist_num)
    
    mc.connectAttr('%s.outputX'%(lower_twist_node),'%s.rotateX'%(lower_twist_list[0]))
    
    for jnt in xrange((lower_twist_num)-1):
        mc.connectAttr('%s.outputY'%(lower_twist_node),'%s.rotateX'%(lower_twist_list[jnt+1]))       

    # Orient Constaint input joints to twist joints
    shoulder_constraint = mc.orientConstraint(arm_joint_list[0],twist_joints[0][0])[0]
    elbow_constraint = mc.orientConstraint(arm_joint_list[1],twist_joints[1][0])[0]
    wrist_constraint = mc.orientConstraint(arm_joint_list[2],twist_joints[1][-2])[0]


def connect_arm_rig(bind_arm,fk_arm,ik_arm,twist_arm,prefix,side):
        
    clavicle_jnt = '%s_%s_clavicleEnd_jnt_01'%(prefix,side)
    hierachy_jnt_group = '%s_joints_grp_01'%(prefix)
    hierachy_ctrl_group = '%s_controls_grp_01'%(prefix)
    fk_ctrl_grp = '%s_%s_shoulder_offset_01'%(prefix,side)
    ik_elbow_ctrl = '%s_%s_elbow_ik_ctrl_01'%(prefix,side)
    ik_arm_ctrl = '%s_%s_arm_ik_ctrl_01'%(prefix,side)
    hand_ctrl = '%s_%s_hand_offset_01'%(prefix,side)
    
        
    mc.select(fk_arm[0])
    fk_group = mc.pickWalk(d='up')
    mc.parent(fk_group,hierachy_jnt_group)

    mc.select(ik_arm[0])
    ik_group = mc.pickWalk(d='up')
    mc.parent(ik_group,hierachy_jnt_group)
    
    mc.select(twist_arm[0][0])
    twist_group = mc.pickWalk(d='up')
    mc.parent(twist_group,hierachy_jnt_group)
    
    mc.parent(fk_ctrl_grp,hierachy_ctrl_group)
    mc.parent(ik_elbow_ctrl,hierachy_ctrl_group)    
    mc.parent(ik_arm_ctrl,hierachy_ctrl_group)
    mc.parent(hand_ctrl,hierachy_ctrl_group)    
    
    mc.pointConstraint(clavicle_jnt, bind_arm)
    mc.pointConstraint(clavicle_jnt,fk_group)
    mc.pointConstraint(clavicle_jnt,ik_group)
    mc.pointConstraint(clavicle_jnt,twist_group)
    mc.pointConstraint(clavicle_jnt,fk_ctrl_grp)

        
def build_arm_rig(prefix='Test',side='L',twist=True,rig_scale=1.0):
    
    if twist == True:
        ik_arm_rig = ik_arm_setup(prefix,side)
        fk_arm_rig = fk_arm_setup(prefix,side,root_jnt=ik_arm_rig[0])
        twist_arm = twist_joint_setup(ik_arm_rig[0],prefix,side,'Arm',4,3)
        setup_fk_ik_blend(prefix,side,fk_arm_rig,ik_arm_rig[1],ik_arm_rig,rig_scale)
        setup_twist_dispersion(ik_arm_rig[0],twist_arm,prefix,side,'arm')
        connect_arm_rig(ik_arm_rig[0],fk_arm_rig,ik_arm_rig[1],twist_arm,prefix,side)
    else:
        ik_arm_rig = ik_arm_setup(prefix,side)
        fk_arm_rig = fk_arm_setup(prefix,side,root_jnt=ik_arm_rig[0])
        setup_fk_ik_blend(prefix,side,fk_arm_rig,ik_arm_rig[1],ik_arm_rig,rig_scale)
