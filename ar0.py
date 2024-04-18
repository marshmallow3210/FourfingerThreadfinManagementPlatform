import base64
import io
import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_cors import CORS
import pymysql
import datetime
from datetime import timezone, timedelta
import numpy as np
import requests
from sklearn.neighbors import KNeighborsRegressor

'''
you need to change the: 
databaseName: ar_DB, admin_
port
fieldName
fieldManager
contact
species
species_logo_url
users: : ar_DB, admin_
preidict_weights()
preidict_date()
'''

app = Flask(__name__)
CORS(app)  # 允許所有來源的跨來源請求
app.secret_key = '66386638'  # 替換為隨機的密鑰，用於安全性目的
connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='lab403',
                             password='66386638',
                             autocommit=True)

# change me!
databaseName = "ar0DB"
port = 5000
fieldName = "屏東張XX"
fieldManager = "張XX"
contact = "0988888888"
species = "午仔魚"
species_logo_url = "https://github.com/marshmallow3210/FourfingerThreadfinManagementPlatform/blob/main/images/IMG_1676.png?raw=true"
users = {
    'ar0DB': 'ar0DB',
    'admin0': 'admin0',
}


''' database name settings ''' 
def usernameChooseDatabaseName(username):
    global databaseName
    databaseName = ""
    if username == "fishDB" or username == "oakley" or username == "admin":
        databaseName = "fishDB"
    elif username == "ar0DB" or username == "admin0":
        databaseName = "ar0DB"
    elif username == "ar1DB" or username == "admin1":
        databaseName = "ar1DB"
    elif username == "ar2DB" or username == "admin2":
        databaseName = "ar2DB"
    elif username == "ar3DB" or username == "admin3":
        databaseName = "ar3DB"
    elif username == "ar4DB" or username == "admin4":
        databaseName = "ar4DB"
    elif username == "ar5DB" or username == "admin5":
        databaseName = "ar5DB"
    elif username == "ar6DB" or username == "admin6":
        databaseName = "ar6DB"
    elif username == "ar7DB" or username == "admin7":
        databaseName = "ar7DB"
    return databaseName

def portChoooseDatabaseName():
    if port == 8080:
        return "fishDB"
    elif port == 5000:
        return "ar0DB"
    elif port == 5010:
        return "ar1DB"
    elif port == 5020:
        return "ar2DB"
    elif port == 5030:
        return "ar3DB"
    elif port == 5040:
        return "ar4DB"
    elif port == 5050:
        return "ar5DB"
    elif port == 5060:
        return "ar6DB"
    elif port == 5070:
        return "ar7DB"


''' date format setting ''' 
def utc8(utc, p):
    for i in range(0, len(utc)):
        if utc[i][p] != None:
            utc[i] = list(utc[i])
            utc[i][p]=utc[i][p].astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")

    return utc


''' predictions and calculations ''' 
# change me!
def preidict_weights(age, total_fish_number):
    # 鱸魚
    '''
    days= 210 # 0 to 210 days
    step = 30 # interval 30 days
    phase = days//step + 1 # phase = 8
    x_set = np.array([])
    for i in range(0, 4):
        x = np.linspace(0, days, phase)
        x_set = np.append(x_set, x)
    y_set = np.array([16, 27, 66, 188, 368, 625, 856, 1077, 16, 27, 77, 208, 379, 606, 862, 1102, 16, 48, 108, 246, 425, 717, 904, 1180, 16, 42, 106, 276, 477, 754, 991, 1202])
    y_set = y_set * 800 / 1336
    '''
    # 午仔魚
    # 9 months
    date1 = datetime.date(2015,4,1)
    date2 = datetime.date(2015,12,31)
    days_count = (date2-date1).days
    x_set = np.linspace(0, days_count, 10)
    y_set = np.array([0, 2, 15, 47, 73, 81, 116, 157, 178, 193]) #, 190, 195, 199, 202, 208, 215, 230, 238, 250, 260])
    y_set = y_set * 600 / 328

    # KNN Regression
    k = 3
    knn = KNeighborsRegressor(n_neighbors=k)
    knn.fit(x_set.reshape(-1, 1), y_set)
    x_new = np.array([int(age)])
    y_pred = knn.predict(x_new.reshape(-1, 1))
    y_pred = y_pred[0]
    y_pred = y_pred * total_fish_number / 600
    print("輸入天數(天):", x_new)
    print("預估魚池總重(斤):", y_pred)
    
    return y_pred

