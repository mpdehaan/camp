
def roll_left(x):
    """ 
    Circularly shifts a list to the left
    [ 1,2,3] -> [2,3,1] 
    """
    new_list = x[:]
    first = new_list.pop(0)
    new_list.append(first)
    return new_list

def roll_right(x):
    """ 
    Circularly shifts a list to the right
    [1,2,3] -> [3,1,2] 
    """
    new_list = x[:]
    first = new_list.pop()
    new_list.insert(0, first)
    return new_list


