import maya.cmds as mc
import timeit

def build_loc_tail(prefix='Test',side='L',loc_num=5):
    
    start = timeit.timeit()
    # Tail Length
    tail_length = 15
    loc_average = (tail_length / float(loc_num))
    print(loc_average)
    
    # Initial counter for Z axis placement    
    z_pos = 0
    # Empty list for locator population
    loc_list = []
    
    # Loop for Locator creation
    for idx in xrange(loc_num):
        loc = mc.spaceLocator(p=(0,0,z_pos))
        z_pos += loc_average
        mc.CenterPivot(loc)
        loc_list.append(loc)
        if idx == 0:
            pass
        if idx >= 1:
            mc.parent(loc,loc_list[idx-1])
        
    # Loop for renaming locators
    for idx in xrange(len(loc_list)):
        new_idx = (idx+1)
        loc_name = '%s_%s_tail_loc_%s'%(prefix,side,new_idx)
        re_loc_name = mc.rename(loc_list[idx],loc_name,ignoreShape=False)
        loc_list[idx] = re_loc_name
        
    end = timeit.timeit()
    print(end - start)
    return loc_list
        

def get_tail_translate(tail_loc):
    
    translate_list = []
    
    for loc in xrange(len(tail_loc)):
        loc_pos = mc.xform(tail_loc[loc],q=True,t=True,ws=True)
        translate_list.append(loc_pos)
        
    return translate_list
    
    
def get_tail_rotate(tail_loc):
    
    rotate_list = []
    
    for loc in xrange(len(tail_loc)):
        loc_rot = mc.xform(tail_loc[loc],q=True,ro=True,ws=True)
        rotate_list.append(loc_rot)
    
    return rotate_list
        
        
test_tail_loc = build_loc_tail(loc_num=6)
get_tail_translate(test_tail_loc)
get_tail_rotate(test_tail_loc)

print(test_tail_loc)