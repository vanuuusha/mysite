import random


def predict(): # True - block, False - unblock
    num = random.randint(1, 2)
    if num == 1:
        return True
    return False