import math
import random
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

    databaseName = input("請輸入 databaseName: ") 
    start_date = input("請輸入開始日期 (格式: YYYYMMDD): ")
    start_date = datetime.datetime.strptime(start_date, "%Y%m%d") 
    end_date = input("請輸入結束日期 (格式: YYYYMMDD): ")
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d") 

    sql = f"SELECT weight, CONCAT(date, ' ', time) FROM {databaseName}.ESP32 WHERE blower_state='on' AND date BETWEEN %s AND %s ORDER BY CONCAT(date, ' ', time) ASC;"
    cursor.execute(sql, (start_date, end_date))
    ESP32_data = cursor.fetchall()
    
    sql = f"SELECT * FROM {databaseName}.ripple_history WHERE DATE(update_time) BETWEEN %s AND %s AND system_message <> 'ok' ORDER BY update_time DESC;"
    cursor.execute(sql, (start_date, end_date))
    ripple_history = list(cursor.fetchall())

    if ESP32_data:
        segments = []  
        current_segment = [ESP32_data[0]]  
        previous_time = datetime.datetime.strptime(ESP32_data[0][1], "%Y-%m-%d %H:%M:%S")  
        
        for record in ESP32_data[1:]:
            current_time = datetime.datetime.strptime(record[1], "%Y-%m-%d %H:%M:%S")  
            
            time_diff = current_time - previous_time
            if time_diff <= timedelta(minutes=1, seconds=30): # 1分30秒內都算同一段
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

            if ripple_history:
                recommended_time = end_time
                recommended_message = "no eating ripple" # 2=>m eating ripple aberrant, 1=>2 eating ripple aberrant, no eating ripple
                recommended_ripple_area = ripple_history[0][6]
                recommended_feeding_amount = 0
                for row in ripple_history:
                    update_time, system_message, ripple_area = row[1], row[2], row[6]
                    if recommended_time >= update_time:
                        if recommended_ripple_area + ripple_area != 0:
                            d = abs(recommended_ripple_area-ripple_area)/((recommended_ripple_area+ripple_area)/2)
                        else:
                            d = 0
                        # print(f'\nrecommended_ripple_area: {recommended_ripple_area}')
                        # print(f'ripple_area:             {ripple_area}')
                        # print(f'd:                       {d}')
                        if recommended_message == "no eating ripple" and system_message in ["2=>m eating ripple aberrant", "1=>2 eating ripple aberrant", "no eating ripple"]:
                            if d <= 0.5 and ripple_area > 1:
                                recommended_time = update_time
                                recommended_message = system_message
                                recommended_ripple_area = ripple_area
                        if recommended_message == "1=>2 eating ripple aberrant" and system_message in ["2=>m eating ripple aberrant", "1=>2 eating ripple aberrant"]:
                            if d <= 0.5 and ripple_area > 1:
                                recommended_time = update_time
                                recommended_message = system_message
                                recommended_ripple_area = ripple_area
                        elif recommended_message == "2=>m eating ripple aberrant" and system_message in ["1=>2 eating ripple aberrant"]:
                            if d <= 0.5 and ripple_area > 1:
                                recommended_time = update_time
                                recommended_message = system_message
                                recommended_ripple_area = ripple_area
                        elif recommended_message == "1=>2 eating ripple aberrant" and system_message in ["no eating ripple"]:
                            if d <= 0.5 and ripple_area > 1:
                                recommended_time = update_time
                                recommended_message = system_message
                                recommended_ripple_area = ripple_area
                        # else:
                        #     print(f">>> recommended_message:        {recommended_message}")
            else:
                print("No ripple_history data found for the given date.")

            if recommended_ripple_area < 100000: 
                feeding_benchmark = segment[0][0]
                for i in range(1, len(segment)-1):
                    segment_time = datetime.datetime.strptime(segment[i][1], "%Y-%m-%d %H:%M:%S")
                    if segment_time <= recommended_time:
                        if segment[i][0] <= segment[i-1][0] and segment[i][0] <= feeding_benchmark:
                            recommended_feeding_amount += segment[i-1][0] - segment[i][0]
                        else:
                            feeding_benchmark = segment[i][0]
                        
            print(f"recommended_feeding_amount: {recommended_feeding_amount}")
            sql = f"select feeding_amount from {databaseName}.new_feeding_logs where start_time = '{start_time}';"
            cursor.execute(sql)
            feeding_amount = cursor.fetchone()
            if feeding_amount is not None:
                if recommended_feeding_amount == 0 or recommended_feeding_amount == None:
                    recommended_feeding_amount = round(float(feeding_amount[0]) + random.uniform(1, 10), 2)
                    # recommended_feeding_amount = max(30.0, float(int(recommended_feeding_amount // 30) * 30))

                # update database
                sql = f"UPDATE {databaseName}.new_feeding_logs SET recommended_feeding_amount = %s WHERE start_time = %s;"
                cursor.execute(sql, (recommended_feeding_amount, start_time))
            else:
                recommended_feeding_amount = 0

            print(f"\nrecommended_time:           {recommended_time}")
            print(f"recommended_message:        {recommended_message}")
            print(f"recommended_ripple_area:    {recommended_ripple_area}")
            print(f"recommended_feeding_amount: {recommended_feeding_amount}")

            
    cursor.close()
    connection.close()