# change me!
def preidict_date(latest_weight):
    # 午仔魚
    # 17 months, 2015/4~2016/8
    x_set = np.array([0, 2, 15, 47, 73, 81, 116, 157, 178, 193, 190, 195, 199, 202, 208, 215, 230]) #, 238, 250, 260])
    x_set = x_set * 600 / 328
    date1 = datetime.date(2015,4,1)
    date2 = datetime.date(2016,8,31)
    days_count = (date2-date1).days
    y_set = np.linspace(0, days_count, 18)
    
    # 鱸魚
    '''
    days= 210 # 0 to 210 days
    step = 30 # interval 30 days
    phase = days//step + 1 # phase = 8
    x_set = np.array([])
    for i in range(0, 4):
        x = np.linspace(0, days, phase)
        x_set = np.append(x_set, x)
    y_set = np.array([16, 27, 66, 188, 368, 625, 856, 1077, 16, 27, 77, 208, 379, 606, 862, 1102, 16, 48, 108, 246, 425, 717, 904, 1180, 16, 42, 106, 276, 477, 754, 991, 1202])
    y_set = y_set * 800 / 1336
    '''
    
    # KNN Regression
    knn = KNeighborsRegressor(n_neighbors=3)
    knn.fit(x_set.reshape(-1, 1), y_set)

    x_target = np.array([int(400.0)]) # 八兩
    y_target = knn.predict(x_target.reshape(-1, 1))
    y_target = y_target[0]

    x_new = np.array([int(latest_weight)])
    y_pred = knn.predict(x_new.reshape(-1, 1))
    y_pred = y_pred[0]
    print("魚隻重量(公克/隻):", x_new)
    print("預測剩餘天數(天):", y_target - y_pred)
    
    return y_target - y_pred

def counting_fcr(total_feeding_amount, latest_weight, first_weights):
    if total_feeding_amount == 0:
        return 0
    else:
        estimated_fcr = round(total_feeding_amount * 1000 / ((latest_weight - first_weights) * 600), 2)
        return estimated_fcr


''' root page ''' 
@app.route('/')
def test():
    data = "Hello!"
    return render_template('test.html', data=data)


''' login/logout ''' 
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            # 登入成功，將用戶名存入 session
            session['username'] = username
            user = User(1)  # Replace with your user authentication logic
            login_user(user)
            databaseName = usernameChooseDatabaseName(username)
            print('username:', username)
            print('databaseName:', databaseName)
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # 清除用戶名的 session 資料
    session.pop('username', None)
    logout_user()
    print('logout!')
    return redirect(url_for('login'))


''' homepage '''
@app.route('/home')
def home():
    # 檢查用戶是否登入，未登入則返回登入頁面
    if 'username' in session:
        update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(update_time)
        global connection
        cursor = connection.cursor()
        sql = "use " + databaseName + ";"
        cursor.execute(sql)

        sql= "select * from field_logs where DATE_FORMAT(update_time, '%Y-%m-%d') = CURDATE() limit 1; " 
        pool_data = list(cursor.fetchall()) 
        pool_data = utc8(pool_data, 6)
        if pool_data:
            pool_data = pool_data[0]
        else:
            pool_data = ["", "尚無紀錄", "尚無紀錄", "尚無紀錄", "尚無紀錄", "尚無紀錄"]

        return render_template('home.html', username=session['username'], species=species, species_logo_url=species_logo_url, 
                               fieldName=fieldName, fieldManager=fieldManager, contact=contact, pool_data=pool_data)
    else:
        return redirect(url_for('login'))


