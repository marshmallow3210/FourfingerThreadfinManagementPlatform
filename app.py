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

app = Flask(__name__)
CORS(app)  # 允許所有來源的跨來源請求
app.secret_key = '66386638'  # 替換為隨機的密鑰，用於安全性目的

connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='lab403',
                             password='66386638',
                             autocommit=True)

users = {
    'oakley': 'letmein',
    'admin': 'admin',
    'fishDB': 'fishDB',
    'ar0DB': 'ar0DB',
    'ar1DB': 'ar1DB',
    'ar2DB': 'ar2DB',
    'ar3DB': 'ar3DB',
    'ar4DB': 'ar4DB'
}

login_manager = LoginManager()
login_manager.init_app(app)

# User class for demonstration purposes
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def choooseDatabaseName(username):
    global databaseName
    databaseName = ""
    if username == "fishDB" or username == "oakley":
        databaseName = "fishDB"
    elif username == "ar0DB":
        databaseName = "ar0DB"
    elif username == "ar1DB":
        databaseName = "ar1DB"
    elif username == "ar2DB":
        databaseName = "ar2DB"
    elif username == "ar3DB":
        databaseName = "ar3DB"
    elif username == "ar4DB":
        databaseName = "ar4DB"

def utc8(utc, p):
    for i in range(0, len(utc)):
        if utc[i][p] != None:
            utc[i] = list(utc[i])
            utc[i][p]=utc[i][p].astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")

    return utc

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

def preidict_date(latest_weight):
    # 午仔魚
    # 17 months, 2015/4~2016/8
    x_set = np.array([0, 2, 15, 47, 73, 81, 116, 157, 178, 193, 190, 195, 199, 202, 208, 215, 230]) #, 238, 250, 260])
    x_set = x_set * 600 / 328
    date1 = datetime.date(2015,4,1)
    date2 = datetime.date(2016,8,31)
    days_count = (date2-date1).days
    y_set = np.linspace(0, days_count, 18)

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
        estimated_fcr = round(total_feeding_amount/(latest_weight-first_weights), 2)
        return estimated_fcr

@app.route('/')
def test():
    data = "Hello!"
    return render_template('test.html', data=data)

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
            choooseDatabaseName(username)
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

@app.route('/home')
def home():
    # 檢查用戶是否登入，未登入則返回登入頁面
    if 'username' in session:
        update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(update_time)
        return render_template('home.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/decision', methods=["GET", "POST"])
def decision():
    if 'username' in session:
        command=None
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

        return render_template('decision.html')
    else:
        return redirect(url_for('login'))

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

def getFrames():
    global connection
    cursor = connection.cursor()
    sql = "use " + databaseName + ";"
    cursor.execute(sql)

    sql = "select update_time, data from frames order by update_time desc LIMIT 1;"
    cursor.execute(sql)
    data = cursor.fetchone()

    if data:
        update_time = data[0]
        binary_data = data[1]
        binary_data_btye_str = io.BytesIO(binary_data) # 將二進制數據讀取為字節串
        binary_data_base64 = base64.b64encode(binary_data_btye_str.getvalue()).decode('utf-8') # 將圖片轉換為Base64字串
        print("return base64 str")
        return update_time, binary_data_base64
    else:
        return 'data from frames were not found', 404

@app.route('/field_view', methods=["GET", "POST"])
def field_view():
    if 'username' in session:
        # storeFrames()
        update_time, binary_data_base64 = getFrames()
        return render_template('field_view.html', update_time=update_time, binary_data_base64=binary_data_base64)
    else:
        return redirect(url_for('login'))
  
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
            
        return render_template('field_logs.html', pool_count=pool_count,pool_data=pool_data, data=data)#, fcr=fcr)
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
                print('estimated_weights:', estimated_weights)
                
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

        return render_template('update.html', isSuccess=isSuccess)
    # else:
    #     return redirect(url_for('login'))

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

        return render_template('feeding_logs.html', feeding_data=feeding_data)  
    else:
        return redirect(url_for('login'))   

@app.route('/query', methods=["GET", "POST"])
def query():
    if 'username' in session:
        return render_template('query.html')
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
            
                return render_template('query_result.html', age=int(age), estimated_date=estimated_date, estimated_weights=latest_weight, estimated_fcr=estimated_fcr, total_feeding_amount=total_feeding_amount, first_weights=first_weight)
        
            return render_template('query.html', alertContent=alertContent)
    else:
        return redirect(url_for('login'))
    
# get field data by jsgrid
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

# get feeding data by jsgrid
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

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True # flask app 自動重新加載模板(html)
    app.jinja_env.auto_reload = True # Jinja2 自動重新加載設定
    # app.run(debug=True) # in development server
    app.run(port=8080, debug=False) # in production server
