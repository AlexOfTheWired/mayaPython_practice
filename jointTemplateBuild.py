import maya.cmds as mc

def templateJointSetup(prefix='Test'):
    
    # Assign variable for Active Selection List
    selection_list = mc.ls(sl=True)
    
    if len(selection_list) >=3:
        pass
    else:
        mc.error('Must select at least 3 guide objects!') 
    
    # Clear active selection list
    mc.select(cl=True)
    # Create empty list for locator world space translation vectors
    loc_position_list = []
    joint_fk_list = []
    
    # Iterate over Locators with for loop
    for loc in selection_list:
        # Get Locator world space Transform data
        loc_position = mc.xform(loc,q=True,translation=True,ws=True,a=True)
        # Append locator position vector to a list
        loc_position_list.append(loc_position) 
        print (loc_position_list)   
    
    # Iterate over locators to create new joints.   
    for idx in xrange(len(loc_position_list)):
        # Assign template locator name to variable
        loc_name = '%s'%(selection_list[idx])
        new_jnt_name = '%s_%s'%(prefix,loc_name.replace('_loc_','_jnt_'))
        print(new_jnt_name)        
        # Create joint and move to template locators
        fk_joint = mc.joint(n=new_jnt_name, p=loc_position_list[idx])
        joint_fk_list.append(fk_joint)
        
    for jnt in joint_fk_list:
        mc.joint(jnt, edit=True, oj='xyz', sao='yup', ch=True, zso=True)

templateJointSetup(prefix='Test')

