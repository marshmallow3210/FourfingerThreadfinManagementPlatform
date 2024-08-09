import pymysql
import base64
import hashlib
import hmac
import json
import uuid
import datetime
from datetime import timedelta
import requests

connection = pymysql.connect(host='127.0.0.1',
                            port=3306,
                            user='lab403',
                            password='66386638',
                            autocommit=True)


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
def send_data(start_time):
    print("\nstart to sending data")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = convert_to_unix_timestamp(current_time)
    
    # get data from database
    global connection
    cursor = connection.cursor()
    
    sql = f"SELECT journal_id, pool_id, start_time, use_time, food_id, food_name, food_unit, feeding_amount, left_amount, status, description FROM {databaseName}.new_feeding_logs WHERE start_time = %s;"
    cursor.execute(sql, (start_time,))
    feeding_logs = list(cursor.fetchall())
    print('feeding_logs:', feeding_logs)
                        
    action = "create"                               
    journal_id = 0

    food_id = feeding_logs[0][4]
    feeding_amount = feeding_logs[0][7]             
    food_unit = str(feeding_logs[0][6])  
    food_name = str(feeding_logs[0][5]) 

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


''' reupload ESP32 data to new_feeding_logs '''
if __name__ == "__main__":
    cursor = connection.cursor()

    # 場域設定
    databaseName = input("請輸入 databaseName: ") # "fishDB"
    aquarium_id = input("請輸入 aquarium_id: ") # "144" 
    food_name = input("請輸入 food_name: ") # "測試"
    query_date = input("請輸入 query_date (格式: YYYY-MM-DD): ")
    new_feeding_logs = []

    sql = f"SELECT * FROM {databaseName}.ESP32 WHERE date = %s ORDER BY CONCAT(date, ' ', time) ASC;"
    cursor.execute(sql, (query_date,))
    rows = cursor.fetchall()
    
    for row in rows:
        columns = list(row)
        blower_state = columns[2].strip()

        # 轉換 timedelta 為 HH:MM:SS 格式
        time_delta = columns[6]
        total_seconds = int(time_delta.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

        # 組合日期和時間字串
        timestamp_str = f"{columns[7]} {time_str}"
        timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        print(f"timestamp: {timestamp}, blower_state: {blower_state}")
        
        if blower_state == "off":
            if new_feeding_logs != []:
                start_time = new_feeding_logs[0][0]
                end_time = new_feeding_logs[-1][0]

                use_time = end_time - start_time
                use_time = use_time.total_seconds() / 60
                use_time = round(use_time, 2)

                # counting feeding_amount 
                weight = [float(log[1]) for log in new_feeding_logs]
                print(f"weight: {weight}")
                feeding_amount = 0
                if weight:
                    feeding_benchmark = weight[0]
                    for i in range(1, len(weight)):
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
                
                food_id_map = {
                    "測試": 39,         # fishDB
                    "海洋牌": 40,       # ar2DB
                    "漢神牌": 41,       # ar4DB
                    "海洋飼料": 42      # ar3DB
                }
                food_id = food_id_map.get(food_name, 39)

                # insert to database
                sql = f"INSERT INTO {databaseName}.new_feeding_logs (journal_id, start_time, use_time, food_id, food_name, feeding_amount, left_amount, status, description) VALUES (0, '{str(start_time)}', {use_time}, {food_id}, '{str(food_name)}', {feeding_amount}, {left_amount}, 'good', '網路斷線重新上傳');"
                cursor.execute(sql)

                # api integration, 午仔魚的場域不用
                send_data(str(start_time))
                print("send_data finished!\n")

                # reset new_feeding_logs
                new_feeding_logs=[]
            else:
                print(f'new_feeding_logs is empty')
        else:
            new_feeding_logs.append([timestamp, columns[0]])
            print(new_feeding_logs)
            
    cursor.close()
    connection.close()