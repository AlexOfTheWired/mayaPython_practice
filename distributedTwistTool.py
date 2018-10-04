import maya.cmds as mc

def distributedTwistJointSetup(prefix='Test', side='L',limb='Arm', upperTwistNum=4, lowerTwistNum=3):

    # Assign variable for Active Selection List
    selection_list = mc.ls(sl=True)
    # Create empty list for upper twist joints.
    upper_twist_list = []
    # Create empty list for lower twist joints.
    lower_twist_list = []

    
    if len(selection_list) >= 4:
        pass
        
    else:
        mc.error('Select at least 4 joints!!!!') 
        
    root_joint_pos =mc.xform(selection_list[0],q=True,t=True,ws=True,a=True)
    root_joint_rot =mc.xform(selection_list[0],q=True,ro=True,ws=True,a=True)
    # Create twist joints group
    twist_joints_group = mc.createNode('transform',n='%s_%s_twistJoint_grp_01'%(prefix,side))
    mc.xform(twist_joints_group,t=root_joint_pos,ro=root_joint_rot,ws=True,a=True)
    # Clear active selection.
    mc.select(cl=True)    
    # Get distance from Shoulder/Hip to Elbow/Knee joints.
    upper_length = mc.getAttr('%s.translateX'%(selection_list[1]))    
    # Divide upperArmDistance by upperArmTwistJoint number.
    upper_length_average = ((upper_length) / upperTwistNum)   
    # Add Shoulder/Hip joint to active selection list.
    mc.select(selection_list[0],tgl=True)
    
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
    mc.select(selection_list[1])    
    # Get distance from Elbow/Knee to Wrist/Ankle joints.
    lower_length = mc.getAttr('%s.translateX'%(selection_list[2]))
    # Divide lowerArmDistance by lowerArmTwistJoint number.
    lower_length_average = ((lower_length) / lowerTwistNum)

    for idx in range(lowerTwistNum):
        l_idx = (idx + 1)       
        # Create distributed twist joint for lower twist joints.
        twist_joint = mc.joint(n='%s_%s_lower%sTwist_jnt_0%s'%(prefix, side, limb, l_idx))
        # Add upperArmTwistJoints to a list.
        lower_twist_list.append(twist_joint)
    
    for jnt in range(len(lower_twist_list)-1):
        # Set new idx to begin operating on second element in lower_twist_list
        new_idx = (jnt + 1)
        # Set twist joint to length average.
        mc.setAttr('%s.translateX'%(lower_twist_list[new_idx]),lower_length_average)
        
    wrist_length = mc.getAttr('%s.translateX'%(selection_list[-1]))

    mc.select(selection_list[2])
    wrist_joint = mc.joint(n='%s_%s_wrist_jnt_01'%(prefix, side))
    wrist_end_joint = mc.joint(n='%s_%s_wristEnd_jnt_01'%(prefix, side))
    mc.setAttr('%s.translateX'%(wrist_end_joint),wrist_length)
    
    mc.parent([upper_twist_list[0],lower_twist_list[0],wrist_joint],w=True)
    mc.parent(wrist_joint, lower_twist_list[-1])
    mc.parent(lower_twist_list[0], upper_twist_list[-1])
    mc.parent(upper_twist_list[0],twist_joints_group)
    
    # Connect distributed twist joints to twist node
    upper_twist_node = mc.createNode('multiplyDivide',n='%s_%s_upper%s_twist_01'%(prefix,side,limb))
    mc.setAttr('%s.operation'%(upper_twist_node), 2)
    mc.connectAttr('%s.rotateX'%(selection_list[0]),'%s.input1X'%(upper_twist_node))
    mc.connectAttr('%s.rotateX'%(selection_list[0]),'%s.input1Y'%(upper_twist_node))
    mc.setAttr('%s.input2X'%(upper_twist_node),-1)
    mc.setAttr('%s.input2Y'%(upper_twist_node),upperTwistNum)
    
    mc.connectAttr('%s.outputX'%(upper_twist_node),'%s.rotateX'%(upper_twist_list[0]))
    
    for jnt in xrange((upperTwistNum)-1):
        mc.connectAttr('%s.outputY'%(upper_twist_node),'%s.rotateX'%(upper_twist_list[jnt+1]))
        
    lower_twist_node = mc.createNode('multiplyDivide',n='%s_%s_lower%s_twist_01'%(prefix,side,limb))
    mc.setAttr('%s.operation'%(lower_twist_node), 2)
    mc.connectAttr('%s.rotateX'%(selection_list[2]),'%s.input1X'%(lower_twist_node))
    mc.connectAttr('%s.rotateX'%(selection_list[2]),'%s.input1Y'%(lower_twist_node))
    mc.setAttr('%s.input2X'%(lower_twist_node),-1)
    mc.setAttr('%s.input2Y'%(lower_twist_node),lowerTwistNum)
    
    mc.connectAttr('%s.outputX'%(lower_twist_node),'%s.rotateX'%(lower_twist_list[0]))
    
    for jnt in xrange((lowerTwistNum)-1):
        mc.connectAttr('%s.outputY'%(lower_twist_node),'%s.rotateX'%(lower_twist_list[jnt+1]))


twist_joints = distributedTwistJointSetup(prefix='Batman', side='L', limb='Arm', upperTwistNum=6, lowerTwistNum=5)


