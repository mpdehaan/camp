import camp.utils as utils

def test_roll_left():
    assert utils.roll_left([1,2,3,4,5]) == [2,3,4,5,1]

def test_roll_right():
    assert utils.roll_right([1,2,3,4,5]) == [5,1,2,3,4]

