import maya.cmds as mc

def overrideColorTool(R=0.0,G=0.0,B=0.0):
    """
    Tool for overriding color of each control or locator and its descendent shape nodes.
    """
    
    # Assign selected objects to list
    selection_list = mc.ls(sl=True)
    
    for loc in xrange(len(selection_list)):
        # Get list of shape nodes for each item in selection_list.
        
        shape_idx = (loc+1)
        loc_shape_nodes = mc.listRelatives(selection_list[loc], shapes=True,f=True)
        print(loc_shape_nodes)
        root_shape_name = '%s'%(selection_list[loc])
        for shape in xrange(len(loc_shape_nodes)):
            print('Shape Node:   ',loc_shape_nodes[shape])
            
            # Iterate through each shape node in list rename to have unique name.
            idx = (shape + 1)
            child_shape_name = root_shape_name.replace('_%s%s'%(root_shape_name[-2],root_shape_name[-1]),'_shape%s'%(shape_idx))
            print(child_shape_name)
            shape_node = mc.rename(loc_shape_nodes[shape],child_shape_name)
            print('SHAPE NODE NEW NAME:     ',shape_node)
            
            # Try setting attributes to selected RGB values.
            try:
                mc.setAttr('%s.overrideEnabled'%(shape_node), True)
                mc.setAttr('%s.overrideRGBColors'%(shape_node), True)
                mc.setAttr('%s.overrideColorRGB'%(shape_node), R, G, B)
            except:
                mc.error('More that one object shares a name. Each Shape Node must have unique name.')

overrideColorTool(R=0.05,G=0.0,B=0.9) # Left side Color
overrideColorTool(R=0.9,G=0.0,B=0.1) # Right side Color
overrideColorTool(R=1.0,G=0.33,B=0.0) # Center Color