from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.bfqfr.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
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

import os
from util import allowed_file, get_file_extension
UPLOAD_FOLDER = 'static/uploads'
profile_save_path = 'static/profile'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
# print(db.users.find_one({'userid': 'test1'}))
# print(db.users.find_one({'userid': 'test2'}))
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
        return redirect(url_for('main'))
# 만약 해당 token의 로그인 시간이 만료되었다면, 아래와 같은 코드를 실행합니다.
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
# 만약 해당 token이 올바르게 디코딩되지 않는다면, 아래와 같은 코드를 실행합니다.
        return redirect(url_for('login', msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('index.html', msg=msg)


@app.route('/signup')
def signup():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'userid': payload['userid']})
        return redirect(url_for('mypage', msg='마이페이지로 이동합니다.'))
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return render_template('signup.html')

@app.route('/home')
def main():
    posts = list(db.posts.find())
    comments = list(db.comments.find())
    return render_template('home.html', posts=posts, comments=comments) # 메인페이지 파일 생성 시 html 주소 수정

@app.route('/writepost')
def writepost():
    try:
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('writepost.html')  # 회원가입 html 파일 생성시 주소 추가

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))

    except jwt.exceptions.DecodeError:
    # 만약 해당 token이 올바르게 디코딩되지 않는다면, 아래와 같은 코드를 실행합니다.
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/mypage')
def mypage():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'userid': payload['userid']})
        # user_info 는 db users 에서 userid를 조회한 값
        id = user_info['userid']
        nick = user_info['nickname']
        # profiles 에서 토큰 id 값으로 검색
        profile = db.profiles.find_one({'userid': id})
        pf_image = profile['pf_image']
        introduce = profile['introduce']
        # posts 에서 토큰 id 값으로 검색
        post = list(db.posts.find({'userid': id}))
        post_cnt = len(post)

        mypage_info = [{
            'userid': id,
            'nickname': nick,
            'pf_image': pf_image,
            'introduce': introduce,
            'post': post,
            'post_cnt': post_cnt
        }]
        print(mypage_info)

        return render_template('mypage.html', mypage_info=mypage_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg="로그인 정보가 존재하지 않습니다."))

@app.route('/myfeed')
def myfeed():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'userid': payload['userid']})
        # user_info 의 id, pw 값을 변수에 저장
        id = user_info['userid']
        nick = user_info['nickname']
        # posts 콜렉션 에서 토큰 id 값으로 검색한 결과 변수에 저장
        posts = list(db.posts.find({'userid': id}))
        post_comment = []
        # posts 의 _id 값을 이용해 comments 의 post_id와 일치한 댓글 찾기
        for post in posts:
            post_id = str(post['_id'])
            comments = list(db.comments.find({'post_id': post_id}))
            # 딕셔너리변수에 post_id 를 key 로하는 comments 리스트를 저장
            p_c = {post_id: comments}
            # p_c변수를 리스트에 추가
            post_comment.append(p_c)

        myfeed_info = [{
            'userid': id,
            'nickname': nick,
        }]
        return render_template('myfeed.html', myfeed_info=myfeed_info, posts=posts, post_comment=post_comment)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg="로그인 정보가 존재하지 않습니다."))

@app.route('/profile')
def profile():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'userid': payload['userid']})
        # user_info 의 id, nick 값을 변수에 저장
        id = user_info['userid']
        nick = user_info['nickname']
        # db profiles 데이터 추출
        profiles = db.profiles.find_one({'userid': id})
        profile_image = profiles['pf_image']
        profile_introduce = profiles['introduce']

        profiles_info = {
            'userid': id,
            'nickname': nick,
            'pf_image': profile_image,
            'introduce': profile_introduce
        }

        return render_template('profile.html', profiles_info=profiles_info)

    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="로그인 시간이 만료되었습니다."))

    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg="로그인 정보가 존재하지 않습니다."))

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
    result = ''
    msg = ''
    if id_receive == '' or pw_receive == '' or nick_receive == '' or em_receive == '':
        result = 'fail'
        msg = '회원가입 정보가 정확하지 않습니다.'

    else:
        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

        db.users.insert_one({
            'userid': id_receive,
            'password': pw_hash,
            'nickname': nick_receive,
            'email': em_receive,
            'date': date_now
        })

