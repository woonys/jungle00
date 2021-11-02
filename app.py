from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
import werkzeug

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#aby2L"F4Q8z\n\xec]'

# mongodb://test:test@
client = MongoClient('localhost', 27017)
db = client.dbjungle

# Route for handling the login page logic


@app.route('/hello_flask')
def hello_flask():
    return render_template('hello_flask.html')


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
    if info_check is not None:
        print(info_check)
        session['id'] = id
        return redirect(url_for('index'))
    else:
        print("아이디/비번 재확인")
        return redirect(url_for('login'))


@app.route('/index')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()
