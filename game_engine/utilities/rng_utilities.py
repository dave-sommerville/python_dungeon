import random
def fifty_fifty():
    return random([True, False])

def weighted_decision(weight: float):
    return random.random() < weight

def random_list_element(list):
    return random.choice((list))