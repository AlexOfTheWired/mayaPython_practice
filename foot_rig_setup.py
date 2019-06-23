import maya.cmds as mc
import maya.OpenMaya as om


def create_locator(pos):
    """
    Function creates in locator in based on position vector.
    """
    loc = mc.spaceLocator()
    mc.move(pos.x, pos.y, pos.z, loc)


def create_foot_ctrl(prefix='Test',side='L'):
    """
    Function creates custom foot control.
    """
    foot_curve = mc.curve(
                       d=3,
                       p=[
                       (-8.552326,0,0.111295),
                       (-8.619388,0,-1.533448),
                       (-8.753511,0,-4.822935),
                       (-9.236188,0,-9.796975),
                       (-6.189172,2.5,-18.188805),
                       (0.7179,2.5,-19.008913),
                       (5.649882,0,-13.83864),
                       (6.558787,0,-10.364002),
                       (8.026455,0,-4.841455),
                       (8.702795,0,0.0955905),
                       (8.724709,0,5.105386),
                       (9.352438,0,10.12076),
                       (7.35878,0,14.840333),
                       (5.50197,0,17.193196),
                       (-1.085671,0,18.964254),
                       (-6.278294,0,14.726305),
                       (-8.53845,0,10.065057),
                       (-8.203282,0,4.876221),
                       (-8.435978,0,1.699604),
                       (-8.552326,0,0.111295)
                       ],
                       k=[0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,17,17])

    foot_curve_re = mc.rename(foot_curve,'%s_%s_foot_ctrl_01'%(prefix,side))    
    foot_curve_dup = mc.duplicate(foot_curve_re)
    foot_curve_dup_shape = mc.listRelatives(foot_curve_dup,s=True)
    
    mc.xform(foot_curve_dup,s=[1.05,1.05,1.05],ws=True)
    mc.makeIdentity(foot_curve_dup,a=True)
    mc.DeleteHistory(foot_curve_dup)
    mc.parent(foot_curve_dup_shape,foot_curve_re,s=True,r=True)
    mc.delete(foot_curve_dup)
    mc.select(foot_curve_re)
                   
    if side == 'L':
        mc.xform(foot_curve_re,s=[1,1,1],ws=True)
        
    else:
        mc.xform(foot_curve_re,s=[-1,1,1],ws=True)

    return foot_curve_re 


def create_pole_vector_control(prefix='Test',side='L',limb='knee'):
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
    
    print(curve_list)
    
    mc.select(cl=True)
    
    for idx in xrange(len(curve_list)):
        curve_re = mc.rename(curve_list[idx],'%s_%s_%s_ctrl_01'%(prefix,side,limb),ignoreShape=False)
        curve_list[idx] = curve_re
        
    for shape in xrange(len(curve_list)-1):
        idx = (shape+1)
        curve_list[idx]
        curve_shape = mc.listRelatives(curve_list[idx],s=True)
        mc.parent(curve_shape,curve_list[0],r=True,s=True)
        mc.delete(curve_list[idx])
    
    return curve_list[0]


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
 
   
def ik_handle_pole_vector_setup(prefix='Test',side='L'):
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
    knee_loc = mc.spaceLocator(n='%s_%s_knee_ctrl_01'%(prefix,side))
    mc.move(pole_vector_pos.x,pole_vector_pos.y,pole_vector_pos.z,knee_loc)
    
    return knee_loc

    
