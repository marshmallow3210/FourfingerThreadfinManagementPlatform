import base64
from collections import defaultdict
import hashlib
import hmac
import io
import json
import math
import pandas as pd
import uuid
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from matplotlib import patches, pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_cors import CORS
import pymysql
import datetime
from datetime import timezone, timedelta
import numpy as np
import requests
from scipy import stats
from sklearn.neighbors import KNeighborsRegressor
from datetime import timedelta
from scipy.signal import medfilt

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
databaseName = "ar3DB"
port = 5030
fieldName = "嘉義鍾XX"
fieldManager = "鍾XX"
contact = "0988776655"
species = "鱸魚"
species_logo_url = "https://github.com/marshmallow3210/FourfingerThreadfinManagementPlatform/blob/main/images/IMG_1676.png?raw=true"
users = {
    'ar3DB': 'ar3DB',
    'admin3': 'admin3',
}
aquarium_id = "82"


def reconnect_to_mysql():
    print("reconnect to mysql...")
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='lab403',
                                 password='66386638',
                                 database=databaseName,
                                 autocommit=True)
    print("connected!")
    return connection


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
    elif port == 5666:
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
    days= 210 # 0 to 210 days
    step = 30 # interval 30 days
    phase = days//step + 1 # phase = 8
    x_set = np.array([])
    for i in range(0, 4):
        x = np.linspace(0, days, phase)
        x_set = np.append(x_set, x)
    y_set = np.array([16, 27, 66, 188, 368, 625, 856, 1077, 16, 27, 77, 208, 379, 606, 862, 1102, 16, 48, 108, 246, 425, 717, 904, 1180, 16, 42, 106, 276, 477, 754, 991, 1202])
    y_set = y_set * 800 / 1336
    
    # 午仔魚
    # 9 months
    '''
    date1 = datetime.date(2015,4,1)
    date2 = datetime.date(2015,12,31)
    days_count = (date2-date1).days
    x_set = np.linspace(0, days_count, 10)
    y_set = np.array([0, 2, 15, 47, 73, 81, 116, 157, 178, 193]) #, 190, 195, 199, 202, 208, 215, 230, 238, 250, 260])
    y_set = y_set * 600 / 328
    '''

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
    '''
    x_set = np.array([0, 2, 15, 47, 73, 81, 116, 157, 178, 193, 190, 195, 199, 202, 208, 215, 230, 238]) #, 250, 260])
    x_set = x_set * 600 / 328
    date1 = datetime.date(2015,4,1)
    date2 = datetime.date(2016,8,31)
    days_count = (date2-date1).days
    y_set = np.linspace(0, days_count, 18)
    '''

    # 鱸魚
    days= 210 # 0 to 210 days
    step = 30 # interval 30 days
    phase = days//step + 1 # phase = 8
    x_set = np.array([])
    for i in range(0, 4):
        x = np.linspace(0, days, phase)
        x_set = np.append(x_set, x)
    y_set = np.array([16, 27, 66, 188, 368, 625, 856, 1077, 16, 27, 77, 208, 379, 606, 862, 1102, 16, 48, 108, 246, 425, 717, 904, 1180, 16, 42, 106, 276, 477, 754, 991, 1202])
    y_set = y_set * 800 / 1336
    
    print("x_set 的長度:", len(x_set))
    print("y_set 的長度:", len(y_set))

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


''' API integration'''
def convert_to_unix_timestamp(datetime_str):
    dt_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    timestamp = int(dt_obj.timestamp() * 1000) # 計算 Unix timestamp (以秒為單位 = 毫秒*1000)
    return timestamp

def generate_signature(api_key, api_endpoint, request_body, nonce):
    message = api_key + api_endpoint + request_body + nonce # according to API Authentication from API key document
    signature = hmac.new(bytes(api_key,'utf-8'), bytes(message,'utf-8'), hashlib.sha256).hexdigest().encode('utf-8')
    return base64.b64encode(signature).decode('utf-8')