# 회원가입하여 계정 생성 시 프로필 테이블 생성(기본값 입력)
        basic_introduce = '안녕하세요'
        pf_image = 'basic.jfif'

        db.profiles.insert_one({
            'userid': id_receive,
            'introduce': basic_introduce,
            'pf_image': pf_image
        }) # 기본 프로필 사진 추가 구현해야됨!!!

        result = 'success'
        msg = '회원가입 성공! 로그인을 해주세요!'

    return jsonify({'result': result, 'msg': msg})

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
@app.route('/signup/nick_check', methods=['POST'])
def nick_check_dup():
    # nick 중복확인
    nick_receive = request.form['nick_give']
    exists = bool(db.users.find_one({'nickname': nick_receive}))
    # 중복 되면 True 중복 아니면 False
    return jsonify({'result': 'success', 'exists': exists})



###############################
##      글 작성하기       ##
###############################
@app.route('/api/writepost', methods=['POST'])
def api_writepost():
    msg = "글 작성 성공"
    result = "fail"
    try:
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'userid': payload['userid']})
        user_id = user_info['userid']
        nickname = user_info['nickname']

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))

    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

    try:
        now = datetime.datetime.now()
        f = request.files['photo_give']

        if f and allowed_file(f.filename):
            ext = get_file_extension(f.filename)
            filename = f"file_{now.strftime('%Y%m%d%H%M%S')}.{ext}"
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        photo_receive = filename
        writing_receive = request.form['writing_give']
        tag_receive = request.form['tag_give']
        location_receive = request.form['location_give']

        doc = {
            'userid': user_id,
            'nickname': nickname,
            'photo': photo_receive,
            'writing': writing_receive,
            'tag': tag_receive,
            'location': location_receive,
            'post_date': now,
            'like_cnt': [],
        }
        insert_result = db.posts.insert_one(doc)

        if insert_result is not None:
            result = "success"
    except Exception as e:
        print(e)
        msg = "글 작성 실패"

    return jsonify({'result': result, 'msg': msg})


#########################
##      게시글 삭제       ##
#########################
@app.route('/api/myfeed/delete', methods=['POST'])
def delete_myfeed():
    post_id = ObjectId(request.form['post_id'])
    result = 'success' if db.posts.delete_one({'_id': post_id}).deleted_count == 1 else "fail"
    msg = "삭제 성공" if result == 'success' else "삭제 실패"

    return jsonify({'result': result, 'msg': msg})

###############################
##      프로필 편집 API       ##
###############################
@app.route('/profile/edit', methods=['POST'])
def profile_edit():
    token_receive = request.cookies.get('mytoken')
    profile_receive = request.form['profile_give']
    introduce_receive = request.form['introduce_give']
    now = datetime.datetime.now()
    update_result = None
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'userid': payload['userid']})
        # user_info 의 id, nick 값을 변수에 저장
        id = user_info['userid']
        nick = user_info['nickname']
        if profile_receive == 'y':
            print('profile_receive == y')
            pfile_receive = request.files['pfile_give']
            if pfile_receive and allowed_file(pfile_receive.filename):
                print('1')
                ext = get_file_extension(pfile_receive.filename)
                filename = f"file_{now.strftime('%Y%m%d%H%M%S')}.{ext}"
                pfile_receive.save(os.path.join(profile_save_path, filename))
                print('2')

                update_result = db.profiles.update_one({'userid': id}, {'$set': {'introduce': introduce_receive, 'pf_image': filename}})
                print(update_result)
        elif profile_receive == 'n':
            print('profile_receive == n')
            update_result = db.profiles.update_one({'userid': id},
                                                   {'$set': {'introduce': introduce_receive}})
            print(update_result)
        print(update_result)
        if update_result is not None:
            result = 'success'
            msg = '프로필 수정 성공.'

        else:
            result = 'fail'
            msg = '프로필 수정 실패.'

        return jsonify({'result': result, 'msg': msg})

    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="로그인 시간이 만료되었습니다."))

    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg="로그인 정보가 존재하지 않습니다."))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

