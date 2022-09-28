from flask import Flask


app = Flask(__name__)

@app.route('/healthz')
def index():
    return "200 OK"


if __name__ == "__main__":
    app.run(debug=True)