def ik_leg_setup(prefix='Test',side='L'):
    """
    Function sets up Leg for IK Rig.
    """    
    selection_list = mc.ls(sl=True)
    foot_joint = selection_list[1]
        
    leg_joint_list = mc.listRelatives(selection_list[0],ad=True,type='joint')
    leg_joint_list.append(selection_list[0])
    leg_joint_list.reverse()
    ik_leg_joint_list = mc.duplicate(leg_joint_list,rc=True)
        
    for idx in xrange(len(ik_leg_joint_list)):
        ik_node_name = ik_leg_joint_list[idx].replace('_jnt_02','_IK_jnt_01') 
        mc.rename(ik_leg_joint_list[idx],ik_node_name)
        ik_leg_joint_list[idx] = ik_node_name
    
    # create ik solvers for leg
    leg_ik_handle = mc.ikHandle(
                                n='%s_%s_leg_ikHandle_01'%(prefix, side),
                                sj=ik_leg_joint_list[0],
                                ee=ik_leg_joint_list[2],
                                sol='ikRPsolver'
                                )[0]
                                
    ball_ik_handle = mc.ikHandle(
                                n='%s_%s_ball_ikHandle_01'%(prefix, side),
                                sj=ik_leg_joint_list[2],
                                ee=ik_leg_joint_list[3],
                                sol='ikSCsolver'
                                )[0]
    
    toe_ik_handle = mc.ikHandle(
                                n='%s_%s_toe_ikHandle_01'%(prefix, side),
                                sj=ik_leg_joint_list[3],
                                ee=ik_leg_joint_list[-1],
                                sol='ikSCsolver'
                                )[0]

    mc.select(leg_ik_handle)
    ik_knee_loc = ik_handle_pole_vector_setup(prefix,side)
    mc.CenterPivot(ik_knee_loc)
    mc.makeIdentity(ik_knee_loc,a=True,pn=True)
    mc.poleVectorConstraint(ik_knee_loc,leg_ik_handle)
    knee_controller = create_pole_vector_control(prefix,side,limb='knee')
    mc.pointConstraint(ik_knee_loc,knee_controller)
    mc.pointConstraint(ik_knee_loc,knee_controller,rm=True)
    mc.makeIdentity(knee_controller,a=True,pn=True)
    mc.parent(ik_knee_loc,knee_controller)
    
    return [selection_list, knee_controller]

#L_leg_ik = ik_leg_setup(prefix='Test',side='L')
#print(L_leg_ik)

