from flask import Flask, jsonify, request
from greetings import say_hello_to

app = Flask(__name__)


@app.route("/")
def index() -> str:
    # transform a dict into an application/json response 
    return jsonify({"message": "It Works"})

@app.route("/hello", methods=['POST'])
def hello() -> str:
    greetee = request.json.get("greetee", None)
    response = {"message": say_hello_to(greetee), "server": request.host_url}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)     