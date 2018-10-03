import maya.cmds as mc
def mirrorLocator(loc_list = mc.ls(sl=True)):
    
    loc_pos_tran = mc.xform(loc_list[0],q=True,t=True,ws=True,a=True)
    print(loc_pos_tran)
    loc_pos_rot = mc.xform(loc_list[0],q=True,ro=True,ws=True,a=True)
    print(loc_pos_rot)
    
    if loc_pos_tran[0] < 0:
        mirror_loc_pos_tran = abs(loc_pos_tran[0])
    else:
        mirror_loc_pos_tran = loc_pos_tran[0]
        
    if loc_pos_rot[1] > 0:
        mirror_loc_rot_y = (-(loc_pos_rot[1]))
    elif loc_pos_rot[1] < 0:
        mirror_loc_rot_y = (abs(loc_pos_rot[1]))
    else:
        mirror_loc_rot_y = loc_pos_rot[1]
    
    if loc_pos_rot[2] < 0:
        mirror_loc__rot_z = abs(loc_pos_rot[2])
    elif loc_pos_rot[2] > 0:
        mirror_loc__rot_z = (-(loc_pos_rot[2]))
    else:
        mirror_loc__rot_z = loc_pos_rot[2]        
        
    mc.setAttr('%s.translateX'%(loc_list[-1]), mirror_loc_pos_tran)
    mc.setAttr('%s.translateY'%(loc_list[-1]), loc_pos_tran[1])
    mc.setAttr('%s.translateZ'%(loc_list[-1]), loc_pos_tran[2])
    
    mc.setAttr('%s.rotateX'%(loc_list[-1]), loc_pos_rot[0])
    mc.setAttr('%s.rotateY'%(loc_list[-1]), mirror_loc_rot_y)
    mc.setAttr('%s.rotateZ'%(loc_list[-1]), mirror_loc__rot_z)

mirrorLocator(loc_list = mc.ls(sl=True))