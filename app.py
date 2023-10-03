import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import pymysql
import datetime
from datetime import timezone, timedelta
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neighbors import KNeighborsRegressor

app=Flask(__name__)
app.secret_key = '66386638'  # 替換為隨機的密鑰，用於安全性目的

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

databaseName = "ai_fish"

def utc8(utc, p):
    for i in range(0, len(utc)):
        if utc[i][p] != None:
            utc[i] = list(utc[i])
            utc[i][p]=utc[i][p].astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")

    return utc

def preidict_weights(age):
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
    print("input Age(d):", x_new)
    print("predicted Body weight(g):", y_pred)
    
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
    
@app.route('/dispenser', methods=["GET", "POST"])
def dispenser():
    global connection
    cursor = connection.cursor()
    sql = "use " + databaseName + ";"
    cursor.execute(sql)

    if request.method == "POST":
        try:
            field_ID = int(request.form.get("field_ID"))
            sql = "insert into dispenser(field_ID) value({})".format(field_ID)
            cursor.execute(sql)
        except:
            sql = "truncate dispenser;"
            cursor.execute(sql)

    sql = "select field_ID from field_logs;"
    cursor.execute(sql)
    fields_count = cursor.fetchall()
    sql = "select ff.field_ID, d.dispenser_ID from field_logs as ff inner join dispenser as d where ff.field_ID=d.field_ID order by field_ID, dispenser_ID;"
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
    page = render_template('dispenser.html', fields_count=fields_count, data=data, data_len=len(data))

    return page

@app.route('/test', methods=["GET", "POST"])
def test():
    global connection
    cursor = connection.cursor()
    sql = "use " + databaseName + ";"
    cursor.execute(sql)

    if request.method == "POST":
        field_ID = int(request.form.get("field_ID"))
        use_time = int(request.form.get("use_time"))
        dispenser_ID = int(request.form.get("dispenser_ID"))
        food_ID = request.form.get("food_ID")
        used = float(request.form.get("used"))
        print(field_ID, dispenser_ID, used)
        sql = 'insert into feeding_logs(dispenser_ID, use_time, food_ID, used, field_ID) values({}, {}, "{}", {}, {})'.format(dispenser_ID, use_time, food_ID, used, field_ID)
        cursor.execute(sql)
        return redirect(url_for("test"))


    sql = "select field_ID from field_logs;"
    cursor.execute(sql)
    fields_count = cursor.fetchall()
    page = render_template('test.html', fields_count=fields_count)

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

@app.route('/show', methods=["GET", "POST"])
def show():
    global connection
    cursor = connection.cursor()
    sql = "use " + databaseName + ";"
    cursor.execute(sql)
    
    sql = "select ff.field_ID, d.dispenser_ID, fl.feeding_time, fl.use_time, fl.food_ID, fl.used from field_logs as ff inner join dispenser as d inner join feeding_logs as fl where ff.field_ID=d.field_ID and d.dispenser_ID=fl.dispenser_ID order by fl.feeding_time desc;"
    cursor.execute(sql)
    data = list(cursor.fetchall())
    data = utc8(data, 2)
    
    sql = "select * from fcr order by end_time desc;"
    cursor.execute(sql)
    fcr = list(cursor.fetchall())
    fcr = utc8(fcr, 2)
    fcr = utc8(fcr, 3)
    
    if request.method == "POST":
        json_data = request.get_json("data")
        field_ID = int(json_data["field_ID"])
        print("receive POST", field_ID)
        if field_ID == 0:
            sql = "select * from field_logs;"
            cursor.execute(sql)
            fields_data = list(cursor.fetchall()) 
            fields_data = utc8(fields_data, 6)
            
            sql = "select field_ID from field_logs;"
            cursor.execute(sql)
            fields_count = cursor.fetchall()
            
        else:
            sql = "select * from field_logs where field_ID=" + str(field_ID) +";"
            cursor.execute(sql)
            fields_data = list(cursor.fetchall()) 
            fields_data = utc8(fields_data, 6)
            
            sql = "select field_ID from field_logs where field_ID=" + str(field_ID) +";"
            cursor.execute(sql)
            fields_count = cursor.fetchall()
            
        # print('POST fields_count', fields_count, 'fields_count', fields_data)
        data = {
            "fields_count": fields_count,
            "fields_data": fields_data
        }
        return data
    
    else:
        sql= "select * from field_logs"
        cursor.execute(sql)
        fields_data = list(cursor.fetchall()) 
        fields_data = utc8(fields_data, 6)
        
        sql = "select field_ID from field_logs;"
        cursor.execute(sql)
        fields_count_list = cursor.fetchall()
        fields_count = []
        [fields_count.append(x) for x in fields_count_list if x not in fields_count]
        
    page = render_template('show.html', fields_count=fields_count,fields_data=fields_data, data=data, fcr=fcr)
    return page   
    