# update data version
def send_data(journal_id1, journal_id2):
    print("\nstart to sending data")
    isSent = False
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('current_time:', current_time)
    date = convert_to_unix_timestamp(current_time)
    
    # get data from database
    global connection
    cursor = connection.cursor()
    for journal_id in range(journal_id1, journal_id2+1): 
        sql = f"select journal_id from {databaseName}.new_feeding_logs;"
        cursor.execute(sql)
        journal_ids = cursor.fetchall()

        if journal_id not in [row[0] for row in journal_ids]:
            print(f"journal_id({journal_id}) is not in journal_ids")
            continue
        else:
            sql = f"select journal_id, pool_id, start_time, use_time, food_id, food_name, food_unit, feeding_amount, left_amount, status, description from {databaseName}.new_feeding_logs where journal_id={journal_id} limit 1;"
            cursor.execute(sql)
            feeding_logs = list(cursor.fetchall())
            print('feeding_logs:', feeding_logs)
                    
            action = "update"                              

            food_id = str(feeding_logs[0][4]) 
            feeding_amount = str(feeding_logs[0][7])        
            food_unit = str(feeding_logs[0][6])             
            food_name = str(feeding_logs[0][5])         

            start_time = utc8(feeding_logs, 2) 
            start_time = start_time[0]
            start_time = start_time[2]
            start_time = convert_to_unix_timestamp(start_time) 
            
            use_time = int(feeding_logs[0][3])
            status = str(feeding_logs[0][9]).strip() if feeding_logs[0][9] is not None else "normal"
            left_amount = str(feeding_logs[0][8])           
            description = str(feeding_logs[0][10]).strip() if feeding_logs[0][10] is not None else ""  
            
            # params from ekoral
            url = 'https://api.ekoral.io' 
            api_key = 'WSGS4kmccIGadre9Cr3PgksaUeR4umR1' 
            api_endpoint = '/api/configure_journal_feeding' 
            member_id = '30095' 
            data = {
                "parm": {
                    "journal": {
                    "aquarium_id": aquarium_id,
                    "journal_id": journal_id,
                    "action": action,
                    "date": date,
                    "feeding": [
                        {
                        "food": [
                            {
                            "id": food_id,
                            "weight": feeding_amount,
                            "unit": food_unit,
                            "name": food_name
                            }
                        ],
                        "feedingTime": start_time,
                        "period": use_time,
                        "status": status,
                        "left": left_amount,
                        "description": description
                        }
                    ]
                    }
                }
            }
            
            print("data:", data)
            
            request_body = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
            nonce = str(uuid.uuid4()) # 動態生成 nonce  
            signature = generate_signature(api_key, api_endpoint, request_body, nonce)
            
            headers = {
                'x-ekoral-memberid': member_id,
                'x-ekoral-authorization': signature,
                'x-ekoral-authorization-nonce': nonce,
                'Content-Type': 'application/json'
            }

            try:
                response = requests.post(url + api_endpoint, headers=headers, json=data)
                response.raise_for_status()  # Raises an exception for non-2xx status codes

                if response.status_code == 200:
                    print("Request successful!")
                    print("Response:", response.json())
                    isSent = True
                else:
                    print("Unexpected status code:", response.status_code)
                    print("Response:", response.text)
            except requests.exceptions.RequestException as e:
                print("Request failed:", e)

    return isSent


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
        sql = f"USE {databaseName};"
        try:
            cursor.execute(sql)
        except pymysql.err.OperationalError as e:
            print(f"OperationalError: {e}")
            connection = reconnect_to_mysql() 
            cursor = connection.cursor()
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
    sql = f"USE {databaseName};"
    try:
        cursor.execute(sql)
    except pymysql.err.OperationalError as e:
        print(f"OperationalError: {e}")
        connection = reconnect_to_mysql() 
        cursor = connection.cursor()
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


