import random
def fifty_fifty():
    return random.choice([True, False])

def weighted_decision(weight: float):
    return random.random() < weight

def random_list_element(lst):
    return random.choice(lst)

def random_integer(min_val, max_val):
    return random.randint(min_val, max_val)

