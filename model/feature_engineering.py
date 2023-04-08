from urllib.parse import urlparse, urlsplit
import requests
import pandas as pd
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from re import findall

def search_webpage_features(url, df):
    try:
        # Send a request to the URL and get its HTML content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract HTML tag count
        html_tag_count = len(soup.find_all())

        # Extract hyperlink count
        hyperlink_count = len(soup.find_all('a'))

        # Extract iframe count
        iframe_count = len(soup.find_all('iframe'))

        # Extract escape count
        escape_count = response.text.count('\\')

        # Extract eval count
        eval_count = response.text.count('eval(')

        # Extract link count
        link_count = response.text.count('link(')

        # Extract underscore count
        underscore_count = response.text.count('_')

        # Extract exec count
        exec_count = response.text.count('exec(')

        # Extract search count
        search_count = response.text.count('search(')

        # Check if exception handling is present
        exception_handling_present = 'try' in response.text and 'except' in response.text

        # Add features as columns to the DataFrame
        df.loc[url, 'html_tag_count'] = html_tag_count
        df.loc[url, 'hyperlink_count'] = hyperlink_count
        df.loc[url, 'iframe_count'] = iframe_count
        df.loc[url, 'escape_count'] = escape_count
        df.loc[url, 'eval_count'] = eval_count
        df.loc[url, 'link_count'] = link_count
        df.loc[url, 'underscore_count'] = underscore_count
        df.loc[url, 'exec_count'] = exec_count
        df.loc[url, 'search_count'] = search_count
        df.loc[url, 'exception_handling_present'] = exception_handling_present

    except requests.exceptions.RequestException:
        # Handle connection errors by setting NaN values for all features
        df.loc[url, 'html_tag_count'] = float('nan')
        df.loc[url, 'hyperlink_count'] = float('nan')
        df.loc[url, 'iframe_count'] = float('nan')
        df.loc[url, 'escape_count'] = float('nan')
        df.loc[url, 'eval_count'] = float('nan')
        df.loc[url, 'link_count'] = float('nan')
        df.loc[url, 'underscore_count'] = float('nan')
        df.loc[url, 'exec_count'] = float('nan')
        df.loc[url, 'search_count'] = float('nan')
        df.loc[url, 'exception_handling_present'] = float('nan')

def getHostname(url):
    try:
        parsedUrl = urlparse(url)
        return str(parsedUrl.hostname)
    except:
        return url

def getPortN(url):
    try:
        parsedUrl = urlparse(url)
        port = parsedUrl.port
        if port is None:
            return 80
        else:
            return port
    except:
        return 80

def hasSuspiciousSymbol(url):
    checkSymbol = ['=', '?', '%', '+', '$', '!', '*', ',', '@']
    # '=','?','%' => used for GET Request.
    # More possibility of Phishing site.
    for symbol in checkSymbol:
        if symbol in url:
            return True
    return False

def getPathLength(url):
    try:
        parsedUrl = urlparse(url)
        return len(str(parsedUrl.path))
    except:
        return len(url)

def add_scheme(url):
    try:
        parsedUrl = urlparse(url)
        if (parsedUrl.scheme == ''):
            return str('http://'+url)
        else:
            return url
    except:
        return url

def extract_features(url):
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    html_tags = len(soup.find_all())
    hyperlinks = len(soup.find_all('a'))
    iframes = len(soup.find_all('iframe'))
    evals = len(findall(r'eval\(', response.text))
    escapes = len(findall(r'escape\(', response.text))
    links = len(findall(r'link\(', response.text))
    underscapes = len(findall(r'_\(', response.text))
    execs = len(findall(r'exec\(', response.text))
    searches = len(findall(r'search\(', response.text))
    exception_handling = 'yes' if len(soup.find_all('try')) > 0 else 'no'

    return [html_tags, hyperlinks, iframes, evals, escapes, links, underscapes, execs, searches, exception_handling]

def feature_engineer(url: str):
    url = url[8:] if url.startswith("https://") else url[7:] if  url.startswith("http://") else url
    url = url[15:] if url.startswith("localhost:8000/") else url
    urlData = pd.DataFrame()

    urlData.loc[0, 'numberDots'] = url.count('.')
    urlData.loc[0, 'numberHyphen'] = url.count('-')
    urlData.loc[0, 'numberDigits'] = len(findall(r'/\d/', url))
    urlData.loc[0, 'urlLen'] = len(url)
    urlData.loc[0, 'hostNameLen'] = len(getHostname(url))
    urlData.loc[0, 'pathLen'] = len(str(urlparse(url).path))
    urlData.loc[0, 'numberBackSlash'] = url.count('/')
    urlData.loc[0, 'hasHttps'] = 1 if 'https' in url else 0
    urlData.loc[0, 'portN'] = getPortN(url)
    # urlData.loc[0, 'hasSuspiciousSymbol'] = hasSuspiciousSymbol(url)

    # search_webpage_features(url, urlData)

    return urlData
