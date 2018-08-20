import maya.cmds as mc
from pprint import pprint

def importJointTemplate(characterName='Test',rigType='Face'):
    
    mayaPath_name = mc.workspace( q=True,  fn=True )
    dataPath_name = '%s/data'%(mayaPath_name)
    file_name = '%s/%s_%s_jointTemplate.json'%(dataPath_name,characterName,rigType)
    
    
    with open(file_name, 'r') as json_file:
        import_nodes = json.load(json_file)
      
    
    for key in import_nodes:
        joint_obj = import_nodes[key]
        jnt_pos = joint_obj["Position"]
        if mc.objExists(key) == False:
            mc.joint(name=key,p=(jnt_pos[0],jnt_pos[1],jnt_pos[2]), radius=0.25)
            mc.select(clear=True)
        else:
            pass
        
    for key in import_nodes:
        joint_obj = import_nodes[key]
        jnt_parent = joint_obj['Parent']
        if mc.objExists(jnt_parent) == True:
            mc.parent(key,jnt_parent)
        else:
            pass
            


importJointTemplate(characterName='Test',rigType='Face')