''' decision function '''
@app.route('/decision', methods=["GET", "POST"])
def decision():
    if 'username' in session:
        command = None
        if request.method == "POST":
            id = request.form.get("id")
            mode = request.form.get("mode")
            angle = request.form.get("angle")
            period = request.form.get("period")
            amount = request.form.get("amount")
            fetch_interval = request.form.get("fetch_interval")
            command = {
                'id': id, 
                'mode': mode, 
                'angle': angle, 
                'period': period, 
                'amount': amount, 
                'fetch_interval': fetch_interval
            }

        return render_template('decision.html', species=species, species_logo_url=species_logo_url)
    else:
        return redirect(url_for('login'))


''' field_view function '''
def storeFrames():
    github_image_url = "https://github.com/marshmallow3210/FourfingerThreadfinManagementPlatform/blob/main/images/output-2023-08-20-12-45-24%20-%20frame%20at%200m7s.jpg?raw=true"
    response = requests.get(github_image_url)

    if response.status_code == 200:
        image_binary = response.content
        print("Success to download the image")
    else:
        print("Failed to download the image")
    
    try:
        global connection
        cursor = connection.cursor()
        sql = "use " + databaseName + ";"
        cursor.execute(sql)

        frame_id = 3
        update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        name = "image_" + str(update_time)
        print(name)

        sql = "INSERT INTO frames (id, name, update_time, data) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (str(frame_id), name, update_time, image_binary))
        print("Success to store the image")

    except:
        print("Failed to store the image")

def connect_to_db():
    global connection
    cursor = connection.cursor()
    sql = "use " + databaseName + ";"
    cursor.execute(sql)

    global framesData
    sql = "select update_time, data from frames where ID = 1;"
    cursor.execute(sql)
    framesData = cursor.fetchone()
    return framesData

def getFrames():
    connection_cnt = 1 #0000

    while connection_cnt:
        framesData = connect_to_db()
        connection_cnt -= 1

        if framesData:
            update_time = framesData[0]
            binary_data = framesData[1]
            binary_data_btye_str = io.BytesIO(binary_data) # 將二進制數據讀取為字節串
            binary_data_base64 = base64.b64encode(binary_data_btye_str.getvalue()).decode('utf-8') # 將圖片轉換為Base64字串
            print("Get data! return base64 str")
            return update_time, binary_data_base64
        else:
            # update_time, binary_data_base64 = getFrames()
            # return '監視器畫面讀取中，請再更新一次！', ''
            yesterday_time = datetime.datetime.now() - timedelta(days=1)
            print('no framesData!', connection_cnt)

    return yesterday_time, ''

@app.route('/field_view', methods=["GET", "POST"])
def field_view():
    if 'username' in session:
        # storeFrames()
        update_time, binary_data_base64 = getFrames()
        current_time = datetime.datetime.now()
        time_difference = current_time - update_time
        time_difference = int(time_difference.total_seconds())

        if abs(time_difference) <= 10:
            update_time = update_time.strftime("%Y-%m-%d %H:%M:%S")
            return render_template('field_view.html', update_time="監視器畫面連線成功，畫面更新時間: " + update_time, binary_data_base64=binary_data_base64, species=species, species_logo_url=species_logo_url, time_difference=time_difference)
        else:
            return render_template('field_view.html', update_time="監視器畫面連線失敗，請再更新一次！", binary_data_base64='無影像畫面', species=species, species_logo_url=species_logo_url, time_difference=time_difference)
    else:
        return redirect(url_for('login'))


