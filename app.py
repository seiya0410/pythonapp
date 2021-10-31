from flask import Flask, redirect, url_for, session
from flask import render_template, request
#from werkzeug.utils import import_string
import os, json, datetime
import bbs_login # login module
import bbs_data # data module

#flask instance and key
app = Flask(__name__)
app.secret_key = 'U1qwerasdf'

# the main page of bbs
@app.route('/')
def index():
    #check login
    if not bbs_login.is_login():
        return redirect('/login')
    #show log
    return render_template('index.html',
            user=bbs_login.get_user(),
            data=bbs_data.load_data())

#show login page
@app.route('/login')
def login():
    return render_template('login.html')
    
#login process
@app.route('/try_login', methods=['POST'])
def try_login():
    user = request.form.get('user', '')
    pw = request.form.get('pw', '')
    # redirect to /
    if bbs_login.try_login(user, pw):
        return redirect('/')
        #fail login
    return show_msg('ログインに失敗しました')

@app.route ('/logout')
def logout():
    bbs_login.try_logout()
    return show_msg('ログアウトしました')


#write the log
@app.route('/write', methods=['POST'])
def write():
    #need to login
    if not bbs_login.is_login():
        return redirect('/login')
   #get the text
    ta = request.form.get('ta', '')
    if ta == '': 
        return show_msg('あたいがからです')

    #add data
    bbs_data.save_data_append(
        user=bbs_login.get_user(),
        text=ta
    )
    return redirect('/')

   #retrive the msg
def show_msg(msg):
    return render_template('msg.html', msg=msg)

if __name__ == '__main__':
   app.run(debug=True, host='192.168.1.6')