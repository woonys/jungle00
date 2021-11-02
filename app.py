from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import werkzeug

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#aby2L"F4Q8z\n\xec]'

# mongodb://test:test@
client = MongoClient('localhost', 27017)
db = client.dbjungle

# Route for handling the login page logic

#1. login page

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return session.clear()


@app.route('/login_confirm', methods=['POST'])
def login_confirm():
    id = request.form['id_']
    pwd = request.form['pw_']
    info_check = db.member_list.find_one({'id': id, 'pwd': pwd})
    usr_name = info_check['name']
    usr_phone = info_check['phone']
    #user_name = info_
    if info_check is not None:
        print(info_check)
        session['name'] = usr_name
        session['phone'] = usr_phone
        return redirect(url_for('index'))
    else:
        print("아이디/비번 재확인")
        return redirect(url_for('login'))


@app.route('/index')
def index():
    return render_template('index.html')

####################
#여기서부터 재운
#2. main page

@app.route('/main')
def main():
    return render_template('main.html')
#세션에서 이름, 전화번호(식별자)를 넘겨받기


@app.route('/memos', methods=['POST'])
def create_card():
    name = session['name']
    phone = session['phone']
    week_receive = request.form['week_give']
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    doc = {'name':name, 'phone': phone, 'title': title_receive, 'content': content_receive, 'week': week_receive}

    db.member_writing.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '오늘 하루도 수고많으셨어요!'})

@app.route('/memos', methods=['GET'])
def list_my_cards():
    week_receive = request.form['week_give']
    all_mywrts = list(db.member_writing.find({'phone': session['phone'], 'week': week_receive}))
    for wrt in all_mywrts:
        wrt['id'] = str(wrt.pop('_id'))
    return jsonify({'result': 'success', 'all_writing': all_mywrt})

@app.route('/memos', methods=['GET'])
def list_others_cards():
    week_receive = request.form['week_give']
    all_othwrt = list(db.member_writing.find({'week': week_receive}))
    for write in all_othwrt:
        if write['phone'] == session['phone']:
            all_othwrt.remove(write)
    return jsonify({'result': 'success', 'all_writing': all_othwrt})


@app.route('/memos', methods=['PATCH'])  # vs PUT
def update_card():
    id_receive = ObjectId(request.form['id_give']) #string
    title_receive = request.form['title_give']
    content_receive = request.form['contents_give']
    week_receive = request.form['week_give']

    db.exam.update_one({'_id': id_receive}, {'$set': {'title': title_receive, 'content': content_receive, 'week': week_receive}})
    return jsonify({'result': 'success', 'msg': '수정 완료'})

@app.route('/memos/{id:str}', methods=['DELETE'])
def delete_card():
    id_receive = ObjectId(request.form['id_give'])
    db.member_writing.delete_one({'_id': id_receive})
    return jsonify({'result': 'success', 'msg': '제거되었습니다!'})

if __name__ == '__main__':
    app.run()