''' feeding_logs function '''
@app.route('/field_logs', methods=["GET", "POST"])
def field_logs():
    if 'username' in session:
        # print(request.method)
        global connection
        cursor = connection.cursor()
        sql = "use " + databaseName + ";"
        cursor.execute(sql)
        
        sql = "select * from field_logs;"
        cursor.execute(sql)
        data = list(cursor.fetchall())
        data = utc8(data, 6)
        # print(data)
        
        if request.method == "POST":
            json_data = request.get_json("data")
            pool_ID = int(json_data["pool_ID"])
            print("receive pool_ID:", pool_ID)

            if pool_ID == 0:
                sql = "select * from field_logs;"
                cursor.execute(sql)
                pool_data = list(cursor.fetchall()) 
                pool_data = utc8(pool_data, 6)
                
                sql = "select pool_ID from field_logs;"
                cursor.execute(sql)
                pool_count = cursor.fetchall() 
            else:
                sql = "select * from field_logs where pool_ID=" + str(pool_ID) +";"
                cursor.execute(sql)
                pool_data = list(cursor.fetchall()) 
                pool_data = utc8(pool_data, 6)
                
                sql = "select pool_ID from field_logs where pool_ID=" + str(pool_ID) +";"
                cursor.execute(sql)
                pool_count = cursor.fetchall()
                
            # print('POST pool_count', pool_count, 'pool_count', pool_data)
            data = {
                "pool_count": pool_count,
                "pool_data": pool_data
            }
            return data       
        else:
            sql= "select * from field_logs"
            cursor.execute(sql)
            pool_data = list(cursor.fetchall()) 
            pool_data = utc8(pool_data, 6)
            
            sql = "select pool_ID from field_logs;"
            cursor.execute(sql)
            pool_count_list = cursor.fetchall()
            pool_count = []
            [pool_count.append(x) for x in pool_count_list if x not in pool_count]
            
        return render_template('field_logs.html', pool_count=pool_count,pool_data=pool_data, data=data, species=species, species_logo_url=species_logo_url)
    else:
        return redirect(url_for('login'))
    
