import maya.cmds as mc

def overrideColorTool(R=0.0,G=0.0,B=0.0):
    loc_selection_list = mc.ls(sl=True)
    print(loc_selection_list)
    rGB = [R, G, B]
    for loc in loc_selection_list:
        loc_shape_node = mc.listRelatives(loc, shapes=True)[0]
        print(loc_shape_node)
        mc.setAttr('%s.overrideEnabled'%(loc_shape_node), True)
        mc.setAttr('%s.overrideRGBColors'%(loc_shape_node), True)
        mc.setAttr('%s.overrideColorRGB'%(loc_shape_node), R, G, B)

overrideColorTool(R=1.0,G=0.15,B=0.0)