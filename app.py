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

#reload를 위해 module을 사용합니다.
from importlib import reload

import os

from util import allowed_file, get_file_extension, elapsedTime, numberImage_modelPredict, foodImage_modelPredict, \
    guess_what_digit_it_is

UPLOAD_FOLDER = 'static/uploads'
profile_save_path = 'static/profile'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import tensorflow as tf
print('현재 위치: ' + os.getcwd())
model_food = tf.keras.models.load_model('static/model/sample_ResNet50_model.h5') # 모델 로딩시간 있음


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
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        dbposts = list(db.posts.find())
        comments = list(db.comments.find())
        profiles = list(db.profiles.find())

        posts = []
        for post in dbposts:
            post_time = post['post_date']
            elapsed_time = elapsedTime(post_time)

            post['elapsed_time'] = elapsed_time
            posts.append(post)
        return render_template('home.html', posts=posts, comments=comments, profiles=profiles, my_id=payload['userid'])
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg="로그인 정보가 존재하지 않습니다."))

@app.route('/home/scrap', methods=['POST'])
def scrap_home():
    result = 'success'
    try:
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # jwt토큰으로부터 사용자 id 얻음
        user_id = payload['userid']

        # 클라이언트로부터 스크랩 유/무, post id 얻음
        scrap_receive = request.form['scrap_give'] # 1: 좋아요 0: 좋아요 해제
        post_id_receive = ObjectId(request.form['post_id_give'])
        user_info = db.users.find_one({'userid': user_id})
        # user_info 는 db users 에서 userid를 조회한 값

        #scrap이 1로 바뀌면 DB에 값을 저장한다
        user_id = user_info['userid']
        if scrap_receive == 1:
            doc = {
                'userid': user_id,
                'post_id': post_id_receive,
            }
            db.scraps.insert_one(doc)

        return jsonify({'result': 'success'})

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
    # 만약 해당 token이 올바르게 디코딩되지 않는다면, 아래와 같은 코드를 실행합니다.
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
    except Exception as e:
        print(e)
        return jsonify({'result': 'fail'})



@app.route('/writepost', methods=['POST'])
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






@app.route('/comment', methods=['POST'])
def comment():
    post_id_receive = request.form['post_id_give']
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'userid': payload['userid']})

        comments = list(db.comments.find({'post_id': post_id_receive}))
        for comment in comments :
            comment['_id']= str(comment['_id'])

        return jsonify({'result': 'success', 'comments': comments, 'nickname': user_info['nickname']})
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg="로그인 정보가 존재하지 않습니다."))
    except Exception as e:
        print(e)
        return jsonify({'result': 'fail'})




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
        posts = list(db.posts.find({'userid': id}))
        post_cnt = len(posts)

        post = []
        for p in posts:
            post_time = p['post_date']
            elapsed_time = elapsedTime(post_time)

            p['elapsed_time'] = elapsed_time
            post.append(p)

        scrap_posts = list(db.scraps.find({'user_id': id}))
        scrap_postid = scrap_posts['post_id']
        #for문으로 하나씩 넣어주고 append하기
        scrap_post_zip = []
        for scrappost in scrap_postid :
            scrapposts = list(db.posts.find({'post_id': scrappost}))
            scrap_post_zip.append(scrapposts)


        mypage_info = [{
            'userid': id,
            'nickname': nick,
            'pf_image': pf_image,
            'introduce': introduce,
            'post': post,
            'post_cnt': post_cnt
        }]

        return render_template('mypage.html', mypage_info=mypage_info, scrap_post_zip=scrap_post_zip)
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

        post = []
        for p in posts:
            post_time = p['post_date']
            elapsed_time = elapsedTime(post_time)

            p['elapsed_time'] = elapsed_time
            post.append(p)

        profiles = db.profiles.find_one({'userid': id})
        pf_image = profiles['pf_image']

        myfeed_info = [{
            'userid': id,
            'nickname': nick,
            'pf_image': pf_image
        }]
        return render_template('myfeed.html', myfeed_info=myfeed_info, posts=post, post_comment=post_comment)
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


@app.route('/mypostedit')
def mypostedit_page():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userid = payload['userid']
        post_id = ObjectId(request.args.get("pi"))
        post = list(db.posts.find({'_id': post_id, 'userid': userid}))

        return render_template('mypostedit.html', post=post)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg="로그인 정보가 존재하지 않습니다."))
    except Exception as e:
        print(e)
        return redirect(url_for('myfeed', msg="[오류] 글 수정 페이지를 열 수 없습니다."))

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

####################################
##       회원가입 사람/봇           ##
####################################

# @app.route('/api/captcha', methods=['POST'])
# def api_signup():
#     user_digit_receive = request.form['user_digit_give']
#     if user_digit_receive != sth:
#         result = 'fail'
#
#     else :
#         result = 'success'
#
#     return jsonify({'result': result})


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

###############################
##      자동태그추천       ##
###############################

@app.route('/api/autotag', methods=['POST'])
def api_autotag():
    file = request.form['file_give']
    # 해당 파일에서 확장자명만 추출
    extension = file.filename.split('.')[-1]
    # 파일 이름이 중복되면 안되므로, 지금 시간을 해당 파일 이름으로 만들어서 중복이 되지 않게 함!
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{mytime}'
    # 파일 저장 경로 설정 (파일은 서버 컴퓨터 자체에 저장됨)
    save_to = f'static/model_food_img/food/{filename}.{extension}'
    # 파일 저장!
    file.save(save_to)
    tag = foodImage_modelTest(model_food)  # 여기서 이미지 검증 함수 호출!!
    os.remove(save_to)
    result = 'success'
    return jsonify({'result':result, 'tag':tag})

