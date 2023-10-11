import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_cors import CORS
import pymysql
import datetime
from datetime import timezone, timedelta
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neighbors import KNeighborsRegressor

app=Flask(__name__)
CORS(app)  # 允許所有來源的跨來源請求
app.secret_key = '66386638'  # 替換為隨機的密鑰，用於安全性目的

databaseName = "fishDB"

connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='marsh12mallow14',
                             autocommit=True)

# connection = pymysql.connect(host='34.81.183.159',
#                              port=3306,
#                              user='lab403',
#                              password='66386638',
#                              autocommit=True)

users = {
    'oakley': 'letmein',
    'admin': 'admin'
}

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
    y_pred = y_pred * total_fish_number /1000
    print("input Age(d):", x_new)
    print("predicted Body weight(kg):", y_pred)
    
    return y_pred

def preidict_date(weight):
    # 午仔魚
    # 9 months
    x_set = np.array([0, 2, 15, 47, 73, 81, 116, 157, 178, 193]) #, 190, 195, 199, 202, 208, 215, 230, 238, 250, 260])
    x_set = x_set * 600 / 328
    date1 = datetime.date(2015,4,1)
    date2 = datetime.date(2015,12,31)
    days_count = (date2-date1).days
    y_set = np.linspace(0, days_count, 10)

    # KNN Regression
    k = 3
    knn = KNeighborsRegressor(n_neighbors=k)
    knn.fit(x_set.reshape(-1, 1), y_set)
    x_new = np.array([int(weight)])
    y_pred = knn.predict(x_new.reshape(-1, 1))
    y_pred = y_pred[0]
    print("input Body weight(g):", x_new)
    print("predicted Age(d):", y_pred)
    
    return y_pred

def counting_fcr(total_feeding_amount, estimated_weights, first_weights):
    estimated_fcr = round(total_feeding_amount/(estimated_weights-first_weights), 2)
    return estimated_fcr

@app.route('/dispenser', methods=["GET", "POST"])
def dispenser():
    global connection
    cursor = connection.cursor()
    sql = "use " + databaseName + ";"
    cursor.execute(sql)

    if request.method == "POST":
        try:
            pool_ID = int(request.form.get("pool_ID"))
            sql = "insert into dispenser(pool_ID) value({})".format(pool_ID)
            cursor.execute(sql)
        except:
            sql = "truncate dispenser;"
            cursor.execute(sql)

    sql = "select pool_ID from field_logs;"
    cursor.execute(sql)
    pool_count = cursor.fetchall()
    sql = "select ff.pool_ID, d.dispenser_ID from field_logs as ff inner join dispenser as d where ff.pool_ID=d.pool_ID order by pool_ID, dispenser_ID;"
    cursor.execute(sql)
    dispenser_count = cursor.fetchall()
    try:
        s=dispenser_count[0][0]
        data = [["場域 {}:".format(s)]]
        if s!=None:
            for temp in dispenser_count:
                if temp[0] != s:
                    data.append(["場域 {}: ".format(temp[0])])
                    s=temp[0]
                data[-1].append(temp[1])
    except:
        data=[]
    page = render_template('dispenser.html', pool_count=pool_count, data=data, data_len=len(data))

    return page

@app.route('/decision', methods=["GET", "POST"])
def decision():
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

    page = render_template('decision.html')
    return page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username)

        if username in users and users[username] == password:
            # 登入成功，將用戶名存入 session
            session['username'] = username
            print('yes')
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    # 清除用戶名的 session 資料
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    usr='jim'
    # 檢查用戶是否登入，未登入則返回登入頁面
    if 'username' in session:
        return render_template('home.html', username=session['username'], usr=usr)
    else:
        return redirect(url_for('login'))
    # home = render_template('home.html')
    # return home

