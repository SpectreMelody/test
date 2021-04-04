from flask import Flask ,Response, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json

app=Flask(__name__)
mongo = PyMongo(app, uri="mongodb://coworking:admin@117.53.44.15:30001,117.53.44.15:30002,117.53.44.15:30003/coworking?authSource=coworking&replicaSet=my-mongo-set")
collection = mongo.db.coworking
collection2 = mongo.db.invoice

@app.route("/coworking/get_coworking", methods=["GET"])
def get_all_data():
    resps = dumps(collection.find({}))
    return resps

@app.route("/coworking/get_coworking/<id>", methods=["GET"])
def get__one_data(id):
    resps = dumps(collection.find({"_id":ObjectId(id)}))
    return resps

@app.route("/coworking/insert_coworking", methods=["POST"])
def insert_data():
    data = request.get_json()
    collection.insert(data)
    return "Succes Inserting"

@app.route("/coworking/update_coworking/<id>", methods=["PUT"])
def update_data(id):
    try:
        test = {
            "nama":request.form["nama"],
            "lokasi":{"X":request.form["X"],"Y":request.form["Y"]},
            "operasional":{"jam_buka":request.form["jam_buka"],"jam_tutup":request.form["jam_tutup"]},
            "harga":request.form["harga"],
            "fasilitas":[request.form["fasilitas"]],
            "membership":[request.form["membership"]],
            "reviews":[request.form["reviews"]],
            "is_aktif":request.form["is_aktif"]
    }

        collection.update_many(
            {'_id':ObjectId(id)},
            {'$set':test}
            )
        return "Data Berhasil di Update!"
    
    except:
        return "Mohon Isi Semua Data Untuk Menjalankan Update!"

# =========================== INVOICE ============================== #

@app.route("/invoice/insert_invoice", methods=["POST"])
def insert_invoice():
    invoice = request.get_json() or {
            'id_user': request.form['id_user'],
            'status': request.form['status'],
            'token': request.form['token'],
            'tempat': request.form['tempat'],
            'capacity': request.form['capacity'],
            'invoice': request.form['invoice'],
            'is_aktif': request.form['is_aktif']
        }
    collection2.insert(invoice)
    return "Succes Inserting"

@app.route("/invoice/get_invoice", methods=["GET"])
def get_all_invoice():
    resps = dumps(collection2.find({}))
    return resps

@app.route("/invoice/get_invoice/<id>", methods=["GET"])
def get_invoice_byid(id):
    resps = dumps(collection2.find({"_id":ObjectId(id)}))
    return resps

@app.route("/invoice/update_invoice/<id>", methods=["PUT"])
def update_invoice(id):
    try:
        invoice = request.get_json() or {
            'id_user': request.form['id_user'],
            'status': request.form['status'],
            'token': request.form['token'],
            'tempat': request.form['tempat'],
            'capacity': request.form['capacity'],
            'invoice': request.form['invoice'],
            'is_aktif': request.form['is_aktif']
        }

        collection2.update_many(
            {"_id":ObjectId(id)},
            {"$set": invoice}
        )

        return "Data Berhasil di Update!"
    
    except:
        return "Mohon Isi Semua Data Untuk Menjalankan Update!"


if "__main__" == __name__:
    app.run(host='127.0.0.1', port=5000, debug=True)