''' field_logs function '''
@app.route('/field_logs', methods=["GET", "POST"])
def field_logs():
    if 'username' in session:
        global connection
        cursor = connection.cursor()
        sql = f"USE {databaseName};"
        try:
            cursor.execute(sql)
        except pymysql.err.OperationalError as e:
            print(f"OperationalError: {e}")
            connection = reconnect_to_mysql() 
            cursor = connection.cursor()
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
        sql = f"USE {databaseName};"
        try:
            cursor.execute(sql)
        except pymysql.err.OperationalError as e:
            print(f"OperationalError: {e}")
            connection = reconnect_to_mysql() 
            cursor = connection.cursor()
            cursor.execute(sql)

        if request.method == "POST":  
            opt = int(request.form.get("opt"))
            pool_ID = request.form.get("pool_ID")
            food_ID = request.form.get("food_ID")
            spec = float(request.form.get("spec"))
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
                first_weights = first_weights[0] if first_weights else record_weights
                sql = "select spec from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
                cursor.execute(sql)
                first_spec = cursor.fetchone()
                first_spec = first_spec[0] if first_spec else 0
                total_fish_number = first_spec * first_weights
                total_fish_number = total_fish_number - dead_counts

                sql = "select dead_counts from field_logs where pool_ID = "+str(pool_ID)+";"
                cursor.execute(sql)
                dead_counts_list = list(cursor.fetchall())
                if dead_counts_list:
                    for i in range(len(dead_counts_list)):
                        total_fish_number -= dead_counts_list[i][0]
                print("total_fish_number:", total_fish_number)
                
                # counting spec
                # spec = round(total_fish_number / record_weights, 2)

                # counting estimated_weights
                sql = "select update_time from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
                cursor.execute(sql) 
                first_time = cursor.fetchone()
                first_time = first_time[0] if first_time else update_time
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
                first_weights = first_weights[0] if first_weights else record_weights
                sql = "select spec from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
                cursor.execute(sql)
                first_spec = cursor.fetchone()
                first_spec = first_spec[0] if first_spec else spec
                total_fish_number = first_spec * first_weights
                total_fish_number = total_fish_number - dead_counts

                sql = "select dead_counts from field_logs where pool_ID = "+str(pool_ID)+";"
                cursor.execute(sql)
                dead_counts_list = list(cursor.fetchall())
                if dead_counts_list:
                    for i in range(len(dead_counts_list)):
                        total_fish_number -= dead_counts_list[i][0]
                print("total_fish_number:", total_fish_number)

                # counting estimated_weights
                sql = "select update_time from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
                cursor.execute(sql) 
                first_time = cursor.fetchone()
                first_time = first_time[0] if first_time else update_time
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
    isSent = False
    if 'username' in session:
        global connection
        cursor = connection.cursor()
        sql = f"USE {databaseName};"
        try:
            cursor.execute(sql)
        except pymysql.err.OperationalError as e:
            print(f"OperationalError: {e}")
            connection = reconnect_to_mysql() 
            cursor = connection.cursor()
            cursor.execute(sql)

        global feeding_logs_date_temp
        feeding_logs_date_temp = ""
        new_feeding_data = None
        original_feeding_data = None
        base64_img = ''
        if request.method == "POST": 
            update_logs = request.form.get("update_logs")
            
            # 填寫紀錄
            if update_logs == 'true' or update_logs == '1': 
                journal_id1 = int(request.form.get("journal_id1"))
                journal_id2 = int(request.form.get("journal_id2"))
                food_name = request.form.get("food_name")

                food_id_map = {
                    "測試": 39,         # fishDB
                    "海洋牌": 40,       # ar2DB
                    "漢神牌": 41,       # ar4DB
                    "海洋飼料": 42      # ar3DB
                }
                food_id = food_id_map.get(food_name, 39)
                
                status = request.form.get("status")
                description = request.form.get("description")
                sql = f"UPDATE new_feeding_logs SET food_id = '{food_id}', food_name = '{food_name}', status = '{status}', description = '{description}' WHERE journal_id BETWEEN {journal_id1} AND {journal_id2};"
                cursor.execute(sql)

                # update api data
                isSent = send_data(journal_id1, journal_id2)

                # show feeding_logs updated result 
                if feeding_logs_date_temp: 
                    feeding_logs_date = feeding_logs_date_temp
                    selected_date = datetime.datetime.strptime(feeding_logs_date, "%Y-%m-%d")
                    next_day = selected_date + timedelta(days=1)
                    one_week_ago = selected_date - timedelta(days=7)
                    time_range = [one_week_ago + timedelta(days=i) for i in range(9)] 

                    sql = "select * from new_feeding_logs where start_time between %s and %s"
                    cursor.execute(sql, (one_week_ago + timedelta(days=1), next_day))
                    new_feeding_data = list(cursor.fetchall())
                    start_times = [row[3] for row in new_feeding_data]  
                    use_times = [row[4] for row in new_feeding_data]  
                    feeding_amounts = [row[8] for row in new_feeding_data]  

                    sql = "select * from original_feeding_logs where start_time between %s and %s"
                    cursor.execute(sql, (one_week_ago + timedelta(days=1), next_day))
                    original_feeding_data = list(cursor.fetchall())
                    original_start_times = [row[2] for row in original_feeding_data]  
                    original_use_times = [row[3] for row in original_feeding_data]  

                    font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
                    font_prop = FontProperties(fname=font_path)
                    plt.figure(figsize=(14, 8))

                    plt.xlim(time_range[0], time_range[-1])
                    plt.xticks(time_range[1:-1], rotation=60, fontproperties=font_prop) 
                    plt.gca().xaxis.set_ticks_position('top')
                    plt.gca().xaxis.set_label_position('top')

                    plt.ylim(0, 24*60)
                    plt.yticks(range(24*60, 0, -60), [f"{h:02d}:00" for h in range(0, 24)], fontproperties=font_prop)  
                    plt.grid(axis='y', linestyle='--', color='gray')

                    # 將每個 start_time 根據 y 軸(00:00 到 23:59，間隔1小時)開始往下，並根據 use_time(分鐘) 來繪製長條
                    for start_time, use_time, feeding_amount in zip(start_times, use_times, feeding_amounts):
                        start_y = (start_time.hour * 60 + start_time.minute)  
                        print(f'part of {start_time} is same as {24-(1440-start_y-use_time)/60}')
                        midday = datetime.datetime(start_time.year, start_time.month, start_time.day, 22, 0) - timedelta(days=1)
                        plt.bar(midday, use_time, width=0.17, bottom=(1440-start_y-use_time), color='#009999')
                        plt.text(midday, (1440 - start_y), str(feeding_amount), ha='center', va='bottom', color='black', fontsize=8)

                    for start_time, use_time in zip(original_start_times, original_use_times):
                        start_y = (start_time.hour * 60 + start_time.minute)  
                        print(f'part of {start_time} is same as {24-(1440-start_y-use_time)/60}')
                        midday = datetime.datetime(start_time.year, start_time.month, start_time.day, 2, 0)
                        plt.bar(midday, use_time, width=0.17, bottom=(1440-start_y-use_time), color='#ee8822')

                    legend_labels = {'#009999': '新料桶', '#ee8822': '舊料桶', 'black': '投餌量(公斤)'}
                    legend_handles = []
                    for color, label in legend_labels.items():
                        legend_handles.append(plt.Rectangle((0,0),1,1, color=color, label=label))
                    plt.legend(handles=legend_handles, prop=font_prop) 

                    plt.xlabel('date', labelpad=10, fontproperties=font_prop)  
                    plt.ylabel('feeding time', labelpad=10, fontproperties=font_prop) 
                    plt.tight_layout()

                    img_data = io.BytesIO()
                    plt.savefig(img_data, format='png')
                    img_data.seek(0)
                    base64_img = base64.b64encode(img_data.getvalue()).decode()
                    update_logs = '' 
                    feeding_logs_date_temp = '' 
                else: # 查看所有紀錄
                    sql = "SELECT * FROM new_feeding_logs"
                    cursor.execute(sql)
                    new_feeding_data = list(cursor.fetchall())
                    sql = "SELECT * FROM original_feeding_logs"
                    cursor.execute(sql)
                    original_feeding_data = list(cursor.fetchall())

            # 不填寫紀錄 => 查看紀錄
            else: 
                all_records = request.form.get("all_records")
                if all_records == 'true' or all_records == '1': # 查看所有紀錄
                    sql = "SELECT * FROM new_feeding_logs"
                    cursor.execute(sql)
                    new_feeding_data = list(cursor.fetchall())
                    sql = "SELECT * FROM original_feeding_logs"
                    cursor.execute(sql)
                    original_feeding_data = list(cursor.fetchall())
                    all_records = ''
                else: # 查看查詢日期開始往前一週(7天)的紀錄
                    feeding_logs_date = request.form.get("feeding_logs_date")
                    selected_date = datetime.datetime.strptime(feeding_logs_date, "%Y-%m-%d")
                    next_day = selected_date + timedelta(days=1)
                    one_week_ago = selected_date - timedelta(days=7)
                    time_range = [one_week_ago + timedelta(days=i) for i in range(9)] 

                    sql = "select * from new_feeding_logs where start_time between %s and %s"
                    cursor.execute(sql, (one_week_ago + timedelta(days=1), next_day))
                    new_feeding_data = list(cursor.fetchall())
                    start_times = [row[3] for row in new_feeding_data]  
                    use_times = [row[4] for row in new_feeding_data]  
                    feeding_amounts = [row[8] for row in new_feeding_data]  
                    descriptions = [row[12] for row in new_feeding_data]  

                    sql = "select * from original_feeding_logs where start_time between %s and %s"
                    cursor.execute(sql, (one_week_ago + timedelta(days=1), next_day))
                    original_feeding_data = list(cursor.fetchall())
                    original_start_times = [row[2] for row in original_feeding_data]  
                    original_use_times = [row[3] for row in original_feeding_data]  

                    font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
                    font_prop = FontProperties(fname=font_path)
                    plt.figure(figsize=(14, 8))

                    plt.xlim(time_range[0], time_range[-1])
                    plt.xticks(time_range[1:-1], rotation=60, fontproperties=font_prop) 
                    plt.gca().xaxis.set_ticks_position('top')
                    plt.gca().xaxis.set_label_position('top')

                    plt.ylim(0, 24*60)
                    plt.yticks(range(24*60, 0, -60), [f"{h:02d}:00" for h in range(0, 24)], fontproperties=font_prop)  
                    plt.grid(axis='y', linestyle='--', color='gray')

                    # 將每個 start_time 根據 y 軸(00:00 到 23:59，間隔1小時)開始往下，並根據 use_time(分鐘) 來繪製長條
                    for start_time, use_time, feeding_amount, description in zip(start_times, use_times, feeding_amounts, descriptions):
                        start_y = (start_time.hour * 60 + start_time.minute)  
                        print(f'part of {start_time} is same as {24-(1440-start_y-use_time)/60}')
                        midday = datetime.datetime(start_time.year, start_time.month, start_time.day, 22, 0) - timedelta(days=1)
                        if description == "投餌機未正常運作":
                            plt.bar(midday, use_time, width=0.17, bottom=(1440-start_y-use_time), color='#e33333')
                        else:
                            plt.bar(midday, use_time, width=0.17, bottom=(1440-start_y-use_time), color='#009999')
                        plt.text(midday, (1440 - start_y), str(feeding_amount), ha='center', va='bottom', color='black', fontsize=8)

                    for start_time, use_time in zip(original_start_times, original_use_times):
                        start_y = (start_time.hour * 60 + start_time.minute)  
                        print(f'part of {start_time} is same as {24-(1440-start_y-use_time)/60}')
                        midday = datetime.datetime(start_time.year, start_time.month, start_time.day, 2, 0)
                        plt.bar(midday, use_time, width=0.17, bottom=(1440-start_y-use_time), color='#ee8822')

                    legend_labels = {'#009999': '新料桶', '#e33333': '新料桶未正常運作', '#ee8822': '舊料桶', 'black': '投餌量(公斤)'}
                    legend_handles = []
                    for color, label in legend_labels.items():
                        legend_handles.append(plt.Rectangle((0,0),1,1, color=color, label=label))
                    plt.legend(handles=legend_handles, prop=font_prop) 

                    plt.xlabel('date', labelpad=10, fontproperties=font_prop)  
                    plt.ylabel('feeding time', labelpad=10, fontproperties=font_prop) 
                    plt.tight_layout()

                    img_data = io.BytesIO()
                    plt.savefig(img_data, format='png')
                    img_data.seek(0)
                    base64_img = base64.b64encode(img_data.getvalue()).decode()
                    feeding_logs_date_temp = feeding_logs_date
                    feeding_logs_date = ''

        return render_template('feeding_logs.html', 
                               new_feeding_data=new_feeding_data, 
                               original_feeding_data=original_feeding_data, 
                               base64_img=base64_img, 
                               isSent=isSent, 
                               species=species, species_logo_url=species_logo_url) 
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
        sql = f"USE {databaseName};"
        try:
            cursor.execute(sql)
        except pymysql.err.OperationalError as e:
            print(f"OperationalError: {e}")
            connection = reconnect_to_mysql() 
            cursor = connection.cursor()
            cursor.execute(sql)
        
        if request.method == "POST":
            pool_id = request.form.get("pool_id")
            print(pool_id)
            sql = f"select pool_id from field_logs where pool_id={str(pool_id)};"
            cursor.execute(sql)
            field_result = cursor.fetchall()

            sql = f"select pool_id from new_feeding_logs where pool_id={str(pool_id)};"
            cursor.execute(sql)
            feeding_result = cursor.fetchall()
            
            if len(field_result) == 0:
                print("field_logs is empty")
                alertContent="ThisPoolhasNoFieldData!"

            elif len(feeding_result) == 0:
                print("new_feeding_logs is empty")
                alertContent="ThisPoolhasNoFeedingData!"

            else:
                print("Result set is not empty")
                # counting estimated_weights
                sql = f"select record_weights from field_logs where pool_id={str(pool_id)} order by update_time asc;"
                cursor.execute(sql)
                first_weight = cursor.fetchone()
                first_weight = first_weight[0]

                sql = f"select spec from field_logs where pool_id={str(pool_id)} order by update_time asc;"
                cursor.execute(sql)
                first_spec = cursor.fetchone()
                first_spec = first_spec[0]
                total_fish_number = first_spec * first_weight

                sql = f"select estimated_weights from field_logs where pool_id={str(pool_id)} order by update_time desc;"
                cursor.execute(sql)
                latest_weight = cursor.fetchone()
                latest_weight = latest_weight[0]

                sql = f"select update_time from field_logs where pool_id={str(pool_id)} order by update_time asc;"
                cursor.execute(sql) 
                first_time = cursor.fetchone()
                first_time = first_time[0]
                query_time = datetime.datetime.now()
                age = str((query_time-first_time).days)
                
                # counting fcr
                sql = f"select feeding_amount from new_feeding_logs where pool_id={str(pool_id)} order by start_time desc;"
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


