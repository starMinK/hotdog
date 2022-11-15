from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://zoon:1234@cluster0.dbul0bg.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.hotdogs



@app.route('/')
def home():
   return render_template('detail.html')

@app.route("/hotdog-list", methods=["GET"])
def hotdog_get():
    hotdog_list = list(db.menu.find({}, {'_id': False}))
    return jsonify({'hotdogs':hotdog_list})

@app.route("/api/detail", methods=["POST"])
def detail_post():
    detail_receive = request.form['detail_give']
    detail_name = db.menu.find_one({'name': detail_receive},{'_id': False})
    return jsonify({'hotdogs':detail_name})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)