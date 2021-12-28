from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.55kei.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


# 테스트용 입니다. 클론 후 삭제 해 주세요.
@app.route('/connection')
def connection_check():
    people = list(db.users.find({}, {'_id': False}))
    print(people)
    return jsonify({'people': people})
# 테스트용 입니다. 클론 후 삭제 해 주세요.


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