def getDataFromESP32():
    global connection
    cursor = connection.cursor()
    sql = "use " + databaseName + ";"
    cursor.execute(sql)

    # counting feeding_amount
    today_date = datetime.datetime.today().date()
    today_date = "2023-10-05"
    sql = "SELECT COUNT(*) AS feeding_count FROM ESP32 WHERE date = '" + today_date +"';"
    cursor.execute(sql)
    feeding_count = list(cursor.fetchall())
    feeding_count = int(feeding_count[0][0])

    sql = "select weight from ESP32"
    cursor.execute(sql)
    weight = list(cursor.fetchall())
    
    feeding_amount = 0
    feeding_benchmark = weight[0][0]
    for i in range(0, feeding_count):
        if weight[i][0] < feeding_benchmark:
            feeding_amount = feeding_amount + (feeding_benchmark - weight[i][0])
        else:
            feeding_benchmark = weight[i][0]
    print('feeding_amount:', feeding_amount)

    # counting start_time and use_time
    sql = "SELECT CONCAT(date, ' ', MIN(time)) AS start_time FROM ESP32 GROUP BY date;"
    cursor.execute(sql)
    start_time = list(cursor.fetchall())
    start_time = start_time[0][0]
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    print('start_time:', start_time)

    sql = "SELECT CONCAT(date, ' ', MAX(time)) AS last_time FROM ESP32 GROUP BY date;"
    cursor.execute(sql)
    last_time = list(cursor.fetchall())
    last_time = last_time[0][0]
    last_time = datetime.datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")

    use_time = last_time - start_time
    use_time = use_time.total_seconds() / 60
    use_time = round(use_time, 2)
    print('use_time:', use_time)

    sql = 'insert into feeding_logs (start_time, use_time, feeding_amount) values("{}", {}, {});'.format(start_time, use_time, feeding_amount)
    cursor.execute(sql)

@app.route('/feeding_logs', methods=["GET", "POST"])
def feeding_logs():
    global connection
    cursor = connection.cursor()
    sql = "use " + databaseName + ";"
    cursor.execute(sql)

    sql = "select * from feeding_logs"
    cursor.execute(sql)
    feeding_data = list(cursor.fetchall())
    print(feeding_data)

    page = render_template('feeding_logs.html', feeding_data=feeding_data)
    return page   
  
@app.route('/field_logs', methods=["GET", "POST"])
def field_logs():
    print(request.method)
    global connection
    cursor = connection.cursor()
    sql = "use " + databaseName + ";"
    cursor.execute(sql)
    
    # sql = "select ff.pool_ID, d.dispenser_ID, fl.feeding_time, fl.use_time, fl.food_ID, fl.used from field_logs as ff inner join dispenser as d inner join feeding_logs as fl where ff.pool_ID=d.pool_ID and d.dispenser_ID=fl.dispenser_ID order by fl.feeding_time desc;"
    # cursor.execute(sql)
    # data = list(cursor.fetchall())
    # data = utc8(data, 2)

    sql = "select * from field_logs;"
    cursor.execute(sql)
    data = list(cursor.fetchall())
    data = utc8(data, 6)
    print(data)
    
    # sql = "select fcr from field_logs;"
    # cursor.execute(sql)
    # fcr = list(cursor.fetchall())
    # print(fcr)
    # fcr = utc8(fcr, 2)
    # fcr = utc8(fcr, 3)
    
    if request.method == "POST":
        json_data = request.get_json("data")
        pool_ID = int(json_data["pool_ID"])
        print("receive POST", pool_ID)
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
        
    page = render_template('field_logs.html', pool_count=pool_count,pool_data=pool_data, data=data)#, fcr=fcr)
    return page   
    
