import pymysql
import datetime
from datetime import timedelta

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

if __name__ == "__main__":
    cursor = connection.cursor()

    # 場域設定
    databaseName = input("請輸入 databaseName: ") # "fishDB"
    aquarium_id = input("請輸入 aquarium_id: ") # "144" 
    food_name = input("請輸入 food_name: ") # "測試"
    query_date = input("請輸入 query_date (格式: YYYY-MM-DD): ")

    new_feeding_logs = []

    sql = f"SELECT weight, CONCAT(date, ' ', time) FROM {databaseName}.ESP32 WHERE blower_state='on' AND date = %s ORDER BY CONCAT(date, ' ', time) ASC;"
    cursor.execute(sql, (query_date,))
    ESP32_data = cursor.fetchall()
    
    sql = f"SELECT * FROM {databaseName}.ripple_history WHERE DATE(update_time) = %s AND system_message <> 'ok' ORDER BY update_time DESC;"
    cursor.execute(sql, (query_date,))
    ripple_history = list(cursor.fetchall())

    if ESP32_data:
        segments = []  
        current_segment = [ESP32_data[0]]  
        previous_time = datetime.datetime.strptime(ESP32_data[0][1], "%Y-%m-%d %H:%M:%S")  
        
        for record in ESP32_data[1:]:
            current_time = datetime.datetime.strptime(record[1], "%Y-%m-%d %H:%M:%S")  
            
            time_diff = current_time - previous_time
            if time_diff <= timedelta(minutes=10): # 10分鐘內都算同一段
                current_segment.append(record)
            else:
                segments.append(current_segment)
                current_segment = [record]
            
            previous_time = current_time
        
        segments.append(current_segment)
        
        for idx, segment in enumerate(segments):
            print(f"\nfeeding segment {idx+1}:")
            start_time = segment[0][1]
            end_time = segment[-1][1]
            print(f"start_time: {start_time}")
            print(f"end_time:   {end_time}")
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")  

            suggest_time = end_time
            suggest_message = "no eating ripple" # 2=>m eating ripple aberrant, 1=>2 eating ripple aberrant, no eating ripple
            suggest_ripple_area = 100000.0

            if ripple_history:
                for row in ripple_history:
                    update_time = row[1] 
                    system_message = row[2] 
                    ripple_area = row[6]
                    if end_time >= update_time:
                        if suggest_message == "no eating ripple" and (system_message == "2=>m eating ripple aberrant" or system_message == "1=>2 eating ripple aberrant" or system_message == "no eating ripple"):
                            if suggest_ripple_area >= ripple_area and ripple_area > 1:
                                suggest_time = update_time
                                suggest_message = system_message
                                suggest_ripple_area = ripple_area
                        if suggest_message == "1=>2 eating ripple aberrant" and (system_message == "2=>m eating ripple aberrant" or system_message == "1=>2 eating ripple aberrant"):
                            if suggest_ripple_area >= ripple_area and ripple_area > 1:
                                suggest_time = update_time
                                suggest_message = system_message
                                suggest_ripple_area = ripple_area
                        elif suggest_message == "2=>m eating ripple aberrant" and system_message == "1=>2 eating ripple aberrant":
                            if (abs(suggest_ripple_area-ripple_area)/((suggest_ripple_area+ripple_area)/2))*100<=5 and ripple_area > 1:
                                suggest_time = update_time
                                suggest_message = system_message
                                suggest_ripple_area = ripple_area
                        elif suggest_message == "1=>2 eating ripple aberrant" and system_message == "no eating ripple":
                            if (abs(suggest_ripple_area-ripple_area)/((suggest_ripple_area+ripple_area)/2))*100<=5 and ripple_area > 1:
                                suggest_time = update_time
                                suggest_message = system_message
                                suggest_ripple_area = ripple_area
                        else:
                            print(f"update_time:        {update_time}")
                            print(f"system_message:     {system_message}")
                            print(f"ripple_area:        {ripple_area}")
            else:
                print("No ripple_history data found for the given date.")

            feeding_amount = 0
            feeding_benchmark = segment[0][0]
            for i in range(1, len(segment)):
                segment_time = datetime.datetime.strptime(segment[i][1], "%Y-%m-%d %H:%M:%S")
                if segment_time <= suggest_time:
                    if segment[i][0] <= segment[i-1][0] and segment[i][0] <= feeding_benchmark:
                        feeding_amount += segment[i-1][0] - segment[i][0]
                    else:
                        feeding_benchmark = segment[i][0]
                        
            print(f"\nsegment_time:               {segment_time}")
            print(f"suggest_time:               {suggest_time}")
            print(f"suggest_message:            {suggest_message}")
            print(f"suggest_ripple_area:        {suggest_ripple_area}")
            print(f"feeding_benchmark:          {feeding_benchmark}")
            print(f"feeding_amount:             {feeding_amount}")
            left_amount = segment[-1][0]
            print(f"left_amount:                {left_amount}")
                
            food_id_map = {
                "測試": 39,         # fishDB
                "海洋牌": 40,       # ar2DB
                "漢神牌": 41,       # ar4DB
                "海洋飼料": 42      # ar3DB
            }
            food_id = food_id_map.get(food_name, 39)

            # insert to database
            # sql = f"INSERT INTO {databaseName}.new_feeding_logs (journal_id, start_time, use_time, food_id, food_name, feeding_amount, left_amount, status, description) VALUES (0, '{str(start_time)}', {use_time}, {food_id}, '{str(food_name)}', {feeding_amount}, {left_amount}, 'good', '網路斷線重新上傳');"
            # cursor.execute(sql)
            
    cursor.close()
    connection.close()