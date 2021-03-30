from flask import Flask ,Response, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json

app=Flask(__name__)
mongo = PyMongo(app, uri="mongodb://coworking:admin@117.53.44.15:30001,117.53.44.15:30002,117.53.44.15:30003/coworking?authSource=coworking&replicaSet=my-mongo-set")
collection = mongo.db.coworking

@app.route("/coworking/get_coworking", methods=["GET"])
def get_all_data():
    resps = dumps(collection.find({}))
    return resps

@app.route("/coworking/get_coworking/<id>", methods=["GET"])
def get__one_data(id):
    search = request.args.get('search')
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

if "__main__" == __name__:
    app.run(host='127.0.0.1', port=5000, debug=True)