''' water_splash_analysis function '''
def generate_heatmap(result, query_date, duration):
    if len(result) == 0:
        print("Error: ripple_result is empty")
        return None
    
    df = pd.DataFrame(result, columns=['update_time', 'ripple_area'])
    if df.empty:
        print("Error: DataFrame is empty")
        return None
    
    df['update_time'] = pd.to_datetime(df['update_time'])
    df['date'] = df['update_time'].dt.date
    df['minute'] = df['update_time'].dt.floor('T')
    df_grouped = df.groupby(['date', 'minute']).mean().reset_index()

    heatmap_data = np.full((24 * 60, duration), np.nan)  # 24小時 x 60分鐘 x duration 天
    for _, row in df_grouped.iterrows():
        day_index = (row['date'] - query_date.date()).days
        minute_of_day = row['minute'].hour * 60 + row['minute'].minute
        heatmap_data[minute_of_day, day_index] = row['ripple_area']

    marks = []
    start_time = df.iloc[0]['update_time']
    prev_time = start_time

    for i in range(1, len(df)):
        current_time = df.iloc[i]['update_time']
        
        time_diff = (current_time - prev_time).total_seconds() / 60 

        if time_diff > 2:  # 如果時間差大於 1 分鐘
            marks.append({'start_time': start_time, 'end_time': prev_time})
            start_time = current_time  

        prev_time = current_time

    marks.append({'start_time': start_time, 'end_time': prev_time})
    marks_df = pd.DataFrame(marks)
    # print(marks_df)

    fig, axes = plt.subplots(1, duration, figsize=(math.ceil(duration*1.8) if duration > 10 else 15,  20 if duration >= 60 else 10), sharey=True, constrained_layout=True, dpi=50)
    cmap = plt.get_cmap('hot')
    cmap.set_bad(color='black')  # 設置 np.nan 部分為黑色
    
    for i in range(duration):
        day_data = heatmap_data[:, i].reshape(-1, 1)
        ax = axes[i]
        im = ax.imshow(day_data, cmap=cmap, aspect='auto', vmin=0, vmax=np.nanmax(heatmap_data))

        ax.set_title((query_date + timedelta(days=i)).strftime('%m-%d'), fontsize=28 if duration >= 60 else 14)
        ax.set_xticks([]) 
        ax.set_yticks(range(0, 24 * 60, 120))
        ax.set_yticklabels([f"{j:02d}:00" for j in range(0, 24, 2)])
        ax.tick_params(axis='y', labelsize=28 if duration >= 60 else 14)
        
        # 畫藍色框
        for mark in marks:
            start_minute = (mark['start_time'].hour * 60) + mark['start_time'].minute
            end_minute = (mark['end_time'].hour * 60) + mark['end_time'].minute

            if mark['start_time'].date() == (query_date + timedelta(days=i)).date():
                rect_y = start_minute -5 # 5 min
                rect_height = (end_minute - start_minute) + 10

                rect = patches.Rectangle(
                    (-0.5, rect_y),     # 左下角座標 (x, y)
                    1,                  # 矩形寬度
                    rect_height,        # 矩形高度
                    linewidth=2,
                    edgecolor='blue',
                    facecolor='none'    # 只顯示邊框
                )
                ax.add_patch(rect)

    cbar = plt.colorbar(im, ax=axes.ravel().tolist(), aspect=50, pad=0.02)
    cbar.set_label('Pixel Number of Water Splashes', fontsize=14)

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    base64_img = base64.b64encode(img_data.getvalue()).decode()
    plt.close(fig)

    return base64_img

