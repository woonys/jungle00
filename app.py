from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import bcrypt

client = MongoClient('localhost', 27017)
db = client.dbjungle

app = Flask(__name__)
app.secret_key = 'any random string'


@app.route('/logged_in')
def logged_in():
    if "user_id" in session:
        userid = session["user_id"]
        username = session["user_name"]
        # print(userid, username) 작동 완료
        return render_template('main.html', userid=userid, username=username)
    else:
        return redirect(url_for("login"))


@app.route("/phone", methods=['post'])
def check_phone_num():
    phone = request.form.get("phone")
    user_found = db.jungledb.find_one({"phone": phone})
    if user_found is not None:
        return jsonify({"result": "success"})
    else:
        return jsonify({"result": "fail"})


@app.route("/user_id", methods=['post'])
def check_id():
    user_id = request.form.get("user_id")
    user_found = db.member_list.find_one({"user_id": user_id})
    if user_found is None:
        return jsonify({"result": "success"})
    else:
        return jsonify({"result": "fail"})


@app.route("/sign_up", methods=['post', 'get'])
def sign_up():
    message = ''
    if "user_id" in session:
        return redirect(url_for("logged_in"))

    if request.method == 'GET':
        return render_template("join.html")

    if request.method == "POST":
        user_id = request.form.get("user_id")
        phone = request.form.get("phone")

        password1 = request.form.get("pwd1")
        password2 = request.form.get("pwd2")

        user_found = db.jungledb.find_one({"phone": phone})
        user_check_id = db.member_list.find_one({"user_id": user_id})
        user_name = user_found['name']
        user_phone = user_found['phone']
        # 아이디 중복 체크해서 아니면 에러 메시지 반환하는 코드 짜기

        if user_found is None:
            message = '정글 학생이 아닙니다!'
            return jsonify({'result': 'fail', 'message': message})

        if user_check_id is not None:
            message = "아이디 중복입니다!"
            print(message)
            return jsonify({'result': 'fail', 'message': message})

        if password1 != password2:
            message = '패스워드가 같지 않습니다!'
            return jsonify({'result': 'fail', 'message': message})

        # 모두 통과완료 => 회원가입 진행 (DB에 회원정보 저장)
        else:
            hashed = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
            user_input = {'user_id': user_id, 'pwd': hashed, 'user_phone': user_phone, 'user_name': user_name}
            db.member_list.insert_one(user_input)

            # return redirect(url_for('login'))
            return jsonify({'result': 'success', 'login_url': '/'})
    return render_template('join.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    #message = 'Please login to your account'
    #print(message) 완료
    if 'user_id' in session:
        return redirect(url_for("logged_in"))
    # 로그인 페이지 조회
    if request.method == 'GET':
        return render_template("login.html")

    # 로그인 요청
    if request.method == 'POST':
        # 클라이언트로부터 데이터를 받기
        #print("post 요청 성공") 완료
        id_receive = request.form['id_give']
        pwd_receive = request.form['pwd_give']
        # print("id, pwd 받음", id_receive, pwd_receive) 완료

        # member_list DB에서 사용자 조회 (db_mem_id, db_mem_pwd 열에서 회원 조회)
        info_check = db.member_list.find_one({'user_id': id_receive})
        # print(info_check) 완료 => info_check는 딕셔너리 반환
        if info_check is not None:
            #print("회원체크 완료") 작동 완료
            id_val = info_check['user_id']  # DB ID 값
            name_val = info_check['user_name']
            # DB PWD 값
            passwordcheck = info_check['pwd']
            if bcrypt.checkpw(pwd_receive.encode('utf-8'), passwordcheck):  # DB PWD/입력값 비교
                session['user_id'] = id_val  # 이름과 user_id로 세션
                session['user_name'] = name_val

                return redirect(url_for('logged_in'))

            else:
                # if session['id_receive'] in session:
                #     return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('/', message=message)

        else:
            message = 'Email not found'
            return render_template('/', message=message)
    return render_template('/', message=message)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "user_id" in session:
        print("logout")
        session.pop("user_id", None)
        return redirect(url_for("login"))
        # return jsonify({"result" : "success"})
    # else:
    #     return render_template('index.html')


####################
# 여기서부터 재운
# 2. main page

@app.route('/main')
def main():
    return render_template('main.html.bak')


# 세션에서 이름, 전화번호(식별자)를 넘겨받기
# 저장 완료!
@app.route('/save_memos', methods=['POST'])
def create_card():
    user_id = session['user_id']
    user_name = session['user_name']
    week_receive = request.form['week_give']
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    doc = {'user_id': user_id, 'user_name': user_name, 'title': title_receive, 'content': content_receive,
           'week': week_receive}

    db.member_writing.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '오늘 하루도 수고많으셨어요!'})


# 클라이언트 사이드
@app.route('/my_memos', methods=['GET'])
def list_my_cards():
    week_receive = request.args.get('week_give')
    # print(session['user_id'], week_receive)
    if week_receive == str(0):
        all_mywrts = list(db.member_writing.find({'user_id': session['user_id']}))
    else:
        all_mywrts = list(db.member_writing.find({'user_id': session['user_id'], 'week': week_receive}))

    for wrt in all_mywrts:
        wrt['_id'] = str(wrt.pop('_id'))  # mongoDB 파일 형식을 String
    #print(all_mywrts)
    return jsonify({'result': 'success', 'all_writing': all_mywrts})


@app.route('/other_memos', methods=['GET'])
def list_others_cards():
    week_receive = request.args.get('week_give')
    print(week_receive)
    print(session['user_id'])#okay
    if week_receive == str(0):
        all_othwrt = list(db.member_writing.find({}))
    else:
        all_othwrt = list(db.member_writing.find({'week': week_receive}))
    for write in all_othwrt:
        write['_id'] = str(write.pop('_id'))
        if write['user_id'] == session['user_id']:
            print(write)
            all_othwrt.remove(write)
            print(all_othwrt)
    return jsonify({'result': 'success', 'all_writing': all_othwrt})


@app.route('/update_memos', methods=['PATCH'])  # vs PUT
def update_card():
    id_receive = ObjectId(request.form['id_give'])  # string
    title_receive = request.form['title_give']
    content_receive = request.form['contents_give']
    week_receive = request.form['week_give']
    db.member_writing.update_one({'_id': id_receive},
                                 {'$set': {'title': title_receive, 'content': content_receive, 'week': week_receive}})
    return jsonify({'result': 'success', 'msg': '수정 완료'})


@app.route('/delete_memos', methods=['POST'])
def delete_card():
    id_receive = ObjectId(request.form['id_give'])
    db.member_writing.delete_one({'_id': id_receive})
    return jsonify({'result': 'success', 'msg': '제거되었습니다!'})


if __name__ == '__main__':
    app.run()