import random
from requests import get
from pandas import Series

from model.feature_engineering import feature_engineer

def resolve_url(url: str) -> str:
    return get(url).url

def predict(url: str) -> bool:
    if type(url) is str:
        # resolving the url:
        # this will get us the actual URL and not just the redirect
        try:
            final_url = resolve_url(url)
        except:
            return False, "could not resolve URL"
        
        # feature engineering:
        # here, we convert the raw URL into a DataFrame, containing the features we need
        try:
            urlData = feature_engineer(final_url)
        except:
            return False, "feature engineering failed"
        
        # making predictions:
        # now, we give the features we got above into the model to get our predictions
        return True if random.randint(0, 1) else False, "OK"
    else:
        raise TypeError("url should be a string")