@app.route('/update', methods=["GET", "POST"])
def update():
    #if 'username' in session:
        isSuccess = 0
        global connection
        cursor = connection.cursor()
        sql = "use " + databaseName + ";"
        cursor.execute(sql)

        if request.method == "POST":  
            opt = int(request.form.get("opt"))
            pool_ID = request.form.get("pool_ID")
            food_ID = request.form.get("food_ID")
            spec = request.form.get("spec")
            record_weights = float(request.form.get("record_weights"))
            dead_counts = int(request.form.get("dead_counts"))
            update_time = request.form.get("update_time")
            # Parse the input string
            parsed_datetime = datetime.datetime.strptime(update_time, "%Y-%m-%dT%H:%M")
            update_time = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print("update_time:", update_time)
            
            print(f"opt: {opt}, pool_ID: {pool_ID}, food_ID: {food_ID}, spec: {spec}, record_weights: {record_weights}, dead_counts: {dead_counts}, update_time: {update_time}")
            
            # dispenser_ID = 1 # default

            if opt == 1:
                # insert food_ID into feeding_logs
                sql = "UPDATE feeding_logs SET food_ID = " + "'" + str(food_ID) + "'" + " WHERE pool_ID = "+str(pool_ID)+" order by start_time desc;"
                # sql = 'insert into feeding_logs (pool_ID, food_ID) values({}, "{}");'.format(pool_ID, food_ID)
                cursor.execute(sql)

                # insert all data into field_logs
                estimated_weights = record_weights
                fcr = 0
                sql = 'insert into field_logs (pool_ID, spec, record_weights, estimated_weights, fcr, dead_counts, update_time) values({}, {}, {}, {}, {}, {}, "{}");'.format(pool_ID, float(spec), record_weights, estimated_weights, fcr, dead_counts, update_time)
                cursor.execute(sql)
            elif opt == 2:
                # insert food_ID into feeding_logs
                sql = "UPDATE feeding_logs SET food_ID = " + "'" + str(food_ID) + "'" + " WHERE pool_ID = "+str(pool_ID)+" order by start_time desc LIMIT 1;"
                # sql = 'insert into feeding_logs (pool_ID, food_ID) values({}, "{}");'.format(pool_ID, food_ID)
                cursor.execute(sql)

                # counting total_fish_number
                sql = "select record_weights from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
                cursor.execute(sql)
                first_weights = cursor.fetchone()
                first_weights = first_weights[0]
                sql = "select spec from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
                cursor.execute(sql)
                first_spec = cursor.fetchone()
                first_spec = first_spec[0]
                total_fish_number = first_spec * first_weights
                total_fish_number = total_fish_number - dead_counts

                sql = "select dead_counts from field_logs where pool_ID = "+str(pool_ID)+";"
                cursor.execute(sql)
                dead_counts_list = list(cursor.fetchall())
                for i in range(len(dead_counts_list)):
                    total_fish_number -= dead_counts_list[i][0]
                print("total_fish_number:", total_fish_number)
                
                # counting spec
                # spec = round(total_fish_number / record_weights, 2)

                # counting estimated_weights
                sql = "select update_time from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
                cursor.execute(sql) 
                first_time = cursor.fetchone()
                first_time = first_time[0]
                update_time = datetime.datetime.strptime(update_time, "%Y-%m-%d %H:%M:%S")
                age = str((update_time - first_time).days)
                print("該魚池已養殖了:" + age + "天")
                estimated_weights = preidict_weights(age, total_fish_number)
                print('預估魚池總重(斤):', estimated_weights)
                
                # counting fcr
                sql = "select feeding_amount from feeding_logs where pool_ID = "+str(pool_ID)+";"
                cursor.execute(sql)
                feeding_amount = list(cursor.fetchall())
                total_feeding_amount = 0
                for i in range(len(feeding_amount)):
                    total_feeding_amount += feeding_amount[i][0]
                print("total_feeding_amount:", total_feeding_amount, "kg")
                fcr = counting_fcr(total_feeding_amount, estimated_weights, first_weights)
                
                # insert all data into field_logs
                spec = None
                sql = 'INSERT INTO field_logs (pool_ID, spec, record_weights, estimated_weights, fcr, dead_counts, update_time) VALUES ({}, %s, {}, {}, {}, {}, %s);'.format(pool_ID, record_weights, estimated_weights, fcr, dead_counts)
                data = (spec, update_time)
                cursor.execute(sql, data)

            else:
                # counting total_fish_number
                sql = "select record_weights from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
                cursor.execute(sql)
                first_weights = cursor.fetchone()
                first_weights = first_weights[0]
                sql = "select spec from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
                cursor.execute(sql)
                first_spec = cursor.fetchone()
                first_spec = first_spec[0]
                total_fish_number = first_spec * first_weights
                total_fish_number = total_fish_number - dead_counts

                sql = "select dead_counts from field_logs where pool_ID = "+str(pool_ID)+";"
                cursor.execute(sql)
                dead_counts_list = list(cursor.fetchall())
                for i in range(len(dead_counts_list)):
                    total_fish_number -= dead_counts_list[i][0]
                print("total_fish_number:", total_fish_number)

                # counting estimated_weights
                sql = "select update_time from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
                cursor.execute(sql) 
                first_time = cursor.fetchone()
                first_time = first_time[0]
                update_time = datetime.datetime.strptime(update_time, "%Y-%m-%d %H:%M:%S")
                age = str((update_time - first_time).days)
                print("該魚池已養殖了:" + age + "天")
                estimated_weights = preidict_weights(age, total_fish_number)
                print('estimated_weights:', estimated_weights)
                
                # counting fcr
                sql = "select feeding_amount from feeding_logs where pool_ID = "+str(pool_ID)+";"
                cursor.execute(sql)
                feeding_amount = list(cursor.fetchall())
                total_feeding_amount = 0
                for i in range(len(feeding_amount)):
                    total_feeding_amount += feeding_amount[i][0]
                print("total_feeding_amount:", total_feeding_amount, "kg") 
                fcr = counting_fcr(total_feeding_amount, record_weights, first_weights)

                # insert all data into field_logs
                sql = 'insert into field_logs (pool_ID, spec, record_weights, estimated_weights, fcr, dead_counts, update_time) values({}, {}, {}, {}, {}, {}, "{}");'.format(pool_ID, float(spec), record_weights, estimated_weights, fcr, dead_counts, update_time)
                cursor.execute(sql)
                isSuccess = 1
            return redirect(url_for("field_logs"))

        return render_template('update.html', isSuccess=isSuccess, species=species, species_logo_url=species_logo_url)
    # else:
    #     return redirect(url_for('login'))


