import datetime

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'jfif'])


# 허용된 이미지 확장자 판단
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 업로드 이미지 확장자 리턴
def get_file_extension(filename):
    return filename.rsplit('.', 1)[1]

# 포스트 경과 시간 계산
def elapsedTime(post_time):
    elapsed_time = datetime.datetime.now() - post_time

    m, s = divmod(elapsed_time.seconds, 60)
    h, m = divmod(m, 60)
    d = elapsed_time.days
    y, d = divmod(d, 365)

    if y > 0:
        elapsed_time = f'{y}년 전'
    elif y == 0 and d > 0:
        elapsed_time = f'{d}일 전'
    elif d == 0 and h > 0:
        elapsed_time = f'{h}시간 전'
    elif h == 0 and m > 0:
        elapsed_time = f'{m}분 전'
    elif m == 0 and s > 0:
        elapsed_time = f'방금 전'

    return elapsed_time