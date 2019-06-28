import os
from flask import Flask
from flask import request
from flask import send_file,render_template

basedir = os.path.abspath(os.path.dirname(__file__))
static_dir = os.path.join(basedir,'static')

app = Flask(__name__)
app.debug=True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/music',methods=['GET','POST'])
def getJson():
    return "{'name':'Tom','age':20,'addr':'taian'}"

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'


@app.route('/data/call_me_al.json')
def get_json_1():
    data_dir = os.path.join(static_dir,'data')
    return send_file(os.path.join(data_dir,'call_me_al.json'))

@app.route('/data/helplessness_blues.json')
def get_json_2():
    data_dir = os.path.join(static_dir,'data')
    return send_file(os.path.join(data_dir,'helplessness_blues.json'))

@app.route('/data/jolene.json')
def get_json_3():
    data_dir = os.path.join(static_dir,'data')
    return send_file(os.path.join(data_dir,'jolene.json'))

@app.route('/data/poker_face.json')
def get_json_4():
    data_dir = os.path.join(static_dir,'data')
    return send_file(os.path.join(data_dir,'poker_face.json'))

@app.route('/data/she_said.json')
def get_json_5():
    data_dir = os.path.join(static_dir,'data')
    return send_file(os.path.join(data_dir,'she_said.json'))

@app.route('/data/short_skirt.json')
def get_json_6():
    data_dir = os.path.join(static_dir,'data')
    return send_file(os.path.join(data_dir,'short_skirt.json'))

@app.route('/data/sledgehammer.json')
def get_json_7():
    data_dir = os.path.join(static_dir,'data')
    return send_file(os.path.join(data_dir,'sledgehammer.json'))

@app.route('/data/sledgehammer_2_rounds.json')
def get_json_8():
    data_dir = os.path.join(static_dir,'data')
    return send_file(os.path.join(data_dir,'sledgehammer_2_rounds.json'))

@app.route('/data/songs.json')
def get_json_9():
    data_dir = os.path.join(static_dir,'data')
    return send_file(os.path.join(data_dir,'songs.json'))

if __name__ == '__main__':
    app.run(port = 8000)