from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.bfqfr.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.gukbob

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = '9VELOPMENT'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib


##############################
##          TEST            ##
##############################

# TEST 계정 생성 코드
# id = 'test1'
# pw = '1234'
# nick = 'test1'
# em = 'test1@gukbab.com'
# pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
# date_now = datetime.datetime.now()
# db.users.insert_one({'userid': id, 'password': pw_hash, 'nickname': nick, 'email': em, 'date': date_now})

print(db.users.find_one({'userid': 'test1'}))
print(db.users.find_one({'userid': 'test2'}))

################################
#  HTML을 주는 부분            ##
################################
@app.route('/')
def home():
# 현재 이용자의 컴퓨터에 저장된 cookie 에서 mytoken 을 가져옵니다.
    token_receive = request.cookies.get('mytoken')
    try:
# 암호화되어있는 token의 값을 우리가 사용할 수 있도록 디코딩(암호화 풀기)해줍니다!
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'userid': payload['userid']})
        return render_template('main.html', nickname=user_info['nickname'])
# 만약 해당 token의 로그인 시간이 만료되었다면, 아래와 같은 코드를 실행합니다.
    except jwt.ExpiredSignatureError:
        return redirect(url_for("index", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
# 만약 해당 token이 올바르게 디코딩되지 않는다면, 아래와 같은 코드를 실행합니다.
        return redirect(url_for("index", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('index.html', msg=msg) # 로그인 html 파일 생성시 주소 추가


@app.route('/signup')
def signup():
    return render_template('signup.html') # 회원가입 html 파일 생성시 주소 추가

#################################
##  로그인을 위한 API            ##
#################################

# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.users.find_one({'userid': id_receive, 'password': pw_hash})
    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=암호화 풀기)해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'userid': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [회원가입 API]
# id, pw, nick, em 을 받아서, date를 추가하여 mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/signup', methods=['POST'])
def api_signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nick_receive = request.form['nick_give']
    em_receive = request.form['em_give']
    date_now = datetime.datetime.now()

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.users.insert_one({'userid': id_receive, 'password': pw_hash, 'nickname': nick_receive, 'email': em_receive, 'date': date_now})

# 회원가입하여 계정 생성 시 프로필 테이블 생성(기본값 입력)
    basic_introduce = '안녕하세요'

    db.profiles.insert_one({'userid': id_receive, 'introduce': basic_introduce, 'pf_image': ''}) # 기본 프로필 사진 추가 구현해야됨!!!

    return jsonify({'result': 'success'})

###############################
##      아이디 중복 체크       ##
###############################
@app.route('/signup/id_check', methods=['POST'])
def id_check_dup():
    # ID 중복확인
    id_receive = request.form['id_give']
    exists = bool(db.users.find_one({'userid': id_receive}))
    # 중복 되면 True 중복 아니면 False
    return jsonify({'result': 'success', 'exists': exists})

###############################
##      닉네임 중복 체크       ##
###############################
@app.route('/sign_up/nick_check', methods=['POST'])
def nick_check_dup():
    # nick 중복확인
    nick_receive = request.form['nick_give']
    exists = bool(db.users.find_one({'nickname': nick_receive}))
    # 중복 되면 True 중복 아니면 False
    return jsonify({'result': 'success', 'exists': exists})

'''
마이페이지 접속 시 유저정보 확인하여 해당 유저 정보 찾기 (아직 미확인)
# # [유저 정보 확인 API]
# # 로그인된 유저만 call 할 수 있는 API입니다.
# # 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# # (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
# @app.route('/api/nick', methods=['GET'])
# def api_valid():
#     token_receive = request.cookies.get('mytoken')
# 
#     # try / catch 문?
#     # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.
# 
#     try:
#         # token을 시크릿키로 디코딩합니다.
#         # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
# 
#         # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
#         userinfo = db.users.find_one({'userid': payload['userid']}, {'_id': 0})
#         return jsonify({'result': 'success', 'nickname': userinfo['nickname']})
#     except jwt.ExpiredSignatureError:
#         # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
#         return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
#     except jwt.exceptions.DecodeError:
#         return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
'''

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

