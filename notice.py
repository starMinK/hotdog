from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
import certifi
from pymongo import MongoClient

ca = certifi.where()
client = MongoClient('mongodb+srv://zoon:1234@cluster0.dbul0bg.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.hotdogs


@app.route('/notice')
def home():
   return render_template('notice.html')

@app.route("/hotdog-list", methods=["GET"])
def hotdog_get():
    hotdog_list = list(db.menu.find({}, {'_id': False}))
    return jsonify({'hotdogs':hotdog_list})

@app.route("/detail")
def detail():
    return render_template("detail.html")

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
