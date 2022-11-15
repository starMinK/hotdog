
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, redirect, url_for
import certifi

app = Flask(__name__)
ca = certifi.where()

client = MongoClient('mongodb+srv://zoon:1234@cluster0.dbul0bg.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.hotdogs

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/main", methods=["GET"])
def menu_get():
    menu_list = list(db.menu.find({}, {'_id': False}))
    return jsonify({'menu_list': menu_list})

@app.route("/recomment", methods=["GET"])
def recomment():
    return render_template('recomment.html');


if __name__ == "__main__":
    app.run('0.0.0.0', port=5500, debug=True)