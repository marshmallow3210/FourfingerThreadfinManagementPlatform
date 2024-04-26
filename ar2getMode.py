'''
check mode from decision in background and get data from ESP32 to feeding_logs
'''
import threading
import pymysql
import time
import datetime

# 創建 Lock 物件，用於同步訪問全局變數
lock = threading.Lock()

connection = pymysql.connect(host='127.0.0.1',
                            port=3306,
                            user='lab403',
                            password='66386638',
                            autocommit=True)

databaseName = "ar2DB"
mode = 0
switchMode = 1
start_time_fromESP32 = None
start_time_temp = None

def getMode():
    global databaseName
    global mode
    global switchMode
    global start_time_fromESP32
    global start_time_temp
    global connection
    cursor = connection.cursor()
    cursor.execute("USE {};".format(databaseName))

    global cnt 
    cnt = 0

    # check if feeding
    while True:
        cnt += 1
        print(cnt)
        cursor.execute("SELECT mode FROM decision")
        result = cursor.fetchone()
        
        if result is not None:
            with lock:  # 使用 Lock 來保護全局變數
                mode = int(result[0])
            print(f'mode: {mode} switchMode: {switchMode}')

            if mode != 0 and switchMode == 1: # 開啟投餌機時
                start_time_temp = getStartTime()
                with lock: 
                    switchMode = 0

                if start_time_fromESP32 is None:
                    start_time_fromESP32 = start_time_temp

                print("dispenser is feeding, getStartTime:", start_time_fromESP32)

            elif mode == 0 and switchMode == 0: # 結束投餌時
                getDataFromESP32(start_time_fromESP32)
                with lock: 
                    switchMode = 1

                print("dispenser finished feeding, getDataFromESP32")

        time.sleep(10)  # 600 sec = 10 min

def getStartTime():
    global mode
    global switchMode
    global start_time_fromESP32
    global start_time_temp

    with lock:
        if mode != 0 and switchMode == 1: # 開啟投餌機時
            cursor = connection.cursor()
            sql = "use " + databaseName + ";"
            cursor.execute(sql)

            sql = "SELECT CONCAT(date, ' ', time) FROM ESP32 ORDER BY CONCAT(date, ' ', time) DESC LIMIT 1;"
            cursor.execute(sql)
            start_time = cursor.fetchone()
            start_time = start_time[0]
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

            switchMode = 0
            return start_time

def getDataFromESP32(start_time):
    global databaseName
    global mode
    global switchMode
    global start_time_fromESP32
    global start_time_temp
    global connection
    
    with lock:
        if mode == 0 and switchMode == 0: # 結束投餌時
            cursor = connection.cursor()
            sql = "use " + databaseName + ";"
            cursor.execute(sql)

            # get end_time
            sql = "SELECT CONCAT(date, ' ', time) FROM ESP32 ORDER BY CONCAT(date, ' ', time) DESC LIMIT 1;"
            cursor.execute(sql)
            end_time = cursor.fetchone()
            end_time = end_time[0]
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

            use_time = end_time - start_time
            use_time = use_time.total_seconds() / 60
            use_time = round(use_time, 2)
            print(f'use_time: {use_time} min')

            # counting feeding_amount
            
            sql = f"SELECT COUNT(*) AS feeding_count FROM ESP32 WHERE CONCAT(date, ' ', time) >= '{str(start_time)}' AND CONCAT(date, ' ', time) <= '{str(end_time)}';"
            cursor.execute(sql)
            feeding_count = list(cursor.fetchall())
            feeding_count = int(feeding_count[0][0])

            sql = f"SELECT weight FROM ESP32 WHERE CONCAT(date, ' ', time) >= '{str(start_time)}' AND CONCAT(date, ' ', time) <= '{str(end_time)}';"
            cursor.execute(sql)
            weight = list(cursor.fetchall())
            print(weight)

            feeding_amount = 0
            feeding_benchmark = weight[0][0]
            for i in range(1, feeding_count):
                if weight[i][0] <= weight[i-1][0] and weight[i][0] <= feeding_benchmark:
                    feeding_amount = feeding_amount + (weight[i-1][0] - weight[i][0])
                else:
                    feeding_benchmark = weight[i][0]
            print('feeding_benchmark:', feeding_benchmark)
            print('feeding_amount:', feeding_amount)

            
            sql = f"INSERT INTO feeding_logs (start_time, use_time, feeding_amount) VALUES ('{str(start_time)}', {use_time}, {feeding_amount});"
            cursor.execute(sql)

            switchMode = 1
            start_time_fromESP32 = None

if __name__ == "__main__":
    background_thread = threading.Thread(target=getMode)
    background_thread.start()
