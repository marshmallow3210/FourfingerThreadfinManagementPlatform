import pymysql
import datetime
import time

# 連接到資料庫
connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='lab403',
                             password='66386638',
                             database='fishDB',
                             autocommit=True)
cursor = connection.cursor()

# 定義 weight 序列和當前索引
weight_sequence = [100, 30, 20, 40, 90, 50, 60, 70, 80]
current_index = 0

def generate_data():
    global current_index
    
    # 從序列中獲取 weight 值
    current_weight = weight_sequence[current_index]
    
    # 更新索引
    current_index += 1
    
    # 如果超出序列長度，循環到開頭
    if current_index >= len(weight_sequence):
        current_index = 0
        weight_sequence.extend([weight_sequence[-1] + 10])  # 在序列中添加新的 weight 值

    # 創建數據字典
    data = {
        'weight': current_weight,
        'laser': 10.50,
        'blower_state': 'on',
        'angle_state': 60,
        'speed_level': 600,
        'system_mode': 1,
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'dispenser_ID': 1
    }
    
    return data

def upload_to_ESP32(data):
    sql = """
    INSERT INTO ESP32 (weight, laser, blower_state, angle_state, speed_level, system_mode, time, date, dispenser_ID)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(sql, (data['weight'], data['laser'], data['blower_state'], data['angle_state'], data['speed_level'], data['system_mode'], data['time'], data['date'], data['dispenser_ID']))
    print('Data uploaded to ESP32:', data)

def main():
    while True:
        data = generate_data()
        upload_to_ESP32(data)
        time.sleep(30)

if __name__ == '__main__':
    main()