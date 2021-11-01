from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from init_db import insert_db

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjungle

@app.route('/', methods=['POST'])
def login():
        #클라이언트로부터 데이터를 받기
        id_receive = request.form['id']
        pwd_receive = request.form['pwd']
        try:
            #member_db (db_mem_id, db_mem_pwd 열에서 회원 조회)
            info_check = db.member_list.find_one({'user_id' : id_receive, 'user_pwd' : pwd_receive})
            if info_check is not None:
                print("회원체크 완료")
                return jsonify({'result': 'success', 'name': id_receive})
            else:
                print("아이디/비번 재확인")
                return jsonify({'result': 'fail', 'msg':'아이디/비밀번호 재확인해주세요.'})
        except:
            return jsonify({'result': 'fail', 'msg':'except.'})

@app.route('/memo', methods=['GET'])
def show_memo():
    # 1. mongoDB에서 _id 값 포함한 모든 데이터 조회해오기 (Read)
    result = list(db.memos.find({}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'articles': dumps(result)})


@app.route('/memo', methods=['POST'])
def post_article():
    # 1. 클라이언트로부터 데이터를 받기
    week_receive = request.form['week']
    title_receive = request.form['title']  # 클라이언트로부터 title을 받는 부분
    content_receive = request.form['content']  # 클라이언트로부터 comment를 받는 부분

    memo = {'week' : week_receive, 'title': title_receive, 'content': content_receive}

    # 3. mongoDB에 데이터를 넣기
    db.member_list.insert_one(memo)
    return jsonify({'result': 'success'})
   

@app.route('/api/delete', methods=['POST'])
def del_article():
    # 들어온 이름으로 DB에 name값의 data를 삭제한다. 
    del_id_receive = request.form['del_id']

    db.articles.delete_one({'_id': ObjectId(del_id_receive)})
    
    return jsonify({'result': 'success'})

@app.route('/api/update', methods=['POST'])
def update_article():
    update_id_receive = request.form['update_id']
    update_title_receive = request.form['update_title']
    update_comment_receive = request.form['update_comment']

    db.articles.update_one({'_id': ObjectId(update_id_receive)},{'$set':{'title':update_title_receive, 'comment': update_comment_receive}})

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