def counting_first_thd_idx_4_test(feeding_result, ripple_result):
    alpha = 0.01            # T 檢驗顯著性水平
    windows_minutes = 25    # 滑動窗口大小
    t3 = 5                  # 最小分析時間
    odd_windows_size = 7     # 中值濾波窗口大小

    first_thd_idx_4_test = [] # 儲存第一次水花顯著下降的索引

    total = len(feeding_result)
    for idx, (start_time, use_time) in enumerate(feeding_result):
        t1_datetime = start_time + timedelta(minutes=5)  # 略過前 5 分鐘
        end_time = start_time + timedelta(minutes=use_time)

        # 過濾ripple_result中的資料，符合這次投餌的時間範圍
        ripple_data_filtered = [(t, ra) for t, ra in ripple_result if t1_datetime <= t <= end_time]
        if len(ripple_data_filtered) <= 20:
            print(f'Skip {idx} data {start_time.strftime("%Y-%m-%d %H:%M:%S")} to {end_time.strftime("%Y-%m-%d %H:%M:%S")}')
            first_thd_idx_4_test.append(None)
            continue

        feed_once_dt_data, feed_once_data = zip(*ripple_data_filtered)
        feed_once_data = np.asarray(feed_once_data)
        smoothed_data = medfilt(feed_once_data, odd_windows_size)

        first_flag = False
        for i in range(math.ceil(use_time)):
            wend = end_time - timedelta(minutes=i)
            wstart = wend - timedelta(minutes=windows_minutes)
            filter = np.logical_and(np.asarray(feed_once_dt_data) >= wstart, np.asarray(feed_once_dt_data) <= wend)
            w_data = smoothed_data[filter]
            w_datetime = np.asarray(feed_once_dt_data)[filter]

            if len(w_data) <= 2:
                break

            threshold_indexs = [len(w_data) // 2]
            if i < 5:
                under_bound = w_datetime > wend - timedelta(minutes=t3)
                if np.any(under_bound):
                    valid_indices = np.where(under_bound == True)[0]
                    if len(valid_indices) > 0:
                        threshold_indexs = list(range(threshold_indexs[0], valid_indices[0]))
                        threshold_indexs.sort(reverse=True)
                    else:
                        continue
                else:
                    continue

            for thd_idx in threshold_indexs:
                threshold_value = w_data[thd_idx]
                global_th_idx = np.where(smoothed_data == threshold_value)[0][0]
                wdata_before = w_data[:thd_idx]
                wdata_after = w_data[thd_idx:]
                t_stat, p_value = stats.ttest_ind(wdata_before, wdata_after, alternative='greater')

                if p_value < alpha and first_flag == False:
                    first_thd_idx_4_test.append(w_datetime[thd_idx])
                    first_flag = True

        if not first_flag:
            first_thd_idx_4_test.append(None)
    
    # print(f"first_thd_idx_4_test: {first_thd_idx_4_test}")
    return first_thd_idx_4_test

def plot_trendchart(period, ripple_result, feeding_result, query_date, selected_date, duration, min_date, max_date):
    morning_segments = defaultdict(list)
    for t, ripple_area in ripple_result:
        morning_segments[t.date()].append(ripple_area)
    
    while min_date <= max_date:
        if min_date not in morning_segments:
            morning_segments[min_date] = None 
        min_date += timedelta(days=1) 

    morning_segments = [
        (idx, date, None if ripple_areas is None else sum(ripple_areas) / len(ripple_areas))
        for idx, (date, ripple_areas) in enumerate(sorted(morning_segments.items()))
    ]
    
    filtered_segments = [(idx, date, ripple_area) for idx, date, ripple_area in morning_segments if ripple_area is not None]
    idxs = np.array([segment[0] for segment in filtered_segments])
    dates = [segment[1] for segment in filtered_segments]
    ripple_areas = np.array([segment[2] for segment in filtered_segments])

    # least square method, f(t) = at + b
    n = len(idxs)
    t = np.sum(idxs)
    t2 = np.sum(idxs**2)
    mt = np.sum(ripple_areas)
    t_mt = np.sum(idxs*ripple_areas)

    if (n*t2-t**2) != 0:
        a = (n*t_mt-t*mt)/(n*t2-t**2)
        b = (mt - a*t)/n
    else:        
        a = float('nan')
        b = float('nan')

    predict_trends=a*idxs+b

    # 找水花明顯下降的時間點
    first_thd_idx_4_test = counting_first_thd_idx_4_test(feeding_result, ripple_result)
    feed_count = []
    decline_dates = []
    minutes = []

    for i, (feed_st_time, feed_used_min) in enumerate(feeding_result):
        if first_thd_idx_4_test[i] is None:
            continue
        # remaining_time = feed_st_time + timedelta(minutes=feed_used_min) - first_thd_idx_4_test[i]
        feeded_time = first_thd_idx_4_test[i] - feed_st_time
        print(f'[{i}] {feed_st_time.strftime("%Y-%m-%d %H:%M:%S")}: ({feeded_time.total_seconds()/60}) minutes')
        feed_count.append(i+1)
        decline_dates.append(feed_st_time.date())
        minutes.append(feeded_time.total_seconds()/60)
    
    if decline_dates:
        # Generate x and y (using total seconds)
        x_dates_num = mdates.date2num(decline_dates)

        # 將日期數值平移，讓最早的日期對應 feed_count 的第1次投餵
        x = np.array(x_dates_num - x_dates_num[0]) 
        # x = np.array(feed_count)
        y = np.array(minutes)
        
        # least square method, f(t) = at + b
        n = len(x)
        t = np.sum(x)
        t2 = np.sum(x**2)
        mt = np.sum(y)
        t_mt = np.sum(x*y)

        if (n*t2-t**2) != 0:
            decline_a = (n*t_mt-t*mt)/(n*t2-t**2)
            decline_b = (mt - decline_a*t)/n
        else:        
            decline_a = float('nan')
            decline_b = float('nan')

        decline_trends=decline_a*x+decline_b
    else:
        print("decline_dates is empty")

    # if len(np.unique(x)) > 1:
    #     # Assemble matrix A
    #     A = np.vstack([x, np.ones(len(x))]).T

    #     # Turn y into a column vector
    #     y = y[:, np.newaxis]

    #     # 檢查 A.T * A 是否為奇異矩陣
    #     if np.linalg.cond(np.dot(A.T, A)) < 1 / np.finfo(A.dtype).eps:
    #         # Direct least square regression
    #         alpha = np.dot(np.dot(np.linalg.inv(np.dot(A.T, A)), A.T), y)
    #         print(f"Slope: {alpha[0][0]:.5f}, Intercept: {alpha[1][0]:.5f}")
    #     else:
    #         print("Warning: Singular matrix encountered. Skipping regression.")
    #         alpha = [[0], [0]] 
    # else:
    #     print("Warning: No variation in x. Skipping regression.")
    #     alpha = [[0], [0]]  

    # print(f"Dates: {dates}")
    # print(f"Decline Dates: {decline_dates}")

    from matplotlib import font_manager
    font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    font_prop = font_manager.FontProperties(fname=font_path)

    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False  # 避免負號顯示為方框

    fig, ax1 = plt.subplots(figsize=(math.ceil(duration * 1.8) if duration > 10 else 15, 20 if duration >= 60 else 10), dpi=50)

    locator = mdates.DayLocator() 
    formatter = mdates.DateFormatter('%m-%d') 
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(formatter)

    # 第一個 Y 軸：水花面積
    ax1.tick_params(axis='x', labelsize=30 if duration >= 60 else 18) 
    ax1.tick_params(axis='y', labelcolor='tab:blue', labelsize=30 if duration >= 60 else 18) 
    ax1.plot(dates, ripple_areas, 'o', color='tab:blue', label="平均水花面積值", markersize=20 if duration >= 60 else 15)
    ax1.plot(dates, predict_trends, '-', color='tab:blue', linewidth=6 if duration >= 60 else 4, label=f"水花面積趨勢: y={a:.0f}t+{b:.0f}")

    original_morning_dates = [r[0].date() for r in ripple_result]
    original_morning_ripple_areas = [r[1] for r in ripple_result]
    ax1.scatter(original_morning_dates, original_morning_ripple_areas, color='black', s=20, label='原始水花面積資料點')

    if a/b > 0.01:
        plt.figtext(0.5, 0.92, f'食慾成長程度={a/b:.3f}>1%, 食慾增加', color='red', fontsize=24 if duration >= 60 else 18, fontweight='bold',  ha="center", fontproperties=font_prop)
    elif a/b < -0.01:
        plt.figtext(0.5, 0.92, f'食慾成長程度={a/b:.3f}<1%, 食慾下降', color='red', fontsize=24 if duration >= 60 else 18, fontweight='bold',  ha="center", fontproperties=font_prop)
    else:
        plt.figtext(0.5, 0.92, f'食慾成長程度={a/b:.3f}≈1%, 食慾持平', color='red', fontsize=24 if duration >= 60 else 18, fontweight='bold',  ha="center", fontproperties=font_prop)
        
    ax2 = ax1.twinx()
    ax2.tick_params(axis='y', labelcolor='tab:orange', labelsize=30 if duration >= 60 else 18) 
    if len(decline_dates) > 0:
        ax2.plot(decline_dates, minutes, 'o', color='tab:orange', label="水花明顯下降時間(分鐘)", markersize=20 if duration >= 60 else 15)
        ax2.plot(decline_dates, decline_trends, '-', color='tab:orange', linewidth=6 if duration >= 60 else 4, label=f"下降時間趨勢: y={decline_a:.2f}t+{decline_b:.2f}")

    ax1.set_xlabel('Date', fontsize=32 if duration >= 60 else 18, fontweight='bold')
    ax1.set_ylabel('Water Splash Area', fontsize=32 if duration >= 60 else 18, fontweight='bold', color='tab:blue')
    ax2.set_ylabel('Water Splash Decline Time (mins)', fontsize=32 if duration >= 60 else 18, fontweight='bold', color='tab:orange')
    plt.xlim(query_date, selected_date)
    plt.title(f'Water Splash Trend Chart for {period}', fontsize=42 if duration >= 60 else 20, fontweight='bold')
    plt.subplots_adjust(top=0.9)

    ax1.legend(loc='upper left', fontsize=28 if duration >= 60 else 18)
    ax2.legend(loc='upper right', fontsize=28 if duration >= 60 else 18)

    plt.grid(True)
    plt.tight_layout()

    trendchart_data = io.BytesIO()
    plt.savefig(trendchart_data, format='png')
    trendchart_data.seek(0)
    trendchart = base64.b64encode(trendchart_data.getvalue()).decode()
    plt.close()

    return trendchart

def generate_trendchart(ripple_result, feeding_result, query_date, selected_date, duration):
    ripple_morning_result = []
    ripple_afternoon_result = []
    feeding_morning_result = []
    feeding_afternoon_result = []
    min_date = ripple_result[0][0].date()
    max_date = ripple_result[-1][0].date()
    
    for r in ripple_result: 
        timestamp, ripple_area = r
        result_date = timestamp.date()
        if 0 < timestamp.hour < 12:
            ripple_morning_result.append((timestamp, ripple_area))
        else:
            ripple_afternoon_result.append((timestamp, ripple_area))

    for r in feeding_result: 
        st, use_time = r
        if 0 < st.hour < 12:
            feeding_morning_result.append((st, use_time))
        else:
            feeding_afternoon_result.append((st, use_time))

    morning_trendchart = plot_trendchart('Morning 0:00-11:59', ripple_morning_result, feeding_morning_result, query_date, selected_date, duration, min_date, max_date)
    afternoon_trendchart = plot_trendchart('Afternoon 12:00-23:59', ripple_afternoon_result, feeding_afternoon_result, query_date, selected_date, duration, min_date, max_date)

    return morning_trendchart, afternoon_trendchart

@app.route('/water_splash_analysis', methods=["GET", "POST"])
def water_splash_analysis():
    if 'username' in session:
        global connection
        cursor = connection.cursor()
        sql = f"USE {databaseName};"
        try:
            cursor.execute(sql)
        except pymysql.err.OperationalError as e:
            print(f"OperationalError: {e}")
            connection = reconnect_to_mysql() 
            cursor = connection.cursor()
            cursor.execute(sql)

        base64_img = ''
        morning_trendchart = '' 
        afternoon_trendchart = '' 
        duration = 0

        if request.method == "POST": 
            opt = int(request.form.get("opt"))
            print(opt)
            selected_date = request.form.get("selected_date")
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d")
            next_day = selected_date + timedelta(days=1)
            if opt == 1:
                query_date = selected_date - timedelta(days=6)
                duration = 7
            elif opt == 2:
                query_date = selected_date - timedelta(days=29)
                duration = 30
            else:
                query_date = selected_date - timedelta(days=89)
                duration = 90

            print(f'selected_date: {selected_date}, query_date: {query_date}')

            sql = "select update_time, ripple_area from ripple_history where update_time between %s and %s order by update_time asc"
            cursor.execute(sql, (query_date, next_day))
            ripple_result = list(cursor.fetchall())

            sql = "SELECT start_time, use_time FROM new_feeding_logs WHERE use_time > %s and start_time between %s and %s order by start_time asc"
            cursor.execute(sql, (10, query_date, next_day))
            feeding_result = list(cursor.fetchall())
            print("feeding_result is from new_feeding_logs")
            
            print(f"Ripple result:  {ripple_result[:1]} ~ {ripple_result[-1:]}")
            print(f"Feeding result: {feeding_result[:1]} ~ {feeding_result[-1:]}")

            print("generate_heatmap")
            base64_img = generate_heatmap(ripple_result, query_date, duration)
            print("generate_trendchart")
            morning_trendchart, afternoon_trendchart = generate_trendchart(ripple_result, feeding_result, query_date, selected_date, duration)

        return render_template('water_splash_analysis.html', 
                            base64_img=base64_img, 
                            morning_trendchart=morning_trendchart, 
                            afternoon_trendchart=afternoon_trendchart, 
                            species=species, species_logo_url=species_logo_url) 
    else:
        return redirect(url_for('login'))
   

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
    sql = f"USE {databaseName};"
    try:
        cursor.execute(sql)
    except pymysql.err.OperationalError as e:
        print(f"OperationalError: {e}")
        connection = reconnect_to_mysql() 
        cursor = connection.cursor()
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
        sql = f"USE {databaseName};"
        try:
            cursor.execute(sql)
        except pymysql.err.OperationalError as e:
            print(f"OperationalError: {e}")
            connection = reconnect_to_mysql() 
            cursor = connection.cursor()
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
