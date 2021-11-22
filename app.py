from flask import *
from backend import backend, sha256
from backend import elgamal
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"]='dump'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/genkey")
def generateKey():
    elgamal.key_generator()
    return render_template("key.html")

@app.route("/sign")
def signFile():
    return render_template("sign.html")

@app.route('/sign', methods=["POST"])
def sign_file_process():
    if request.method == 'POST':
        path = os.path.join(current_app.root_path + "/" + app.config["UPLOAD_FOLDER"])
        key = request.form.get("key")
        f = request.files['input-file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config["UPLOAD_FOLDER"] ,filename))
        ds2 = backend.get_hash_file(os.path.join(app.config["UPLOAD_FOLDER"] ,filename))
        print("hasil 1 (encrypt)= ",ds2)
        ds = elgamal.encrypt_elgamal(ds2)
        f = open(os.path.join(app.config["UPLOAD_FOLDER"] ,filename), "ab")
        #plain = f.read()
        #cipher = rc4.encrypt(plain, key)
        #open("dump/output", "wb").write(cipher)
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
        key = request.form.get("key")
        f = request.files['input-file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config["UPLOAD_FOLDER"] ,filename))
        #plain = f.read()
        #cipher = rc4.encrypt(plain, key)
        #open("dump/output", "wb").write(cipher)
        content = bytes(backend.find_content(os.path.join(app.config["UPLOAD_FOLDER"] ,filename))[2:-1],"utf-8")
        fbin = open("dump/content.bin", "wb")
        fbin.write(content)
        fbin.close()
        #print("Content:",content)
        hasil1 = backend.get_hash_file("dump/content.bin")
        hasil2_temp = int(backend.find_signature(os.path.join(app.config["UPLOAD_FOLDER"] ,filename)))
        hasil2 = elgamal.decrypt_elgamal(hasil2_temp)
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
    #backend.get_private_key_file(os.path.join(path,"private.pri"))
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