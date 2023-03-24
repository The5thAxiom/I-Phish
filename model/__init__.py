import random
from requests import get
from pandas import Series

from model.feature_engineering import feature_engineer

def resolve_url(url: str) -> str:
    return get(url).url

def predict(url: str) -> bool:
    if type(url) is str:
        try:
            final_url = resolve_url(url)
        except:
            return False, "could not resolve URL"
        try:
            urlData = feature_engineer(final_url)
        except:
            return False, "feature engineering failed"
        return True if random.randint(0, 1) else False, "OK"
    else:
        raise TypeError("url should be a string")