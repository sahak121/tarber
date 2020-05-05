from flask import *
from flask_login import UserMixin, LoginManager, login_required, current_user, login_user, logout_user
#from Model.dModel import *
#from functools import wraps
import os
import requests
from flask import Flask, jsonify
from flask_sslify import SSLify
import ssl
from OpenSSL import SSL
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import random
import ast

conn = sqlite3.connect("user.db")
c = conn.cursor()

#context = SSL.Context(ssl.OP_NO_SSLv3)
#context = ssl.create_default_context()
#context.use_privatekey_file('server.key')
#context.use_certificate_file('server.crt')
context = SSL.Context(SSL.SSLv23_METHOD)
cer = os.path.join(os.path.dirname(__file__), 'resources/udara.com.crt')
key = os.path.join(os.path.dirname(__file__), 'resources/udara.com.key')
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!
login_manager = LoginManager()
sslify = SSLify(app)
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message = "Please LOG IN"
login_manager.login_message_category = "info"
quest_id = ''
name = ''
inform = ''
fb_set = 0
email_send_num = 0
new_username = ''

def query_user(username):
    user = UserAccounts.query.filter_by(UserName=username).first()
    if user:
        return True
    return False


def query_FBuser(FBuserID):
    FBuser = UserAccounts.query.filter_by(FBuserID=FBuserID).first()
    if FBuser:
        return True
    return False


@login_manager.user_loader
def user_loader(username):
    if query_user(username) or query_FBuser(username):
        user = User()
        user.id = username
        return user
    return None


