from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/healthz')
def index():
    return jsonify(response= "200 OK")


if __name__ == "__main__":
    app.run(debug=True)
