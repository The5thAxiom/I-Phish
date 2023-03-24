from pickle import load
import random
from requests import get
from pandas import Series

from sklearn.ensemble import StackingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

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
        
        model = load(open('model/model.sav', 'rb'))
        prediction = model.predict(urlData)[0]

        print(f'{url:} | {prediction:}')

        return True if prediction == 1 else False, "OK"

    else:
        raise TypeError("url should be a string")