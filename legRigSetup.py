import maya.cmds as mc
import maya.OpenMaya as om

def create_locator(pos):
    loc = mc.spaceLocator()
    mc.move(pos.x, pos.y, pos.z, loc)

# Function creates custom foot control
def create_foot_ctrl(prefix='Test',side='L'):
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

# Create active selection list
selection_list = mc.ls(sl=True)
    
# Query Translation vectors
root_pos = mc.xform(selection_list[0], q=True, ws=True, t=True)
mid_pos = mc.xform(selection_list[1], q=True, ws=True, t=True)
end_pos = mc.xform(selection_list[2], q=True, ws=True, t=True) 
   
def get_pole_vector_pos(root_pos, mid_pos, end_pos):

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

ik_handle_pole_vector_setup()

def ik_limb_presetup(prefix='Test',side='L'):
    
    leg_joint_list = mc.ls(sl=True)
    
    ik_leg_joint_list = mc.duplicate(leg_joint_list,rc=True)
        
    for idx in xrange(len(ik_leg_joint_list)):
        ik_node_name = ik_leg_joint_list[idx].replace('_jnt_03','_IK_jnt_01') 
        mc.rename(ik_leg_joint_list[idx],ik_node_name)
        ik_leg_joint_list[idx] = ik_node_name
    
    # create ik solvers for leg
    leg_ik_handle = mc.ikHandle(
                                n='%s_%s_leg_ikHandle_01'%(prefix, side),
                                sj=ik_leg_joint_list[0],
                                ee=ik_leg_joint_list[2],
                                sol='ikRPsolver'
                                )
                                
    ball_ik_handle = mc.ikHandle(
                                n='%s_%s_ball_ikHandle_01'%(prefix, side),
                                sj=ik_leg_joint_list[2],
                                ee=ik_leg_joint_list[3],
                                sol='ikSCsolver'
                                )
    
    toe_ik_handle = mc.ikHandle(
                                n='%s_%s_toe_ikHandle_01'%(prefix, side),
                                sj=ik_leg_joint_list[3],
                                ee=ik_leg_joint_list[-1],
                                sol='ikSCsolver'
                                )
                                
    return [leg_ik_handle,ball_ik_handle,toe_ik_handle]                     
                            
EightBall_l_leg_ik_handle = ik_limb_presetup('EightBall','L')[0][0]
print(EightBall_l_leg_ik_handle)

mc.select(EightBall_l_leg_ik_handle)
ik_knee_loc =ik_handle_pole_vector_setup()
mc.CenterPivot(ik_knee_loc)
mc.makeIdentity(ik_knee_loc,a=True,pn=True)
mc.poleVectorConstraint(ik_knee_loc,EightBall_l_leg_ik_handle)



def ik_leg_build():
    
    

    

mc.xform(foot_ctrl, s=[])