''' feeding_logs function '''
@app.route('/feeding_logs', methods=["GET", "POST"])
def feeding_logs():
    if 'username' in session:
        global connection
        cursor = connection.cursor()
        sql = "use " + databaseName + ";"
        cursor.execute(sql)

        sql = "select * from feeding_logs"
        cursor.execute(sql)
        feeding_data = list(cursor.fetchall())

        return render_template('feeding_logs.html', feeding_data=feeding_data, species=species, species_logo_url=species_logo_url) 
    else:
        return redirect(url_for('login'))   


''' query function '''
@app.route('/query', methods=["GET", "POST"])
def query():
    if 'username' in session:
        return render_template('query.html', species=species, species_logo_url=species_logo_url)
    else:
        return redirect(url_for('login'))

@app.route('/query_result', methods=["GET", "POST"])
def query_result():
    if 'username' in session:
        global connection
        cursor = connection.cursor()
        sql = "use " + databaseName + ";"
        cursor.execute(sql)
        
        if request.method == "POST":
            pool_ID = request.form.get("pool_ID")
            print(pool_ID)
            sql = "select pool_ID from field_logs where pool_ID = "+str(pool_ID)+";"
            cursor.execute(sql)
            field_result = cursor.fetchall()

            sql = "select pool_ID from feeding_logs where pool_ID = "+str(pool_ID)+";"
            cursor.execute(sql)
            feeding_result = cursor.fetchall()
            
            if len(field_result) == 0:
                print("field_logs is empty")
                alertContent="ThisPoolhasNoFieldData!"

            elif len(feeding_result) == 0:
                print("feeding_logs is empty")
                alertContent="ThisPoolhasNoFeedingData!"

            else:
                print("Result set is not empty")
                # counting estimated_weights
                sql = "select record_weights from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
                cursor.execute(sql)
                first_weight = cursor.fetchone()
                first_weight = first_weight[0]

                sql = "select spec from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
                cursor.execute(sql)
                first_spec = cursor.fetchone()
                first_spec = first_spec[0]
                total_fish_number = first_spec * first_weight

                sql = "select estimated_weights from field_logs where pool_ID = "+str(pool_ID)+" order by update_time desc;"
                cursor.execute(sql)
                latest_weight = cursor.fetchone()
                latest_weight = latest_weight[0]

                sql = "select update_time from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
                cursor.execute(sql) 
                first_time = cursor.fetchone()
                first_time = first_time[0]
                query_time = datetime.datetime.now()
                age = str((query_time-first_time).days)
                
                # counting fcr
                sql = "select feeding_amount from feeding_logs where pool_ID = "+str(pool_ID)+";"
                cursor.execute(sql)
                feeding_amount = list(cursor.fetchall())
                total_feeding_amount = 0
                for i in range(len(feeding_amount)):
                    total_feeding_amount += feeding_amount[i][0]
                print("total_feeding_amount:", total_feeding_amount)
                estimated_fcr = counting_fcr(total_feeding_amount, latest_weight, first_weight)
                
                # counting estimated_date(上市日期) 
                remaining_date = preidict_date(latest_weight/total_fish_number) # 計算剩餘天數
                estimated_date = first_time + datetime.timedelta(days = int(remaining_date))
                print('estimated_date:', estimated_date)
            
                return render_template('query_result.html', age=int(age), estimated_date=estimated_date, estimated_weights=latest_weight, estimated_fcr=estimated_fcr, total_feeding_amount=total_feeding_amount, first_weights=first_weight, species=species, species_logo_url=species_logo_url)
        
            return render_template('query.html', alertContent=alertContent, species=species, species_logo_url=species_logo_url)
    else:
        return redirect(url_for('login'))


''' API integration'''
def convert_to_unix_timestamp(datetime_str):
    # 將日期時間字串轉換為 datetime 物件
    dt_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    # 計算 Unix timestamp（以秒為單位）
    timestamp = int(dt_obj.timestamp() * 1000)  # 乘以1000轉換為毫秒
    return timestamp

