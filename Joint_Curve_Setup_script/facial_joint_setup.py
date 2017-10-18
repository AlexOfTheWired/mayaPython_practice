jnt_list = []


def position_and_freeze(object, destination):
    obj_pos = mc.xform('locator1', q=True, ws=True, t=True)
    mc.move(a=True, p=obj_pos[0], obj_pos[1], obj_pos[2])
    mc.makeIdentity(destination, apply=True)


def facial_joint_setup(prefix):
    
    
    for loc in curve_selection:
        print ('balls')
        #offset_jnt = mc.joint(n=(prefix + "_offset_jnt_"))
        jnt_list.append
        position_and_freeze(offset_jnt)
        #main_jnt = mc.joint(n=(prefix + "_main_jnt_"))
        
        
    
facial_joint_setup("curve1")
    
print(curve_selection)    
    