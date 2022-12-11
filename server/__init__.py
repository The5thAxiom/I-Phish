from flask import Flask, jsonify, request
from model import run_model

app = Flask(__name__)

@app.route('/is-valid-url', methods=['POST'])
def validate():
    url = request.json.get("url", None)
    if url is not None:
        ans = run_model(url)
        return jsonify({
            'msg': 'OK',
            'ans': ans
        })
    else:
        return jsonify({
            'msg': 'please give a url'
        })

@app.route('/validate', methods=['POST'])
def validate_list():
    urls = request.json.get('urls', None)
    url = request.json.get("url", None)

    multiple_urls = urls is not None and isinstance(urls, list)
    single_url = urls is None and url is not None

    if multiple_urls or single_url:
        try:
            ans = {url: run_model(url) for url in urls} if multiple_urls else run_model(url)
            return jsonify({
                'msg': 'OK',
                'ans': ans
            })
        except TypeError:
            msg = "'urls' should be a list of strings" if multiple_urls else 'url should be a string'
            return jsonify({
                'msg': msg
            })
        except:
            return jsonify({
                'msg': 'an error occurred'
            }), 500
    else:
        return jsonify({
            'msg': 'please give url(s) to validate'
        })