from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import csv
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


def foodImage_modelTest(model):
    mydict = {}
    with open('muchinLearning1.csv', mode='r', encoding='utf8') as inp:
        reader = csv.reader(inp)
        mydict = {rows[0]: rows[1] for rows in reader}
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    test_dir = 'static/model_food_img/'
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(224, 224),
        color_mode="rgb",
        shuffle=False,
        class_mode=None,
        batch_size=1)
    pred = model.predict(test_generator)
    # 마지막으로 업로드한 사진에 대한 판별결과를 보여줌
    # 이 부분은 어떤 서비스를 만들고자 하는지에 따라서 얼마든지 달라질 수 있음
    classes = dict((v, k) for k, v in mydict.items())
    result = classes[str(np.argmax(
        pred))]  # 결과를 onHotIncoding으로 변경 / int64 type / 해당 타입과 매칭되는 자료가 코랩에 있기 때문에 str으로 변환하여 데이서셋 좌표에서 찾기
    print(result)
    return result