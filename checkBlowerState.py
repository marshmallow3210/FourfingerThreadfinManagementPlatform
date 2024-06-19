'''
check blower_state from ESP32 in background and get data from ESP32 to feeding_logs
'''
import threading
import pymysql
import time
import base64
import hashlib
import hmac
import json
import uuid
import datetime
from datetime import timedelta
import requests

# 創建 Lock 物件，用於同步訪問全局變數
lock = threading.Lock()

connection = pymysql.connect(host='127.0.0.1',
                            port=3306,
                            user='lab403',
                            password='66386638',
                            autocommit=True)

databaseName = "fishDB"
aquarium_id = "144" 
food_name = "測試"

blower_state = 'off'
switchMode = 1
start_time_fromESP32 = None
start_time_temp = None


''' date format setting ''' 
def utc8(utc, p):
    for i in range(0, len(utc)):
        if utc[i][p] != None:
            utc[i] = list(utc[i])
            utc[i][p]=utc[i][p].astimezone(datetime.timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")

    return utc


''' API integration'''
def convert_to_unix_timestamp(datetime_str):
    dt_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    timestamp = int(dt_obj.timestamp() * 1000) # 計算 Unix timestamp (以秒為單位 = 毫秒*1000)
    return timestamp

def generate_signature(api_key, api_endpoint, request_body, nonce):
    message = api_key + api_endpoint + request_body + nonce # according to API Authentication from API key document
    signature = hmac.new(bytes(api_key,'utf-8'), bytes(message,'utf-8'), hashlib.sha256).hexdigest().encode('utf-8')
    return base64.b64encode(signature).decode('utf-8')

# create data version
def send_data():
    print("\nstart to sending data")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = convert_to_unix_timestamp(current_time)
    
    # get data from database
    global connection
    cursor = connection.cursor()
    
    sql = f"select journal_id, pool_id, start_time, use_time, food_id, food_name, food_unit, feeding_amount, left_amount, status, description from {databaseName}.new_feeding_logs order by start_time desc limit 1;"
    cursor.execute(sql)
    feeding_logs = list(cursor.fetchall())
    print('feeding_logs:', feeding_logs)
                        
    action = "create"                               
    journal_id = 0

    food_id_map = {
        "測試": 39,         # fishDB
        "海洋牌": 40,       # ar2DB
        "漢神牌": 41,       # ar4DB
        "海洋飼料": 42      # ar3DB
    }
    food_id = food_id_map.get(food_name, 39)

    feeding_amount = feeding_logs[0][7]             
    food_unit = str(feeding_logs[0][6])  

    start_time = utc8(feeding_logs, 2) 
    start_time = start_time[0][2]
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
            response_data  = response.json()
            if 'data' in response_data and 'journal' in response_data['data'] and 'id' in response_data['data']['journal']:
                journal_id = response_data['data']['journal']['id']
                print("Response journal_id is:", journal_id)
                sql = f"update {databaseName}.new_feeding_logs set journal_id = {journal_id} order by start_time desc limit 1;"
                cursor.execute(sql)
            else:
                print("Error: Cannot find journal id in response data.")
        else:
            print("Unexpected status code:", response.status_code)
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

    return 


''' check blower_state from ESP32 in background and get data from ESP32 to feeding_logs '''
def getStartTime():
    global blower_state
    global switchMode
    global start_time_fromESP32
    global start_time_temp
    global connection

    with lock:
        if blower_state != 'off' and switchMode == 1: # 開啟投餌機時
            cursor = connection.cursor()
            sql = f"SELECT CONCAT(date, ' ', time) FROM {databaseName}.ESP32 ORDER BY CONCAT(date, ' ', time) DESC LIMIT 1;"
            cursor.execute(sql)
            start_time = cursor.fetchone()
            if start_time:
                start_time = start_time[0]
                start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                switchMode = 0
                return start_time
            else:
                print("cannot get the start_time")
                return None

def getDataFromESP32(start_time, description):
    global blower_state
    global switchMode
    global start_time_fromESP32
    global start_time_temp
    global connection
    
    with lock:
        if blower_state == 'off' and switchMode == 0: # 結束投餌時
            cursor = connection.cursor()

            # get end_time
            sql = f"SELECT CONCAT(date, ' ', time) FROM {databaseName}.ESP32 ORDER BY CONCAT(date, ' ', time) DESC LIMIT 1;"
            cursor.execute(sql)
            end_time = cursor.fetchone()
            end_time = end_time[0]
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

            use_time = end_time - start_time
            use_time = use_time.total_seconds() / 60
            use_time = round(use_time, 2)
            print(f'use_time: {use_time} min')

            # counting feeding_amount
            sql = f"SELECT COUNT(*) AS feeding_count FROM {databaseName}.ESP32 WHERE CONCAT(date, ' ', time) >= '{str(start_time)}' AND CONCAT(date, ' ', time) <= '{str(end_time)}';"
            cursor.execute(sql)
            feeding_count = cursor.fetchone()[0]
            
            sql = f"SELECT weight FROM {databaseName}.ESP32 WHERE CONCAT(date, ' ', time) >= '{str(start_time)}' AND CONCAT(date, ' ', time) <= '{str(end_time)}';"
            cursor.execute(sql)
            weight = [row[0] for row in cursor.fetchall()]
            print('weight:', weight)

            feeding_amount = 0
            if weight:
                feeding_benchmark = weight[0]
                for i in range(1, feeding_count):
                    if weight[i] <= weight[i-1] and weight[i] <= feeding_benchmark:
                        feeding_amount += weight[i-1] - weight[i]
                    else:
                        feeding_benchmark = weight[i]
                print('feeding_benchmark:', feeding_benchmark)
                print('feeding_amount:', feeding_amount)
                left_amount = weight[-1]
                print('left_amount', left_amount)
            else:
                print("The weight list is empty.")
                left_amount = 0 
            
            # insert to database
            sql = f"INSERT INTO {databaseName}.new_feeding_logs (journal_id, start_time, use_time, feeding_amount, left_amount, description) VALUES (0, '{str(start_time)}', {use_time}, {feeding_amount}, {left_amount}, '{str(description)}');"
            cursor.execute(sql)

            # api integration
            send_data()
            print("send_data finished!")

            switchMode = 1
            start_time_fromESP32 = None

def checkBlowerState():
    global databaseName
    global blower_state
    global switchMode
    global start_time_fromESP32
    global start_time_temp
    global connection

    # check if feeding
    while True:
        cursor = connection.cursor()
        
        current_time = datetime.datetime.now()

        cursor.execute(f"SELECT CONCAT(date, ' ', time) AS datetime_str FROM {databaseName}.ESP32 ORDER BY CONCAT(date, ' ', time) DESC LIMIT 1;")
        latest_time = cursor.fetchone()
        latest_time = latest_time[0]
        latest_time = datetime.datetime.strptime(latest_time, '%Y-%m-%d %H:%M:%S')
        time_difference = current_time - latest_time
        print(f'blower_state: {blower_state}, switchMode: {switchMode}, time_difference: {time_difference.total_seconds()} sec')
        
        # 用ESP32最新紀錄的時間是否在現在時間的一小時內來檢查投餌機是否正常運作
        if time_difference.total_seconds() <= 31:            
            cursor.execute(f"SELECT blower_state FROM {databaseName}.ESP32 ORDER BY CONCAT(date, ' ', time) DESC LIMIT 1;")
            result = cursor.fetchone()
            if result:
                with lock:  # 使用 Lock 來保護全局變數
                    blower_state = result[0]

                # 開啟投餌機時
                if blower_state != 'off' and switchMode == 1: 
                    start_time_temp = getStartTime()
                    with lock: 
                        switchMode = 0

                    if start_time_fromESP32 is None:
                        start_time_fromESP32 = start_time_temp

                    print(f"dispenser is feeding, getStartTime: {start_time_fromESP32}")

                # 結束投餌時
                elif blower_state == 'off' and switchMode == 0: 
                    print("dispenser finished feeding, getDataFromESP32")
                    getDataFromESP32(start_time_fromESP32, "")
                    with lock: 
                        switchMode = 1

        # 超過一小時內，投餌機未正常運作
        else:
            print(f"投餌機未正常運作! ESP32 最新紀錄的時間: {latest_time} 距離現在時間: {current_time} 已超過一小時")
            
            # set blower_state = 'off' and getDataFromESP32 and set switchMode = 1
            cursor.execute(f"UPDATE {databaseName}.ESP32 SET blower_state = 'off' ORDER BY CONCAT(date, ' ', time) DESC LIMIT 1;")    
            blower_state = 'off'
            getDataFromESP32(start_time_fromESP32, "投餌機未正常運作")
            with lock: 
                switchMode = 1
                
            # print("ending to check blower_state...")
            # break
        
        time.sleep(30) 


if __name__ == "__main__":
    background_thread = threading.Thread(target=checkBlowerState)
    background_thread.start()
