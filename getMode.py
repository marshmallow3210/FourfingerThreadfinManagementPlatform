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

databaseName = "fishDB"
mode = 0
switchMode = 0

def getMode():
    global databaseName
    global mode
    global switchMode
    global connection
    cursor = connection.cursor()
    sql = "use " + databaseName + ";"
    cursor.execute(sql)

    # check if feeding
    while True:
        cursor.execute("SELECT mode FROM decision")
        result = cursor.fetchone()
        if result is not None:
            with lock:  # 使用 Lock 來保護全局變數
                mode = result[0]
            print(mode)

        if mode == 0:
            getDataFromESP32(start_time)
            with lock: 
                switchMode = 1
            print("dispensers are not feeding, getDataFromESP32")
        else:
            start_time = getStartTime()
            with lock: 
                switchMode = 0
            print("dispensers are feeding, getStartTime:", start_time)

        time.sleep(600)  # 600 sec = 10 min

def getStartTime():
    global switchMode # 確保 switchMode 在函數中被識別為一個 global variable
    with lock:
        if mode != 0 and switchMode == 1:
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
    global switchMode # 確保 switchMode 在函數中被識別為一個 global variable
    with lock:
        if mode == 0 and switchMode == 0:
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
            print('use_time:', use_time)

            # counting feeding_amount
            sql = "SELECT COUNT(*) AS feeding_count FROM ESP32 WHERE CONCAT(date, ' ', time) >= " + start_time + "AND CONCAT(date, ' ', time) <= " + end_time + ";"
            cursor.execute(sql)
            feeding_count = list(cursor.fetchall())
            feeding_count = int(feeding_count[0][0])

            sql = "SELECT weight FROM ESP32 WHERE CONCAT(date, ' ', time) >= " + start_time + "AND CONCAT(date, ' ', time) <= " + end_time + ";"
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

            sql = 'insert into feeding_logs (start_time, use_time, feeding_amount) values("{}", {}, {});'.format(start_time, use_time, feeding_amount)
            cursor.execute(sql)

            switchMode = 1

if __name__ == "__main__":
    background_thread = threading.Thread(target=getMode)
    background_thread.start()
