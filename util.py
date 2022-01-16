from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import csv
import datetime
from PIL import Image
import tensorflow as tf
import base64


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


def foodImage_modelPredict(model):
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


def numberImage_modelPredict(model):
    mydict = {}
    with open('static/model/numberModel_location.csv', mode='r', encoding='utf8') as inp:
        reader = csv.reader(inp)
        mydict = {rows[0]: rows[1] for rows in reader}
    print(1, mydict)
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    print(2, test_datagen)
    test_dir = 'static/model_num_img/'
    print(3, test_dir)
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(28, 28),
        color_mode="grayscale",
        shuffle=False,
        class_mode=None,
        batch_size=1)
    print(4, test_generator.shape)
    print(4, test_generator)
    pred = model.predict(test_generator)
    print(5, pred)
    # 마지막으로 업로드한 사진에 대한 판별결과를 보여줌
    # 이 부분은 어떤 서비스를 만들고자 하는지에 따라서 얼마든지 달라질 수 있음
    classes = dict((v, k) for k, v in mydict.items())
    result = classes[str(np.argmax(
        pred))]  # 결과를 onHotIncoding으로 변경 / int64 type / 해당 타입과 매칭되는 자료가 코랩에 있기 때문에 str으로 변환하여 데이서셋 좌표에서 찾기
    print(result)
    return result


def guess_what_digit_it_is(user_image_base64):
    # 1. 사용자가 전달한 이미지 저장
    imgdata = base64.b64decode(user_image_base64)  # base64 string -> binary로 디코딩한다
    filename = 'static/testbed/user_draw_image.jpg'  # 이미지 저장 경로 및 파일명 설정
    with open(filename, 'wb') as f:
        f.write(imgdata)  # 설정한 경로에 이미지 파일을 쓴다(저장)

    # 2. 사용자가 그린 이미지를 테스트셋으로 가공
    img = Image.open('static/testbed/user_draw_image.jpg')
    rgb_im = img.convert('RGB')  # rgb로 모드 설정
    img_resize = rgb_im.resize((28, 28))  # 크기 28 x 28 리사이즈
    img_resize_path = 'static/testbed/user_draw_image_resize.jpg'  # 리사이즈 파일 경로 설정
    img_resize.save(img_resize_path)  # 지정경로에 저장

    img_file = Image.open(img_resize_path)  # PIL 이미지로 파일 열기

    # Make image Greyscale
    img_grey = img_file.convert('L')  # grayscale 모드 설정

    # Save Greyscale values
    value = np.asarray(img_grey.getdata(), dtype=np.int).reshape(28, 28)  # 이미지 픽셀값 numpy array 28*28로 저장
    value = value.flatten()  # 28 * 28 -> 한 row로 변경

    with open("static/testbed/img_pixels.csv", 'w') as f:  # csv파일로 저장
        writer = csv.writer(f)
        writer.writerow(value)

    # 3. 모델로 예측
    model = tf.keras.models.load_model('static/model/single_number_model.h5')  # 모델 로드
    csv_file = 'static/testbed/img_pixels.csv'
    data = np.genfromtxt(csv_file, delimiter=',')  # csv파일 내용을 numpy array로 넣어줌
    data = np.array([data])  # 2차 array로 만들어 줌
    data = data / 255.  # 각 pixel값이 0~1값 갖도록

    pred = model.predict(data)  # 예측한다
    # 예) pred 결과값
    # [[3.4968239e-06 4.9684513e-07 1.8553355e-07 9.9596691e-01 3.2290333e-07
    # 7.4722834e-07 3.3085087e-11 2.5017182e-14 3.2954663e-03 7.3243584e-04]]

    max_acc = max(pred[0]).item()  # 가장 높은 값을 찾는다 (정확도)
    predict_num = np.argmax(pred).item()  # 가장 높은 값의 인덱스 리턴
    return max_acc, predict_num