###############################
##      댓글작성       ##
###############################
@app.route('/api/comment', methods=['POST'])
def api_comment():
    msg = "글 작성 성공"
    result = "fail"
    try:
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'userid': payload['userid']})
        # user_info 의 id, pw 값을 변수에 저장
        id = user_info['userid']
        nick = user_info['nickname']
        now = datetime.datetime.now()
        comment_receive = request.form['comment_give']
        post_id_receive = request.form['post_id_give']
        cmd_date = now



        db.comments.insert_one({
            'post_id': post_id_receive,
            'nickname': nick,
            'comment': comment_receive,
            'userid': id,
            'cmd_date': cmd_date
        })


        comments = list(db.comments.find({'post_id': post_id_receive}))
        for comment in comments:
            comment['_id'] = str(comment['_id'])
            # db.comments.update_one({'post_id': post_id_receive, 'cmd_date':cmd_date}, {'$set': {'comment_id': comment_id}})



        result = 'success'


        return jsonify({'result': result, 'msg': msg, 'nickname': nick})
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg="로그인 정보가 존재하지 않습니다."))

#########################
##      댓글 삭제      ##
#########################
@app.route('/api/comment/delete', methods=['POST'])
def delete_mycomment():
    comment_id = ObjectId(request.form['comment_id_give'])
    result = 'success' if db.comments.delete_one({'_id': comment_id}).deleted_count == 1 else "fail"
    msg = "삭제 성공" if result == 'success' else "삭제 실패"

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
            pfile_receive = request.files['pfile_give']
            if pfile_receive and allowed_file(pfile_receive.filename):
                ext = get_file_extension(pfile_receive.filename)
                filename = f"file_{now.strftime('%Y%m%d%H%M%S')}.{ext}"
                pfile_receive.save(os.path.join(profile_save_path, filename))

                update_result = db.profiles.update_one({'userid': id}, {'$set': {'introduce': introduce_receive, 'pf_image': filename}})
        elif profile_receive == 'n':
            update_result = db.profiles.update_one({'userid': id},
                                                   {'$set': {'introduce': introduce_receive}})
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


#########################
##      게시글 수정       ##
#########################
@app.route('/api/mypostedit', methods=['POST'])
def api_mypostedit():
    msg = "게시글 수정 실패"
    result = "fail"
    try:
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['userid']

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))

    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

    try:
        post_id_receive = ObjectId(request.form['post_id_give'])
        writing_receive = request.form['writing_give']
        tag_receive = request.form['tag_give']
        location_receive = request.form['location_give']

        doc = {
            'writing': writing_receive,
            'tag': tag_receive,
            'location': location_receive,
        }
        update_result = db.posts.update_one({'_id': post_id_receive, 'userid': user_id}, {'$set': doc})

        if update_result.modified_count == 1:
            result = "success"
            msg = "게시글 수정 성공"

    except Exception as e:
        print(e)

    return jsonify({'result': result, 'msg': msg})



#########################
##      좋아요 수정       ##
#########################
@app.route('/api/like', methods=['POST'])
def process_heart():
    msg = "좋아요 수정 실패"
    result = "fail"
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # jwt토큰으로부터 사용자 id 얻음
        user_id = payload['userid']

        # 클라이언트로부터 좋아요 유/무, post id 얻음
        like_receive = request.form['like_give'] # 1:좋아요, 0:좋아요 해제
        post_id_receive = ObjectId(request.form['post_id_give'])

        # 해당 포스트의 '좋아요 유저'를 db로부터 받아 리스트에 담음
        post = list(db.posts.find({'_id': post_id_receive}))
        like_list = post[0]['like_cnt']

        # '좋아요 유/무'에 따라 '좋아요 유저리스트'에서 '좋아요 누른 유저'를 추가 or 삭제
        like_list.append(user_id) if like_receive == '1' else like_list.remove(user_id)
        doc = {
            'like_cnt': like_list
        }

        # 변경된 '좋아요 유저 리스트'를 해당 포스트에 db 업데이트 한다
        update_result = db.posts.update_one({'_id': post_id_receive}, {'$set': doc})

        # 업데이트가 잘 완료되면 응답해 줄 값들을 정함
        if update_result.modified_count == 1:
            result = "success"
            msg = "좋아요 수정 성공"

        # 클라이언트로 응답
        return jsonify({'result':result, 'msg':msg})
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg="로그인 정보가 존재하지 않습니다."))
    except Exception as e:
        print(e)
        return jsonify({'result':result, 'msg':msg})


#######################################################
##      제시한 이미지와 모델이 예측한 수가 일치하는지 판별       ##
#######################################################
@app.route('/api/digit', methods=['POST'])
def check_digit():
    result = 'fail' # 결과 기본값 설정
    try:
        answer = int(request.form['answer_digit_give']) # 이미지 정답
        user_image_base64 = request.form['user_digit_give'].rsplit(',')[1] # 사용자가 그린 이미지의 base64 string만 남긴다

        max_acc, predict_num = guess_what_digit_it_is(user_image_base64) # 모델이 추측한 숫자와 정확도를 리턴
        print(max_acc, predict_num)

        if predict_num == answer: # 제시한 수와 모델 예측 수가 일치한다면
            result = 'success'
        return jsonify({'result': result, 'acc': max_acc})
    except Exception as e:
        print(e)
        return jsonify({'result':'error'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

