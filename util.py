ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# 허용된 이미지 확장자 판단
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 업로드 이미지 확장자 리턴
def get_file_extension(filename):
    return filename.rsplit('.', 1)[1]