from flask import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/genkey")
def generateKey():
    return render_template("key.html")

@app.route("/sign")
def signFile():
    return render_template("sign.html")

@app.route("/verify")
def verifyFile():
    return render_template("verify.html")

if __name__ == "__main__":
    app.run(debug=True)