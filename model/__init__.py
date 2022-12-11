import random

def run_model(url: str) -> bool:
    if type (str) is str:
        return True if random.randint(0, 1) else False
    else:
        raise TypeError("url should be a string")