def foot_rig_setup(prefix='Test',side='L',foot_joint=mc.ls(sl=True),knee_ctrl='knee_loc'):
    """
    Function builds foot rig with basic animation attributes.
    """ 
    print('DEBUG: >>>' ,foot_joint) 
    foot_joint_list = mc.listRelatives(foot_joint,ad=True,type='joint')
    foot_joint_list.append(foot_joint)
    foot_joint_list.reverse()
    
    print(foot_joint_list)
    mc.select(cl=True)
    
    # Setup Toe Controller
    toe_pos = mc.xform(foot_joint_list[3],q=True,t=True,ws=True)
    toe_offset = mc.group(n='%s_%s_toe_offset_01'%(prefix, side),em=True)
    toe_ctrl = mc.circle(n='%s_%s_toe_ctrl_01'%(prefix, side))[0]
    mc.parent(toe_ctrl, toe_offset)
    mc.parentConstraint(foot_joint_list[3],toe_offset)
    mc.parentConstraint(foot_joint_list[3],toe_offset,e=True,rm=True)
    mc.xform(toe_offset,t=[0,10,0],r=True)
    mc.xform('%s.rotatePivot'%(toe_ctrl),t=toe_pos,ws=True,a=True)
    mc.xform('%s.scalePivot'%(toe_ctrl),t=toe_pos,ws=True,a=True)
    mc.xform('%s.rotatePivot'%(toe_offset),t=toe_pos,ws=True,a=True)
    mc.xform('%s.scalePivot'%(toe_offset),t=toe_pos,ws=True,a=True)

    # Setup Ball Controller
    print('FOOT JOINT LIST: %s' %(foot_joint_list))
    ball_pos = mc.xform(foot_joint_list[4],q=True,t=True,ws=True)
    ball_offset = mc.group(n='%s_%s_ball_offset_01'%(prefix, side),em=True)
    ball_ctrl = mc.circle(n='%s_%s_ball_ctrl_01'%(prefix, side))[0]
    mc.parent(ball_ctrl, ball_offset)
    mc.parentConstraint(foot_joint_list[4],ball_offset)
    mc.parentConstraint(foot_joint_list[4],ball_offset,e=True,rm=True)
    mc.xform(ball_offset,t=[0,14,0],r=True)
    mc.xform('%s.rotatePivot'%(ball_ctrl),t=ball_pos,ws=True,a=True)
    mc.xform('%s.scalePivot'%(ball_ctrl),t=ball_pos,ws=True,a=True)
    mc.xform('%s.rotatePivot'%(ball_offset),t=ball_pos,ws=True,a=True)
    mc.xform('%s.scalePivot'%(ball_offset),t=ball_pos,ws=True,a=True)
    mc.parent(ball_offset,toe_ctrl) 
    
    # Constrain joints to foot controls
    mc.parentConstraint(toe_ctrl,foot_joint_list[3])
    mc.parentConstraint(ball_ctrl,foot_joint_list[4])
    
    # Parent IK Handles to Reverse Foot Joints
    mc.parent('%s_%s_toe_ikHandle_01'%(prefix,side),foot_joint_list[3])
    mc.parent('%s_%s_ball_ikHandle_01'%(prefix,side),foot_joint_list[4])
    mc.parent('%s_%s_leg_ikHandle_01'%(prefix,side),foot_joint_list[-1])
    
    # get pos vector for foot control
    heel_pos = mc.xform(foot_joint_list[2],q=True,t=True,ws=True)
    toe_vector = om.MVector(toe_pos[0],0,toe_pos[2])
    heel_vector = om.MVector(heel_pos[0],heel_pos[1],heel_pos[2])    
    foot_ctrl_pos = (toe_vector - heel_vector) * 0.5 + heel_vector

    # Place foot control
    foot_ctrl_loc = create_locator(foot_ctrl_pos)
    foot_ctrl = create_foot_ctrl(prefix,side)
    mc.move(foot_ctrl_pos.x,foot_ctrl_pos.y,foot_ctrl_pos.z,foot_ctrl)
    mc.makeIdentity(foot_ctrl,pn=True,a=True)
    mc.parentConstraint(foot_ctrl,foot_joint_list[0],mo=True)
    print(foot_joint_list[0])
    mc.parent(toe_offset,foot_joint_list[2])
    
    # Parent knee controller to foot controller
    mc.parent(knee_ctrl,foot_ctrl)
    mc.makeIdentity(knee_ctrl,a=True,pn=True)
    mc.setAttr("%s.sx"%(knee_ctrl),lock=True,keyable=False,channelBox=False)
    mc.setAttr("%s.sy"%(knee_ctrl),lock=True,keyable=False,channelBox=False)
    mc.setAttr("%s.sz"%(knee_ctrl),lock=True,keyable=False,channelBox=False)
    mc.setAttr("%s.v"%(knee_ctrl),lock=True, keyable=False,channelBox=False)
    
    # Add foot Control Attributes
    # Toe Rise Attribute
    mc.select(foot_ctrl)
    mc.addAttr(foot_ctrl,longName='ToeRise',at='double',dv=0,min=-50,max=50)
    mc.setAttr('%s.ToeRise'%(foot_ctrl),e=True, keyable=True)
    
    # Toe Rise SDK's
    mc.setDrivenKeyframe('%s.rotateZ'%(foot_joint_list[2]),cd='%s.ToeRise'%(foot_ctrl))
    mc.setAttr('%s.ToeRise'%(foot_ctrl),-50)
    mc.setAttr('%s.rotateZ'%(foot_joint_list[2]),-50)
    mc.setDrivenKeyframe('%s.rotateZ'%(foot_joint_list[2]),cd='%s.ToeRise'%(foot_ctrl))
    mc.setAttr('%s.ToeRise'%(foot_ctrl),50)
    mc.setAttr('%s.rotateZ'%(foot_joint_list[2]),50)
    mc.setDrivenKeyframe('%s.rotateZ'%(foot_joint_list[2]),cd='%s.ToeRise'%(foot_ctrl))
    mc.setAttr('%s.ToeRise'%(foot_ctrl),0)
    
    # Heel Pivot Attribute
    mc.select(foot_ctrl)
    mc.addAttr(foot_ctrl,longName='HeelPivot',at='double',dv=0,min=-50,max=50)
    mc.setAttr('%s.HeelPivot'%(foot_ctrl),e=True, keyable=True)
    # Heel Pivot SDK's
    mc.setDrivenKeyframe('%s.rotateY'%(foot_joint_list[2]),cd='%s.HeelPivot'%(foot_ctrl))
    mc.setAttr('%s.HeelPivot'%(foot_ctrl),-50)
    mc.setAttr('%s.rotateY'%(foot_joint_list[2]),-50)
    mc.setDrivenKeyframe('%s.rotateY'%(foot_joint_list[2]),cd='%s.HeelPivot'%(foot_ctrl))
    mc.setAttr('%s.HeelPivot'%(foot_ctrl),50)
    mc.setAttr('%s.rotateY'%(foot_joint_list[2]),50)
    mc.setDrivenKeyframe('%s.rotateY'%(foot_joint_list[2]),cd='%s.HeelPivot'%(foot_ctrl))
    mc.setAttr('%s.HeelPivot'%(foot_ctrl),0)
    
    # Foot Banking Attribute
    mc.select(foot_ctrl)
    mc.addAttr(foot_ctrl,longName='FootBanking',at='double',dv=0,min=-50,max=50)
    mc.setAttr('%s.FootBanking'%(foot_ctrl),e=True, keyable=True)
    # Foot Banking SDK's
    mc.setDrivenKeyframe('%s.rotateZ'%(foot_joint_list[0]),cd='%s.FootBanking'%(foot_ctrl))
    mc.setDrivenKeyframe('%s.rotateZ'%(foot_joint_list[1]),cd='%s.FootBanking'%(foot_ctrl))
    mc.setAttr('%s.FootBanking'%(foot_ctrl),-50)
    mc.setAttr('%s.rotateZ'%(foot_joint_list[0]),50)
    mc.setDrivenKeyframe('%s.rotateZ'%(foot_joint_list[0]),cd='%s.FootBanking'%(foot_ctrl))
    mc.setDrivenKeyframe('%s.rotateZ'%(foot_joint_list[1]),cd='%s.FootBanking'%(foot_ctrl))
    mc.setAttr('%s.FootBanking'%(foot_ctrl),50)
    mc.setAttr('%s.rotateZ'%(foot_joint_list[0]),0)
    mc.setAttr('%s.rotateZ'%(foot_joint_list[1]),-50)
    mc.setDrivenKeyframe('%s.rotateZ'%(foot_joint_list[0]),cd='%s.FootBanking'%(foot_ctrl))
    mc.setDrivenKeyframe('%s.rotateZ'%(foot_joint_list[1]),cd='%s.FootBanking'%(foot_ctrl))
    mc.setAttr('%s.FootBanking'%(foot_ctrl),0)    
    
    # Lock and hide Scale and Visibility Channels so animators dont break my Rig.........
    mc.setAttr("%s.sx"%(foot_ctrl),lock=True,keyable=False,channelBox=False)
    mc.setAttr("%s.sy"%(foot_ctrl),lock=True,keyable=False,channelBox=False)
    mc.setAttr("%s.sz"%(foot_ctrl),lock=True,keyable=False,channelBox=False)
    mc.setAttr("%s.v"%(foot_ctrl),lock=True, keyable=False,channelBox=False)   
        
    return foot_ctrl


def build_ik_leg(prefix='Test',side='L'):
    """
    Function builds entire IK leg Rig with basic animation controls.
    """ 
    
    if side == 'L':
        L_ik_leg = ik_leg_setup(prefix,side)
        L_foot_rig = foot_rig_setup(prefix,side,L_ik_leg[0][1],L_ik_leg[-1])
    elif side == 'R':
        R_ik_leg = ik_leg_setup(prefix,side)
        R_foot_rig = foot_rig_setup(prefix,side,R_ik_leg[0][1],R_ik_leg[1])
        
    
R_ik_leg_rig = build_ik_leg(prefix='EightBall',side='R')
L_ik_leg_rig = build_ik_leg(prefix='EightBall',side='L')