@app.route('/update', methods=["GET", "POST"])
def update():
    global connection
    cursor = connection.cursor()
    sql = "use " + databaseName + ";"
    cursor.execute(sql)

    if request.method == "POST":   
        field_ID = int(request.form.get("field_ID"))
        
        if request.form["fcr"] == "":
            sql = "select fcr from field_logs where field_ID = "+str(field_ID)+" order by update_time desc;"
            cursor.execute(sql)
            fcr = cursor.fetchone()
            fcr = fcr[0]
        else:
            fcr=float(request.form["fcr"])
            
        if request.form["counts"] == "":
            sql = "select counts from field_logs where field_ID = "+str(field_ID)+" order by update_time desc;"
            cursor.execute(sql)
            counts = cursor.fetchone()
            counts = counts[0]
        else:
            counts=int(request.form["counts"])
            
        if request.form["dead_counts"] == "":
            dead_counts=0
        else:
            dead_counts=int(request.form["dead_counts"])
        
        if request.form["avg_weights"] == "":
            sql = "select * from field_logs where field_ID = "+str(field_ID)+" order by update_time desc;"
            cursor.execute(sql)
            fields_data = cursor.fetchone()
            avg_weights = "NULL" or None 
            estimated_avg_weights = fields_data[2] # estimated_avg_weights on last time
            fcr = fields_data[3]
            counts = fields_data[4]
            update_time = fields_data[6]
            cursor.execute(sql)
            sql = "select feeding_time, used from feeding_logs where field_ID = "+str(field_ID)+" order by feeding_time desc;"
            cursor.execute(sql)
            feeding_logs = list(cursor.fetchall())
            total_used = 0
            for i in range(len(feeding_logs)):
                feeding_time = feeding_logs[i][0]
                used = feeding_logs[i][1]
                if update_time < feeding_time:
                    total_used += used
            
            estimated_avg_weights = round(((counts*estimated_avg_weights)+(total_used/fcr))/(counts-dead_counts),2)

        else:
            avg_weights=float(request.form["avg_weights"])
            estimated_avg_weights=avg_weights
            
        sql = 'insert into field_logs (field_ID, avg_weights, estimated_avg_weights, fcr, counts, dead_counts, update_time) values({}, {}, {}, {}, {}, {}, "{}");'.format(field_ID, avg_weights, estimated_avg_weights, fcr, counts, dead_counts, datetime.datetime.now())
        cursor.execute(sql)
                
        return redirect(url_for("show"))

    sql = "select field_ID from field_logs;"
    cursor.execute(sql)
    fields_count = cursor.fetchall()
    page = render_template('update.html', fields_count=fields_count)
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
        field_ID = int(request.form["field_ID"])
        query_time = datetime.datetime.now()
        # target_weight = float(request.form["target_weight"])
        # daily_feed = float(request.form["daily_feed"])
        sql = "select update_time from field_logs where field_ID = "+str(field_ID)+" order by update_time asc;"
        cursor.execute(sql)
        first_time = cursor.fetchone()
        first_time = first_time[0]
        print(first_time)
        age = str((query_time-first_time).days)
        print("兩個日期相差了"+ age +"天")
        estimated_weights = preidict_weights(age)
        
        sql = "select spec from field_logs where field_ID = "+str(field_ID)+" order by update_time asc;"
        cursor.execute(sql)
        first_spec = cursor.fetchone()
        first_spec = first_spec[0]
        print(first_spec)
        sql = "select record_weights from field_logs where field_ID = "+str(field_ID)+" order by update_time asc;"
        cursor.execute(sql)
        first_weights = cursor.fetchone()
        first_weights = first_weights[0]
        print(first_weights)
        estimated_weights = round(estimated_weights * first_spec * first_weights / 1000, 2)
        
        estimated_date = preidict_date(estimated_weights)
        estimated_date = first_time + datetime.timedelta(days=int(estimated_date))
        print('estimated_date:', estimated_date)
        
        '''
        if request.form["avg_weights"] == '':
            sql = "select avg_weights from field_logs where field_ID = "+str(field_ID)+";"
            cursor.execute(sql)
            avg_weights = cursor.fetchone()
            avg_weights = avg_weights[0]
        else:
            avg_weights=float(request.form["avg_weights"])
        
        if request.form["fcr"] == '':
            sql = "select fcr from fcr where field_ID = "+str(field_ID)+" order by end_time desc;"
            cursor.execute(sql)           
            fcr = cursor.fetchone()
            fcr = fcr[0]
        else:
            fcr=float(request.form["fcr"])
            
        if request.form["counts"] == '':
            sql = "select counts from field_logs where field_ID = "+str(field_ID)+";"
            cursor.execute(sql)
            counts = cursor.fetchone()
            counts = counts[0]
        else:
            counts=int(request.form["counts"])
            
        if request.form["dead_counts"] == '':
            sql = "select dead_counts from field_logs where field_ID ="+str(field_ID)+";"
            cursor.execute(sql)
            dead_counts = cursor.fetchone()
            dead_counts = dead_counts[0]
        else:
            dead_counts=int(request.form["dead_counts"])
        
        '''
        
        sql = "select used from feeding_logs where field_ID = "+str(field_ID)+";"
        cursor.execute(sql)
        used = list(cursor.fetchall())
        total_used = 0
        for i in range(len(used)):
            total_used += used[i][0]
        total_used = total_used/1000
        print("total_used", total_used)
        
        # target_feed = (target_weight-avg_weights)*(counts-dead_counts)*fcr
        # estimated_feed = target_feed-total_used
        # estimated_days = estimated_feed/daily_feed
        # print("換肉率:", fcr, "\n目標均重(公克):", target_weight, "\n目前均重(公克):", avg_weights, "\n魚隻數量(隻):", counts, "\n魚隻死亡數量(隻):", dead_counts)
        # print("目標飼料量(公克):", target_feed, "\n已用飼料量(公克):", total_used, "\n每日飼料量(公克):", daily_feed, "\n預估天數(天):", estimated_days)

        estimated_fcr = round(total_used/(estimated_weights-first_weights), 2)
    query_result = render_template('query_result.html', age=int(age), estimated_date=estimated_date, estimated_weights=estimated_weights, estimated_fcr=estimated_fcr, total_used=total_used, first_weights=first_weights)
    # target_feed=target_feed, total_used=total_used, estimated_days=estimated_days, fcr=fcr, target_weight=target_weight, avg_weights=avg_weights, counts=counts, dead_counts=dead_counts, estimated_feed=estimated_feed, daily_feed=daily_feed)
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

@app.route('/feeding_logs', methods=["GET", "POST"])
def feeding_logs():
    page = render_template('feeding_logs.html')
    return page   

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
