from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Main page, nothing special..."

app.run(host='0.0.0.0',port=1080)
