from flask import *
from backend import backend
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"]='dump'

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

@app.route('/download/public')
def download_public():
    path = os.path.join(current_app.root_path + "/" + app.config["UPLOAD_FOLDER"])
    backend.get_public_key_file(os.path.join(path,"public.pub"))
    #ext = filename.rsplit('.', 1)[1].lower()
    return send_file(os.path.join(path,"public.pub"), as_attachment=True)

@app.route('/download/private')
def download_private():
    #Program untuk generate key di sini
    path = os.path.join(current_app.root_path + "/" + app.config["UPLOAD_FOLDER"])
    backend.get_private_key_file(os.path.join(path,"private.pri"))
    #ext = filename.rsplit('.', 1)[1].lower()
    return send_file(os.path.join(path,"private.pri"), as_attachment=True)
    """
    if(ext in ALLOWED_EXTENSIONS_CITRA):
        return send_file(os.path.join(path,filename), as_attachment=True, mimetype='image/'+str(ext))
    elif(ext in ALLOWED_EXTENSIONS_VIDEO):
        return send_file(os.path.join(path,filename), as_attachment=True, mimetype='video/'+str(ext))
    """

if __name__ == "__main__":
    app.run(debug=True)