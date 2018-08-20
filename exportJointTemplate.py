import maya.cmds as mc
import json

def exportJointTemplate(jnt_sel=mc.ls(sl=True),characterName='Test',rigType='Face'):

    if len(jnt_sel) < 1:
        raise mc.error('Must have at least one joint selected')
    
    # Get scene working directory
    mayaPath_name = mc.workspace( q=True,  fn=True )
    # Append data folder to dath with string formating
    dataPath_name = '%s/data'%(mayaPath_name)
    # Combine full path to create file name
    file_name = '%s/%s_%s_jointTemplate.json'%(dataPath_name,characterName,rigType)


    # Create empty json object
    json_string = {}
    
    for idx in range(len(jnt_sel)):
        # Assign key for jnt position values
        joint_position = mc.xform(jnt_sel[idx], q=True, t=True, ws=True)
        # Assign key for joint parent values 
        joint_parent = mc.listRelatives(jnt_sel[idx],p=True)[0]

        # Format json object     
        joint_node = {
            'Position': [joint_position[0],joint_position[1],joint_position[2]],
            'Parent':('%s'%(joint_parent))
        }
        json_string[jnt_sel[idx]] = joint_node
        
    # use context manager to write object data to json file
    with open( file_name, 'w+') as json_file:
        json.dump(json_string, json_file, sort_keys=True, indent=4, separators=(',' , ':'))
        json_file.close()   

exportJointTemplate(jnt_sel=mc.ls(sl=True),characterName='Test')