@app.route('/')
@app.route('/index', methods=['GET'])
@login_required
def index():
    global new_username
    user_id = session.get('user_id')
    user = UserAccounts.query.filter_by(FBuserID=user_id).first()

    if user:
        if user.UserName == None:
            data = requests.get(
                "https://graph.facebook.com/me?fields=id,name,email&access_token=" + user.FBAccessToken)
            if data.status_code == 200:
                user.UserName = data.json()['name']
                db.session.add(user)
                db.session.commit()
                FBuser = data.json()['name']
        else:
            FBuser = user.UserName
    else:
        FBuser = ""

    return render_template("index.html", FBuser=FBuser)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global new_username
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    if request.method == 'GET':
        asd = ""
        if getsession() == "not":
            asd = 0;
        else:
            asd = getsession()
        return render_template("login.html", user=asd)

    if request.method == 'POST':
        print("YO")
        for i in range(len(c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())):
            if request.form['username'] ==  c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]:
                print("YOO")
                print(request.form['password'])
                if(request.form['password'][-1] == "!" and request.form['password'][-2] != "?" and request.form['password'][-3] == "!"):
                    print("man")
                    my_pass = list(request.form['password'])
                    my_pass.pop(-1)
                    my_back = 0
                    my_back = int(my_pass[-1])
                    my_pass.pop(-1)
                    my_pass.pop(-1)
                    print(my_pass)
                    my_fin_pass = ""
                    my_fin_pass = my_fin_pass.join(my_pass)
                    print(request.form['my_url_bc'])
                    some_val = request.form['my_url_bc']
                    if my_fin_pass ==  c.execute("SELECT * FROM " + c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]).fetchall()[0][6]:
                        new_username = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]
                        session['user'] = request.form['username']
                        print("finall")
                        return redirect("/quest?id=" + str(my_back), code=302)

                  
                elif(request.form['password'][-1] == "!" and request.form['password'][-3] == "!" and request.form['password'][-2] == "?"):
                    print("man")
                    my_pass = list(request.form['password'])
                    my_pass.pop(-1)
                    my_pass.pop(-1)
                    my_pass.pop(-1)
                    print(my_pass)
                    my_fin_pass = ""
                    my_fin_pass = my_fin_pass.join(my_pass)
                    if my_fin_pass ==  c.execute("SELECT * FROM " + c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]).fetchall()[0][6]:
                        new_username = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]
                        session['user'] = request.form['username']
                        print("finall")
                        return redirect("/noto?create=1", code=302)


                else:
                    if request.form['password'] ==  c.execute("SELECT * FROM " + c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]).fetchall()[0][6]:
                        new_username = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[i][0]
                        session['user'] = request.form['username']
                        return redirect(url_for('noto'))
    return redirect(url_for('lg_dp'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']

    return 'not'

@app.route('/valod', methods=['GET', 'POST'])
def valod():
    global break_sesion
    print(1)
    for i in range(5):
        while 'user' in session:
            print(getsession())
            session.pop('user', None)
            print(getsession())
    print(getsession())
    return getsession()

@app.route('/do_log', methods=['GET', 'POST'])
def do_log():
    print(getsession())
    while 'user' in session:
        print(getsession())
        session.pop('user', None)
        print(13)
    return "11"


@app.route('/user/<inform1>', methods=['GET', 'POST'])
def user(inform1):
    global inform
    inform = inform1
    return "11"

@app.route('/name/<name1>', methods=['POST', 'GET'])
def name(name1):
    global name
    name = name1
    check_fb()
    return "11"

@app.route('/valodik/<name11>', methods=['POST', 'GET'])
def valodik(name11):
    global name
    name = name11
    check_fb()
    return "11"

@app.route('/check_fb', methods=['GET', 'POST'])
def check_fb():
    global name
    global inform
    global fb_set
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    curr_name = ''
    user_list = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    for i in user_list:
        if i[0] == name.replace(" ", ""):
            return jsonify(c.execute("SELECT * FROM " + name.replace(" ", "")).fetchall())
            #login()
            #pass
    print("CREATE TABLE IF NOT EXISTS " + name.replace(" ", "") + " (name TEXT, surname TEXT, likes INT, posts TEXT, token TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS " + name.replace(" ", "") + " (name TEXT, surname TEXT, likes INT, posts TEXT, token TEXT)")
    c.execute('INSERT INTO ' + name.replace(" ", "") + ' VALUES("' + name.split(' ')[0] +'", "' + name.split(' ')[1] + '", "' + '0' + '", "' + '{}' + '", "' + inform.split('$')[0] + '")')
    print('vsyo')
    conn.commit()
    return jsonify(c.execute("SELECT * FROM " + name.replace(" ", "")).fetchall())
    #login()

@app.route("/main", methods=['GET', 'POST'])
def main():
    print("axxc")
    return render_template("main.html")

@app.route("/noto", methods=['GET', 'POST'])
def noto():
    if getsession() != "not":
        return render_template("noto.html")
    else:
        asd = ""
        if getsession() == "not":
            asd = 0;
        else:
            asd = getsession()
        return render_template("login.html", user=asd)        

@app.route("/lg_dp", methods=['GET', 'POST'])
def lg_dp():
    return render_template("login1.html")

@app.route("/rg_dp", methods=['GET', 'POST'])
def rg_dp():
    return render_template("regist.html")

@app.route('/emailver/<email_inform>', methods=['GET', 'POST'])
def emailver(email_inform):
    global email_send_num
    email = 'mybot7777@gmail.com'
    password = 'newdvbt2'
    subject = 'Verification'
    send_num = random.randint(10000, 99999)
    email_send_num = send_num
    email_code()
    send_to_email = email_inform.split('$')[0]
    message = "Dear " + email_inform.split('$')[1] + " your verification code is " + str(send_num)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()
    return jsonify(str(send_num))

@app.route('/email_code', methods=['GET', 'POST'])
def email_code():
    global email_send_num
    return jsonify(email_send_num)

@app.route('/user_login_info', methods=['GET', 'POST'])
def user_login_info():
    return jsonify(getsession())

@app.route('/read_notefic/<notefic_username>', methods=['GET', 'POST'])
def read_notefic(notefic_username):
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    a = ast.literal_eval(c.execute("SELECT * FROM " + notefic_username).fetchall()[0][9].strip())
    send_list = []
    l = a[1]
    for i in a[0]:

        l.append(i)
        print(i, l)
    send_list = [[], l]
    print(send_list)
    c.execute('UPDATE ' + notefic_username + ' SET note = " '  + str(send_list) +  '"')
    conn.commit()
    return "11"

@app.route('/add_new_user/<new_user_inform>', methods=['GET', 'POST'])
def add_new_user(new_user_inform):
    global new_username
    import sqlite3
    name = new_user_inform.split('|||')[0]
    surname = new_user_inform.split('|||')[1]
    email = new_user_inform.split('|||')[2]
    username = new_user_inform.split('|||')[3]
    password = new_user_inform.split('|||')[4]
    birth_dat = new_user_inform.split('|||')[5]
    gend = new_user_inform.split('|||')[6]
    print(new_user_inform.split("|||"))
    conn3 = sqlite3.connect("user.db")
    c3 = conn3.cursor()
    new_username = username
    not_list = [['Welcome dear user'], []]
    session['user'] = username
    print(getsession())
    c3.execute("CREATE TABLE IF NOT EXISTS " + username + " (name TEXT, surname TEXT, likes INT, posts TEXT, email TEXT, username TEXT, password TEXT, birth TEXT, gend TEXT, note TEXT)")
    c3.execute('INSERT INTO ' + username + ' VALUES("' + name + '", "' + surname + '", "' + '0' + '", "' + '[]' + '", "' + email + '", "' + username + '", "' + password + '" , "' + birth_dat + '" , "' + gend + '" , "' + str(not_list) +'")')
    print(getsession())
    session['user'] = username
    print(getsession())
    conn3.commit()
    return "11"

@app.route('/user_info', methods=['GET', 'POST'])
def user_info():
    global new_username
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    user_list = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    for i in user_list:
        print(getsession())
        if i[0] == getsession():
            print("gnac")
            return jsonify(c.execute("SELECT * FROM " + getsession()).fetchall(), sqlite3.connect("post.db").cursor().execute('SELECT * FROM posts').fetchall())

@app.route('/get_full_posts', methods=['GET', 'POST'])
def get_full_posts():
    return jsonify(sqlite3.connect("post.db").cursor().execute('SELECT * FROM posts').fetchall())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/book_agree/<agree_info>', methods=['GET', 'POST'])
def book_agree(agree_info):
    print(agree_info.split("|||"))
    driver = agree_info.split("|||")[0]
    not_id = agree_info.split("|||")[1]
    user = agree_info.split("|||")[2]
    want_palce = agree_info.split("|||")[3]
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    conn1 = sqlite3.connect("post.db")
    c1 = conn1.cursor()
    booked_places = c1.execute("SELECT * FROM posts WHERE id = " + str(not_id)).fetchall()[0][-5]
    booked_list =  ast.literal_eval(c1.execute("SELECT * FROM posts WHERE id = " + str(not_id)).fetchall()[0][-2].strip())
    booked_list.append(user)
    c1.execute('UPDATE posts SET goue = "' + str(booked_list) + '"' + ' WHERE id=" ' + str(not_id) + '"')
    c1.execute('UPDATE posts SET av_space = "' + str(int(want_palce) + int(booked_places)) + '" WHERE id=" ' + str(not_id) + '"')
    my_list = ast.literal_eval(c.execute("SELECT * FROM " + driver).fetchall()[0][-1].strip())
    my_list_wanter = ast.literal_eval(c.execute("SELECT * FROM " + user).fetchall()[0][-1].strip())
    my_list_wanter[0].append(driver + " accecpted your request")
    send_list = []
    print(my_list)
    for i in my_list[1]:
        print(i)
        try:
            if i.split("||||")[1] == not_id and i.split("||||")[0].split(" ")[0] == user:
                send_str = "You accecpted " + user + " request " + "||||" + not_id + "||||" + "0" 
                send_list.append(send_str)
            
            else:
                send_list.append(i)
        except:
            send_list.append(i)
    print(send_list)
    update_list = [[], send_list]
    print(update_list)
    c.execute('UPDATE ' + driver +  ' SET note="' + str(update_list) + '"')
    c.execute('UPDATE ' + user +  ' SET note="' + str(my_list_wanter) + '"')
    conn.commit()
    conn1.commit()
    return "11"
@app.route('/book_seat/<booking_info>', methods=['GET', 'POST'])
def book_seat(booking_info):
    conn = sqlite3.connect("post.db")
    c = conn.cursor()
    conn1 = sqlite3.connect("user.db")
    c1 = conn1.cursor()
    number = booking_info.split("|||")[0]
    want_seat = booking_info.split("|||")[1]
    way_id = booking_info.split("|||")[2]
    book_uname = booking_info.split("|||")[3]
    driver = booking_info.split("|||")[4]
    fromo = booking_info.split("|||")[5]
    too = booking_info.split("|||")[6]
    my_list = ast.literal_eval(c1.execute("SELECT * FROM " + driver).fetchall()[0][9].strip())
    print(my_list)
    my_mess = book_uname + ' Wants to book ' + want_seat + ' seats his number is ' + number + "  " + fromo + "-" + too + "  !" + "||||" + str(way_id) + "||||" + "1"
    my_list[0].append(my_mess)
    print(my_list)
    c1.execute('UPDATE ' + driver + ' SET note = "' + str(my_list) + '"')
    conn1.commit()
    return "11"

@app.route('/book_decil/<deciling_info>', methods=['GET', 'POST'])
def book_decil(deciling_info):
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    conn1 = sqlite3.connect("post.db")
    c1 = conn1.cursor()
    not_id = deciling_info.split("|||")[1]
    user = deciling_info.split("|||")[2]   
    driver =  deciling_info.split("|||")[0]
    my_list_wanter = ast.literal_eval(c.execute("SELECT * FROM " + user).fetchall()[0][-1].strip())
    my_list_wanter[0].append(driver + " decilind your request")
    my_list = ast.literal_eval(c.execute("SELECT * FROM " + driver).fetchall()[0][-1].strip())
    send_list = []
    print(my_list)
    for i in my_list[1]:
        print(i)
        if i.split("||||")[1] == not_id and i.split("||||")[0].split(" ")[0] == user:
            send_str = "You deciled " + user + " request " + "||||" + not_id + "||||" + "0" 
            send_list.append(send_str)
            
        else:
            send_list.append(i)
    update_list = [[], send_list]
    c.execute('UPDATE ' + driver +  ' SET note="' + str(update_list) + '"')
    c.execute('UPDATE ' + user +  ' SET note="' + str(my_list_wanter) + '"')
    conn.commit()
    conn1.commit()
@app.route("/new_quest", methods=['GET', 'POST'])
def new_quest():
    return render_template("new_quest.html")

@app.route("/quest", methods=['GET', 'POST'])
def quest():
    return render_template("quest.html")

@app.route("/sc", methods=['GET', 'POST'])
def sc():
    return render_template("search.html")

@app.route("/just_test", methods=['GET', 'POST'])
def just_test():
    session['user'] = "testmy"
    return getsession()

@app.route("/sl_ph", methods=['GET', 'POST'])
def sl_ph():
    return render_template("frame.html")

@app.route("/get_quest/<quest_info>", methods=['GET', 'POST'])
def get_quest(quest_info):
    global quest_id
    quest_id = quest_info
    return "11"

@app.route("/user_add_ph/<user_ph_info>", methods=['GET', 'POST'])
def user_add_ph(user_ph_info):
    os.system("sudo mkdir /home/pi/Flask-Login-example-master/Flask-Login-example-master/static/user_image/" + user_ph_info)
    os.system("sudo cp /home/pi/Flask-Login-example-master/Flask-Login-example-master/static/user_image/last_ph/a.png  /home/pi/Flask-Login-example-master/Flask-Login-example-master/static/user_image/" + user_ph_info)
    os.system("sudo rm /home/pi/Flask-Login-example-master/Flask-Login-example-master/static/user_image/last_ph/a.png")
    return "11"

@app.route("/send_quest", methods=['GET', 'POST'])
def send_quest():
    global quest_id
    conn = sqlite3.connect("post.db")
    c = conn.cursor()
    return jsonify(c.execute("SELECT * FROM posts WHERE id = " + quest_id).fetchall(), c.execute("SELECT * FROM posts").fetchall())

@app.route('/new_posts/<new_post_info>', methods=['GET', 'POST'])
def new_posts(new_post_info):
    conn = sqlite3.connect("user.db")
    conn1 = sqlite3.connect("post.db")
    c = conn.cursor()
    c1 = conn1.cursor()
    info = tuple(new_post_info.split('$$$'))
    print(info)
    id = str(len(c1.execute("SELECT * FROM posts").fetchall()) + 1)
    save_info = []
    my_dict = {id : {new_post_info : ()}}
    my_dict[id][new_post_info] = []
    print(my_dict)

    a = ast.literal_eval(c.execute('SELECT * FROM ' + new_post_info.split('$$$')[9]).fetchall()[0][3])
    a.append(id)
    c.execute('UPDATE ' + info[9] + ' SET posts = "' + str(a) + ' "')
    c1.execute("CREATE TABLE IF NOT EXISTS posts (id INT, fromo TEXT, too TEXT, go_time TEXT, back_time TEXT, money INT, car TEXT, free_space INT, phone TEXT, av_space INT, more_inf TEXT, driver TEXT, goue TEXT, smth TEXT)")
    c1.execute('INSERT INTO posts VALUES(  " ' + str(id) + ' ", "' + str(new_post_info.split('$$$')[0]) + '" , "' + str(new_post_info.split('$$$')[1]) + '" , "' + str(new_post_info.split('$$$')[2]) + '", "' + str(new_post_info.split('$$$')[3]) + '", "' + str(new_post_info.split('$$$')[4]) + '", "' + str(new_post_info.split('$$$')[5]) + '", "' + str(new_post_info.split('$$$')[6]) + '", "' + str(new_post_info.split('$$$')[7]) + '", "' + str(0) + '", "' + str(new_post_info.split('$$$')[8]) + '",  "' + str(new_post_info.split('$$$')[9]) + '" ,  "[]", "' + str(str(new_post_info.split('$$$')[10]) + str(new_post_info.split('$$$')[11]) + str(new_post_info.split('$$$')[12])) + '" )')
    print('INSERT INTO posts VALUES(  " ' + str(id) + ' ", "' + str(new_post_info.split('$$$')[0]) + '" , "' + str(new_post_info.split('$$$')[1]) + '" , "' + str(new_post_info.split('$$$')[2]) + '", "' + str(new_post_info.split('$$$')[3]) + '", "' + str(new_post_info.split('$$$')[4]) + '", "' + str(new_post_info.split('$$$')[5]) + '", "' + str(new_post_info.split('$$$')[6]) + '", "' + str(new_post_info.split('$$$')[7]) + '", "' + str(0) + '", "' + str(new_post_info.split('$$$')[8]) + '",  "' + str(new_post_info.split('$$$')[9]) + '" ,  "[]", ' + str(str(new_post_info.split('$$$')[10]) + str(new_post_info.split('$$$')[11]) + str(new_post_info.split('$$$')[12])) + ' )')
    conn1.commit()
    conn.commit()
    return "11"

#ssl_context=('cert.pem', 'key.pem')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,   port=1234)