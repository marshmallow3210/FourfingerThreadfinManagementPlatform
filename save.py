import pandas as pd
import mysql.connector
import os

connection = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='lab403',
    password='66386638',
)

databases = [f"ar{i}DB" for i in range(8) if i != 5]  # 跳過 ar5DB
tables = ['ripple_history'] # 'new_feeding_logs', 'original_feeding_logs', 'field_logs'

try:
    for db in databases:
        for table in tables:
            query = f"SELECT * FROM {db}.{table}"
            try:
                data = pd.read_sql(query, connection)
                # data['start_time'] = pd.to_datetime(data['start_time'])
                output_file = os.path.join(f"{db}_{table}.xlsx")
                data.to_excel(output_file, index=False, engine="openpyxl")
                print(f"成功匯出：{output_file}")
            except Exception as e:
                print(f"匯出失敗 - 資料庫：{db}，資料表：{table}，錯誤：{e}")
finally:
    connection.close()
