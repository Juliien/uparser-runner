import time

from flask import Flask, jsonify, request
from src.urunner.runner import Urunner
app = Flask(__name__)


@app.route('/api/runner/run', methods=['GET', 'POST'])
def urunner_on_user_code():
    if request.method == 'POST':
        exercice = Urunner()
    elif request.method == 'GET':
        print("Fake data for now")
    return jsonify({'code': 200, 'response': 'test started'}), 200


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