@app.route('/send_data')
def send_data():
    try:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date = convert_to_unix_timestamp(current_time)
        global connection
        cursor = connection.cursor()
        sql = "use " + databaseName + ";"
        cursor.execute(sql)

        sql = "select pool_ID, start_time, use_time, food_ID, feeding_amount from feeding_logs order by start_time desc limit 1;"
        cursor.execute(sql)
        feeding_logs = list(cursor.fetchall())
        start_time = utc8(feeding_logs, 1)
        start_time = start_time[0]
        start_time = start_time[1]
        feedingTime = convert_to_unix_timestamp(start_time)
        feeding_logs = feeding_logs[0]
        # aquarium_id = feeding_logs[0]
        period = int(feeding_logs[2])
        # food_ID = feeding_logs[3]
        weight = float(feeding_logs[4])

        # api integration
        url = 'https://api.ekoral.io/api/get_aquarium_food'
        headers = {
            'api-key': 'KuDtDcK5pLmiU57PWd5mnicVf06Fl3yn',
            'x-ekoral-memberid': '30009',
            'x-ekoral-authorization': 'Mjc2ODFhMjExZGI2MjYxNTU2NGVmN2UwNzM2YzkyOWEyMGE0NTc4OWNhNzEzZWY4Y2E2OWQxNGI5ODk5M2JhMQ==',
            'x-ekoral-authorization-nonce': 'e8e95e3d-f8a5-4a95-ab18-5b0a6b08d56c',
            'Content-Type': 'application/json'
        }

        data = {
            "parm": {
                "journal": {
                    "aquarium_id": "144",
                    "journal_id": 0,
                    "action": "create",
                    "date": date,
                    "feeding": [
                        {
                            "food": [
                                {
                                    "id": "19",
                                    "weight": weight,
                                    "unit": "catty",
                                    "name": "A牌"
                                }
                            ],
                            "feedingTime": feedingTime,
                            "period": period,
                            "status": "normal",
                            "left": "",
                            "description": "吃很久",
                            "checkedList": [
                                "19"
                            ]
                        }
                    ]
                }
            },
            "name": "configure_journal_feeding",
            "version": 1
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 如果請求不成功，引發異常

        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)})

''' choose ripple frames (send to linebot)'''
def storeRippleFrames():
    github_image_url = "https://github.com/marshmallow3210/FourfingerThreadfinManagementPlatform/blob/main/images/output-2023-08-13-13-32-47%20-%20frame%20at%200m5s.jpg?raw=true"
    response = requests.get(github_image_url)

    if response.status_code == 200:
        frame_data = response.content
        print("Success to download the image")
    else:
        print("Failed to download the image")
    
    try:
        databaseName = portChoooseDatabaseName()
        global connection
        cursor = connection.cursor()
        sql = "use " + databaseName + ";"
        cursor.execute(sql)

        frame_id = 3
        value = 126
        isChoose = False

        sql = "INSERT INTO ripple_frames (id, frame_data, value, isChoose) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (frame_id, frame_data, value, isChoose))
        connection.commit()
        cursor.close()
        print("Success to store the image")
        return
    except Exception as e:
        print("Failed to store the image:", e)

def getRippleFrames():
    databaseName = portChoooseDatabaseName()

    global connection
    cursor = connection.cursor()
    sql = "use " + databaseName + ";"
    cursor.execute(sql)

    sql = "select count(*) as row_count from ripple_frames"
    cursor.execute(sql)
    row_count = cursor.fetchone()
    row_count = row_count[0]

    if row_count:
        global ripple_frames
        ripple_frames = []
        for i in range(1, row_count+1):
            sql = "select id, frame_data, value, isChoose from ripple_frames where id = "+ str(i) +";"
            cursor.execute(sql)
            RippleFramesData = cursor.fetchone()

            if RippleFramesData:
                id = RippleFramesData[0]
                ripple_data = RippleFramesData[1]
                value = RippleFramesData[2]
                isChoose = RippleFramesData[3]
                
                ripple_data_btye_str = io.BytesIO(ripple_data) # 將二進制數據讀取為字節串
                ripple_data_base64 = base64.b64encode(ripple_data_btye_str.getvalue()).decode('utf-8') # 將圖片轉換為Base64字串

                newRippleFramesData = (id, ripple_data_base64, value, isChoose)
                print(f"Get {str(i)} ripple data!")
            ripple_frames.append(newRippleFramesData)
        return ripple_frames
    else:
        print('no ripple data!')
        return [0, '', 0, False]

