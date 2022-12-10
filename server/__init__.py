from flask import Flask, jsonify, request
from model import run_model

app = Flask(__name__)

@app.route('/validate', methods=['GET', 'POST'])
def validate():
    url = request.json.get("url", None)
    if url is not None:
        ans = run_model(url)
        return jsonify({
            'ans': ans
        })
    else:
        return jsonify({
            'msg': 'please give a url'
        })