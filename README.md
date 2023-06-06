# I-Phish

ML based detection of Phishing URL. Chrome Extension product. 

## Dev setup

-   setup venv: `python -m venv venv`
-   activate venv:
    -   linux: `source venv/bin/activate`
-   `pip install -r requirements`
-   after installing from pip: `

## Testing

-   `curl`:
    -   single url: `curl -X POST http://127.0.0.1:8000/validate -H 'Content-Type: application/json' -d '{"url":"abc"}'`
    -   list of urls: `curl -X POST http://127.0.0.1:8000/validate -H 'Content-Type: application/json' -d '{"urls": ["abc", "def", "ghi"]}'`