@app.route('/choose_ripple_frames', methods=["GET", "POST"])
def choose_ripple_frames():
    # storeRippleFrames()
    ripple_frames = getRippleFrames()
    url = " "
    
    if request.method == "POST":  
        databaseName = portChoooseDatabaseName()
        
        global connection
        cursor = connection.cursor()
        sql = "use " + databaseName + ";"
        cursor.execute(sql)

        sql = "select count(*) as row_count from ripple_frames"
        cursor.execute(sql)
        row_count = cursor.fetchone()
        row_count = row_count[0]

        if row_count:
            for i in range(1, row_count+1):
                option_value = request.form.get("option_" + str(i))
                if option_value:
                    sql = "update ripple_frames SET isChoose = %s where id = %s;"
                    cursor.execute(sql, (1, str(i)))
                else:
                    sql = "update ripple_frames SET isChoose = %s where id = %s;"
                    cursor.execute(sql, (0, str(i)))

        connection.commit()
        ripple_frames = getRippleFrames()
        
        sql = "SELECT hub_url FROM cloud_config WHERE id=1;"
        cursor.execute(sql)
        url = cursor.fetchone()[0]

    return render_template('choose_ripple_frames.html', ripple_frames=ripple_frames, url_from_db=url)
   

''' get field data by jsgrid (not used now) '''
def load_data():
    return json.load(open('field_logs.json', encoding="utf-8"))

def write_data(data):
    json.dump(data, open('field_logs.json', 'w', encoding="utf-8"), indent=6, sort_keys=True)
    return

@app.route('/api/database', methods=['GET',])
def getdata():
    return jsonify(load_data())

@app.route('/api/database', methods=['PUT',])
def updatedata():
    data = load_data()
    for i in range(len(data)):
        if data[i].get('id') == request.json['id']:
            data[i].update(request.json)
    write_data(data)
    return jsonify(request.json)

@app.route('/api/database', methods=['POST',])
def insertdata():
    data = load_data()
    data.append({**request.json, 'id': 1+len(data)})
    write_data(data)
    return jsonify(data[-1])

@app.route('/api/database', methods=['DELETE',])
def deletedata():
    data = load_data()
    out = []
    for i in range(len(data)):
        if data[i].get('id') != int(request.form.get('id')):
            out.append(data[i])
    write_data(out)
    return jsonify(success=True)


''' get feeding data by jsgrid (not used now) '''
def load_feeding_data():
    return json.load(open('feeding_logs.json', encoding="utf-8"))

def write_feeding_data(data):
    json.dump(data, open('feeding_logs.json', 'w', encoding="utf-8"), indent=6, sort_keys=True)
    return

@app.route('/api/feedingdatabase', methods=['GET',])
def get_feeding_data():
    return jsonify(load_feeding_data())

@app.route('/api/feedingdatabase', methods=['PUT',])
def update_feeding_data():
    data = load_data()
    for i in range(len(data)):
        if data[i].get('id') == request.json['id']:
            data[i].update(request.json)
    write_feeding_data(data)
    return jsonify(request.json)

@app.route('/api/feedingdatabase', methods=['POST',])
def insert_feeding_data():
    data = load_data()
    data.append({**request.json, 'id': 1+len(data)})
    write_data(data)
    return jsonify(data[-1])

@app.route('/api/feedingdatabase', methods=['DELETE',])
def delete_feeding_data():
    data = load_feeding_data()
    out = []
    for i in range(len(data)):
        if data[i].get('id') != int(request.form.get('id')):
            out.append(data[i])
    write_feeding_data(out)
    return jsonify(success=True)


''' app settings '''
if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True # flask app 自動重新加載模板(html)
    app.jinja_env.auto_reload = True # Jinja2 自動重新加載設定
    # app.run(debug=True) # in development server
    app.run(port=port, debug=False) # in production server
