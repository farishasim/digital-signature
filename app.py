from flask import *
from backend import backend, elgamal, sha256
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"]='dump'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/genkey")
def generateKey():
    return render_template("key.html")

@app.route("/genkey/new")
def generateNewKey():
    elgamal.key_generator()
    return "done"

@app.route("/sign")
def signFile():
    return render_template("sign.html")

@app.route('/sign', methods=["POST"])
def sign_file_process():
    if request.method == 'POST':
        path = os.path.join(current_app.root_path + "/" + app.config["UPLOAD_FOLDER"])
        key = request.files['input-key']
        f = request.files['input-file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config["UPLOAD_FOLDER"] ,filename))
        k_filename = secure_filename(key.filename)
        key.save(os.path.join(app.config["UPLOAD_FOLDER"] ,k_filename))
        ds2 = backend.get_hash_file(os.path.join(app.config["UPLOAD_FOLDER"] ,filename))
        print("hasil 1 (encrypt)= ",ds2)
        ds = elgamal.encrypt_elgamal(ds2, os.path.join(app.config["UPLOAD_FOLDER"] ,k_filename))
        f = open(os.path.join(app.config["UPLOAD_FOLDER"] ,filename), "ab")
        f.write(bytes(f'<ds>{ds}</ds>', encoding='utf8'))
        f.close()
        return send_file(os.path.join(app.config["UPLOAD_FOLDER"] ,filename), as_attachment=True)
    return 

@app.route("/verify")
def verifyFile():
    return render_template("verify.html")

@app.route('/verify', methods=["POST"])
def verify_file_process():
    if request.method == 'POST':
        path = os.path.join(current_app.root_path + "/" + app.config["UPLOAD_FOLDER"])
        f = request.files['input-file']
        key = request.files['input-key']
        filename = secure_filename(f.filename)
        k_filename = secure_filename(key.filename)
        f.save(os.path.join(app.config["UPLOAD_FOLDER"] ,filename))
        key.save(os.path.join(app.config["UPLOAD_FOLDER"] ,k_filename))
        content = bytes(backend.find_content(os.path.join(app.config["UPLOAD_FOLDER"] ,filename)),"utf-8")
        fbin = open("dump/content.txt", "wb+")
        fbin.write(content)
        fbin.close()
        #print("Content:",content)
        hasil1 = backend.get_hash_file("dump/content.txt")
        hasil2_temp = int(backend.find_signature(os.path.join(app.config["UPLOAD_FOLDER"] ,filename)))
        hasil2 = elgamal.decrypt_elgamal(hasil2_temp, os.path.join(app.config["UPLOAD_FOLDER"] , k_filename))
        print("hasil 1", hasil1)
        print("hasil 2", hasil2)
        if (hasil2 == -1):
            return render_template("verify.html", kosong=True)
        elif(hasil1 == hasil2):
            return render_template("verify.html", verify=True, sign=hasil1)
        else:
            return render_template("verify.html", not_verify=True)
    return

@app.route('/download/public')
def download_public():
    path = os.path.join(current_app.root_path + "/" + app.config["UPLOAD_FOLDER"])
    #backend.get_public_key_file(os.path.join(path,"public.pub"))
    #ext = filename.rsplit('.', 1)[1].lower()
    return send_file(os.path.join(path,"public.pub"), as_attachment=True)

@app.route('/download/private')
def download_private():
    #Program untuk generate key di sini
    path = os.path.join(current_app.root_path + "/" + app.config["UPLOAD_FOLDER"])
    return send_file(os.path.join(path,"private.pri"), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)