from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, redirect, url_for
import certifi

app = Flask(__name__)
ca = certifi.where()

client = MongoClient('mongodb+srv://zoon:1234@cluster0.dbul0bg.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.hotdogs

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'team1HotdogSecretKey'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib


@app.route("/")
def homeHtml():
    return render_template('index.html')


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# @app.route("/main", methods=["GET"])
# def menu_get():
    # menu_list = list(db.menu.find({}, {'_id': False}))
    # return jsonify({'menu_list': menu_list})


@app.route("/map")
def map():
    return render_template('map.html')

@app.route("/recomment")
def recomment():
    return render_template('recomment.html')


@app.route("/api/recomment", methods=["POST"])
def recomment_post():
    recomment_receive = request.form['recomment_give']
    recommnet_name = db.menu.find_one({'result': recomment_receive}, {'_id': False})
    return jsonify({'result': recommnet_name})

@app.route("/api/number", methods=["POST"])
def number_get():
    name_receive = request.form['name_give']
    recommnet_name = db.menu.find_one({'result':name_receive}, {'_id':False}) 
    print(recommnet_name['total'])
    return jsonify({'result':recommnet_name['total']})

@app.route("/api/plus", methods=["POST"])
def plus_post():
    num_receive = request.form['num_give']
    name_receive = request.form['name_give']
    print(num_receive)
    print(name_receive)
    db.menu.update_one({'result':name_receive}, {'$set':{'total': int(num_receive)}})
    return jsonify({'result':"total변경 성공"})

@app.route("/api/total", methods=["GET"])
def total_get():
    total_list = list(db.menu.find({}, {'_id':False}))
    return jsonify({'result':total_list})


@app.route('/notice')
def notice():
    return render_template('notice.html')


@app.route("/detail")
def detailHtml():
    return render_template('detail.html')


@app.route("/api/detail", methods=["POST"])
def detail_post():
    detail_receive = request.form['detail_give']
    detail_name = db.menu.find_one({'name': detail_receive}, {'_id': False})
    return jsonify({'hotdogs': detail_name})


@app.route("/hotdog-list", methods=["GET"])
def hotdog_get():
    hotdog_list = list(db.menu.find({}, {'_id': False}))
    return jsonify({'hotdogs': hotdog_list})


@app.route("/api/save-review", methods=["POST"])
def comment_save():
    star_count = request.form['starCount']
    comment = request.form['comment']
    pagecoor = request.form['pagecoor']
    token_receive = request.form['token_give'][8:]
    deco = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    nickname = deco['nickname']

    db.comment.insert_one({"pagecoor": pagecoor, "star": star_count, "comment": comment, "nickname": nickname})
    return jsonify({'msg': "success"})


@app.route("/api/load-comment", methods=["POST"])
def comment_get():
    title_receive = request.form['title_give']
    comment_list = list(db.comment.find({'pagecoor': title_receive}, {'_id': False}))
    return jsonify({'result': comment_list})


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    id_duplicate_check = db.user.find_one({'id': id_receive})
    nickname_duplicate_check = db.user.find_one({'nick': nickname_receive})
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    if id_duplicate_check:
        return jsonify({'result': 'id_default'})
    elif nickname_duplicate_check:
        return jsonify({'result': 'nickname_default'})
    else:
        db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})
        return jsonify({'result': 'success'})


@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})
    nickname_receive = result['nick']

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'nickname': nickname_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/show_user', methods=['POST'])
def api_showUser():
    token_receive = request.form['token_give'][8:]
    deco = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    userId = deco['id']
    user_inform = db.user.find_one({'id': userId}, {'_id': False})
    return jsonify({"result": user_inform['nick']})


if __name__ == "__main__":
    app.run('0.0.0.0', port=5500, debug=True)