@app.route('/update', methods=["GET", "POST"])
def update():
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
            sql = "UPDATE feeding_logs SET food_ID = " + "'" + str(food_ID) + "'" + " WHERE pool_ID = "+str(pool_ID)+" order by start_time desc;"
            # sql = 'insert into feeding_logs (pool_ID, food_ID) values({}, "{}");'.format(pool_ID, food_ID)
            cursor.execute(sql)
            
            # counting estimated_weights
            sql = "select record_weights from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
            cursor.execute(sql)
            first_weights = cursor.fetchone()
            first_weights = first_weights[0]
            sql = "select spec from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
            cursor.execute(sql)
            first_spec = cursor.fetchone()
            first_spec = first_spec[0]
            total_fish_number = first_spec * first_weights
            sql = "select update_time from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
            cursor.execute(sql) 
            first_time = cursor.fetchone()
            first_time = first_time[0]
            update_time = datetime.datetime.strptime(update_time, "%Y-%m-%d %H:%M:%S")
            age = str((update_time-first_time).days)
            print("養殖了:" + age + "天")
            estimated_weights = preidict_weights(age, total_fish_number)
            print('total_fish_number:', total_fish_number)
            print('estimated_weights:', estimated_weights)
            
            # counting fcr
            sql = "select feeding_amount from feeding_logs where pool_ID = "+str(pool_ID)+";"
            cursor.execute(sql)
            feeding_amount = list(cursor.fetchall())
            total_feeding_amount = 0
            for i in range(len(feeding_amount)):
                total_feeding_amount += feeding_amount[i][0]
            print("total_feeding_amount:", total_feeding_amount)
            fcr = counting_fcr(total_feeding_amount, estimated_weights, first_weights)
            
            # insert all data into field_logs
            spec = None
            sql = 'INSERT INTO field_logs (pool_ID, spec, record_weights, estimated_weights, fcr, dead_counts, update_time) VALUES ({}, %s, {}, {}, {}, {}, %s);'.format(pool_ID, record_weights, estimated_weights, fcr, dead_counts)
            data = (spec, update_time)
            cursor.execute(sql, data)

        else:
            # counting estimated_weights
            sql = "select record_weights from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
            cursor.execute(sql)
            first_weights = cursor.fetchone()
            first_weights = first_weights[0]
            sql = "select spec from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
            cursor.execute(sql)
            first_spec = cursor.fetchone()
            first_spec = first_spec[0]
            total_fish_number = first_spec * first_weights
            sql = "select update_time from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
            cursor.execute(sql) 
            first_time = cursor.fetchone()
            first_time = first_time[0]
            update_time = datetime.datetime.strptime(update_time, "%Y-%m-%d %H:%M:%S")
            age = str((update_time-first_time).days)
            print("養殖了:" + age + "天")
            estimated_weights = preidict_weights(age, total_fish_number)
            print('total_fish_number:', total_fish_number)
            print('estimated_weights:', estimated_weights)
            
            # counting fcr
            sql = "select feeding_amount from feeding_logs where pool_ID = "+str(pool_ID)+";"
            cursor.execute(sql)
            feeding_amount = list(cursor.fetchall())
            total_feeding_amount = 0
            for i in range(len(feeding_amount)):
                total_feeding_amount += feeding_amount[i][0]
            print("total_feeding_amount:", total_feeding_amount)
            fcr = counting_fcr(total_feeding_amount, estimated_weights, first_weights)

            # insert all data into field_logs
            sql = 'insert into field_logs (pool_ID, spec, record_weights, estimated_weights, fcr, dead_counts, update_time) values({}, {}, {}, {}, {}, {}, "{}");'.format(pool_ID, float(spec), record_weights, estimated_weights, fcr, dead_counts, update_time)
            cursor.execute(sql)
            isSuccess = 1
        return redirect(url_for("field_logs"))

    page = render_template('update.html', isSuccess=isSuccess)
    return page

@app.route('/query', methods=["GET", "POST"])
def query():
    query = render_template('query.html')
    return query

@app.route('/query_result', methods=["GET", "POST"])
def query_result():
    global connection
    cursor = connection.cursor()
    sql = "use " + databaseName + ";"
    cursor.execute(sql)
    
    if request.method == "POST":
        pool_ID = request.form.get("pool_ID")
        print(pool_ID)
        # counting estimated_weights
        sql = "select record_weights from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
        cursor.execute(sql)
        first_weights = cursor.fetchone()
        first_weights = first_weights[0]
        sql = "select spec from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
        cursor.execute(sql)
        first_spec = cursor.fetchone()
        first_spec = first_spec[0]
        total_fish_number = first_spec * first_weights
        sql = "select update_time from field_logs where pool_ID = "+str(pool_ID)+" order by update_time asc;"
        cursor.execute(sql) 
        first_time = cursor.fetchone()
        first_time = first_time[0]
        query_time = datetime.datetime.now()
        age = str((query_time-first_time).days)
        print("養殖了:" + age + "天")
        estimated_weights = preidict_weights(age, total_fish_number)
        print('total_fish_number:', total_fish_number)
        print('estimated_weights:', estimated_weights)
        
        # counting fcr
        sql = "select feeding_amount from feeding_logs where pool_ID = "+str(pool_ID)+";"
        cursor.execute(sql)
        feeding_amount = list(cursor.fetchall())
        total_feeding_amount = 0
        for i in range(len(feeding_amount)):
            total_feeding_amount += feeding_amount[i][0]
        print("total_feeding_amount:", total_feeding_amount)
        estimated_fcr = counting_fcr(total_feeding_amount, estimated_weights, first_weights)
        
        # counting estimated_date
        estimated_date = preidict_date(estimated_weights)
        estimated_date = first_time + datetime.timedelta(days=int(estimated_date))
        print('estimated_date:', estimated_date)
        
    query_result = render_template('query_result.html', age=int(age), estimated_date=estimated_date, estimated_weights=estimated_weights, estimated_fcr=estimated_fcr, total_feeding_amount=total_feeding_amount, first_weights=first_weights)
    return query_result

# get field data
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

# get feeding data
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
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.run(debug=True) # in development server
    # app.run(debug=False) # in production server
