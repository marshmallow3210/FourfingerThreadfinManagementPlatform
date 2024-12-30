import base64
from collections import defaultdict
import hashlib
import hmac
import io
import json
import math
import pandas as pd
import uuid
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from matplotlib import patches, pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_cors import CORS
import pymysql
import datetime
from datetime import timezone, timedelta
import numpy as np
import requests
from scipy import stats
from sklearn.neighbors import KNeighborsRegressor
from datetime import timedelta
from scipy.signal import medfilt


connection = pymysql.connect(host='127.0.0.1',
                            port=3306,
                            user='lab403',
                            password='66386638',
                            autocommit=True)


def generate_heatmap(result, query_date, duration):
    if len(result) == 0:
        print("Error: ripple_result is empty")
        return None
    
    df = pd.DataFrame(result, columns=['update_time', 'ripple_area'])
    if df.empty:
        print("Error: DataFrame is empty")
        return None
    
    df['update_time'] = pd.to_datetime(df['update_time'])
    df['date'] = df['update_time'].dt.date
    df['minute'] = df['update_time'].dt.floor('T')
    df_grouped = df.groupby(['date', 'minute']).mean().reset_index()

    # 開根號
    df_grouped['ripple_area'] = np.sqrt(df_grouped['ripple_area'])

    heatmap_data = np.full((24 * 60, duration), np.nan)  # 24小時 x 60分鐘 x duration 天
    for _, row in df_grouped.iterrows():
        day_index = (row['date'] - query_date.date()).days
        minute_of_day = row['minute'].hour * 60 + row['minute'].minute
        heatmap_data[minute_of_day, day_index] = row['ripple_area']

    marks = []
    start_time = df.iloc[0]['update_time']
    prev_time = start_time

    for i in range(1, len(df)):
        current_time = df.iloc[i]['update_time']
        
        time_diff = (current_time - prev_time).total_seconds() / 60 

        if time_diff > 2:  # 如果時間差大於 1 分鐘
            marks.append({'start_time': start_time, 'end_time': prev_time})
            start_time = current_time  

        prev_time = current_time

    marks.append({'start_time': start_time, 'end_time': prev_time})

    fig, axes = plt.subplots(1, duration, figsize=(math.ceil(duration * 2) if duration >= 60 else (130 if duration >= 30 else 15), 26 if duration >= 60 else (40 if duration >= 30 else 10)), sharey=True, constrained_layout=True, dpi=50) 
    cmap = plt.get_cmap('hot')
    cmap.set_bad(color='black')  # 設置 np.nan 部分為黑色
    
    for i in range(duration):
        day_data = heatmap_data[:, i].reshape(-1, 1)
        ax = axes[i]
        im = ax.imshow(day_data, cmap=cmap, aspect='auto', vmin=0, vmax=np.nanmax(heatmap_data))

        ax.set_title((query_date + timedelta(days=i)).strftime('%-m/%-d'), fontsize = 64 if duration >= 60 else (110 if duration >= 30 else 20))
        ax.set_xticks([]) 
        ax.set_yticks(range(0, 24 * 60, 120))
        ax.set_yticklabels([f"{j:02d}:00" for j in range(0, 24, 2)])
        ax.tick_params(axis='y', labelsize = 64 if duration >= 60 else (100 if duration >= 30 else 20))
        
        # 畫框
        for mark in marks:
            start_minute = (mark['start_time'].hour * 60) + mark['start_time'].minute
            end_minute = (mark['end_time'].hour * 60) + mark['end_time'].minute

            if mark['start_time'].date() == (query_date + timedelta(days=i)).date():
                rect_y = start_minute -5 # 5 min
                rect_height = (end_minute - start_minute) + 10

                rect = patches.Rectangle(
                    (-0.5, rect_y),     # 左下角座標 (x, y)
                    1,                  # 矩形寬度
                    rect_height,        # 矩形高度
                    linewidth=2,
                    edgecolor='white',
                    facecolor='none'    # 只顯示邊框
                )
                ax.add_patch(rect)

    # plt.tight_layout(rect=[0, 0, 1.05, 0.995])  
    
    cbar = plt.colorbar(im, ax=axes.ravel().tolist(), aspect=50, pad=0.01)
    cbar.set_label('Pixel Number of Water Splashes', fontsize = 64 if duration >= 60 else (90 if duration >= 30 else 20))
    cbar.ax.tick_params(labelsize=56 if duration >= 60 else (100 if duration >= 30 else 16))

    save_path = f"heatmap_{query_date.strftime('%Y%m%d')}_{duration}.png"
    plt.savefig(save_path, format='png')
    print(f"Heatmap saved to {save_path}")
    plt.close(fig)

    return save_path

def counting_first_thd_idx_4_test(feeding_result, ripple_result):
    alpha = 0.01            # T 檢驗顯著性水平
    windows_minutes = 25    # 滑動窗口大小
    t3 = 5                  # 最小分析時間
    odd_windows_size = 7     # 中值濾波窗口大小

    first_thd_idx_4_test = [] # 儲存第一次水花顯著下降的索引

    total = len(feeding_result)
    for idx, (start_time, use_time) in enumerate(feeding_result):
        t1_datetime = start_time + timedelta(minutes=5)  # 略過前 5 分鐘
        end_time = start_time + timedelta(minutes=use_time)

        # 過濾ripple_result中的資料，符合這次投餌的時間範圍
        ripple_data_filtered = [(t, ra) for t, ra in ripple_result if t1_datetime <= t <= end_time]
        if len(ripple_data_filtered) <= 20:
            print(f'Skip {idx} data {start_time.strftime("%Y-%m-%d %H:%M:%S")} to {end_time.strftime("%Y-%m-%d %H:%M:%S")}')
            first_thd_idx_4_test.append(None)
            continue

        feed_once_dt_data, feed_once_data = zip(*ripple_data_filtered)
        feed_once_data = np.asarray(feed_once_data)
        smoothed_data = medfilt(feed_once_data, odd_windows_size)

        first_flag = False
        for i in range(math.ceil(use_time)):
            wend = end_time - timedelta(minutes=i)
            wstart = wend - timedelta(minutes=windows_minutes)
            filter = np.logical_and(np.asarray(feed_once_dt_data) >= wstart, np.asarray(feed_once_dt_data) <= wend)
            w_data = smoothed_data[filter]
            w_datetime = np.asarray(feed_once_dt_data)[filter]

            if len(w_data) <= 2:
                break

            threshold_indexs = [len(w_data) // 2]
            if i < 5:
                under_bound = w_datetime > wend - timedelta(minutes=t3)
                if np.any(under_bound):
                    valid_indices = np.where(under_bound == True)[0]
                    if len(valid_indices) > 0:
                        threshold_indexs = list(range(threshold_indexs[0], valid_indices[0]))
                        threshold_indexs.sort(reverse=True)
                    else:
                        continue
                else:
                    continue

            for thd_idx in threshold_indexs:
                threshold_value = w_data[thd_idx]
                global_th_idx = np.where(smoothed_data == threshold_value)[0][0]
                wdata_before = w_data[:thd_idx]
                wdata_after = w_data[thd_idx:]
                t_stat, p_value = stats.ttest_ind(wdata_before, wdata_after, alternative='greater')

                if p_value < alpha and first_flag == False:
                    first_thd_idx_4_test.append(w_datetime[thd_idx])
                    first_flag = True

        if not first_flag:
            first_thd_idx_4_test.append(None)
    
    # print(f"first_thd_idx_4_test: {first_thd_idx_4_test}")
    return first_thd_idx_4_test

def plot_trendchart(period, ripple_result, feeding_result, query_date, selected_date, duration, min_date, max_date):
    morning_segments = defaultdict(list)
    for t, ripple_area in ripple_result:
        morning_segments[t.date()].append(ripple_area)
    
    while min_date <= max_date:
        if min_date not in morning_segments:
            morning_segments[min_date] = None 
        min_date += timedelta(days=1) 

    morning_segments = [
        (idx, date, None if ripple_areas is None else sum(ripple_areas) / len(ripple_areas))
        for idx, (date, ripple_areas) in enumerate(sorted(morning_segments.items()))
    ]
    
    filtered_segments = [(idx, date, ripple_area) for idx, date, ripple_area in morning_segments if ripple_area is not None]
    idxs = np.array([segment[0] for segment in filtered_segments])
    dates = [segment[1] for segment in filtered_segments]
    ripple_areas = np.array([segment[2] for segment in filtered_segments])

    # least square method, f(t) = at + b
    n = len(idxs)
    t = np.sum(idxs)
    t2 = np.sum(idxs**2)
    mt = np.sum(ripple_areas)
    t_mt = np.sum(idxs*ripple_areas)

    if (n*t2-t**2) != 0:
        a = (n*t_mt-t*mt)/(n*t2-t**2)
        b = (mt - a*t)/n
    else:        
        a = float('nan')
        b = float('nan')

    predict_trends=a*idxs+b

    # 找水花明顯下降的時間點
    first_thd_idx_4_test = counting_first_thd_idx_4_test(feeding_result, ripple_result)
    feed_count = []
    decline_dates = []
    minutes = []

    for i, (feed_st_time, feed_used_min) in enumerate(feeding_result):
        if first_thd_idx_4_test[i] is None:
            continue
        # remaining_time = feed_st_time + timedelta(minutes=feed_used_min) - first_thd_idx_4_test[i]
        feeded_time = first_thd_idx_4_test[i] - feed_st_time
        # print(f'[{i}] {feed_st_time.strftime("%Y-%m-%d %H:%M:%S")}: ({feeded_time.total_seconds()/60}) minutes')
        feed_count.append(i+1)
        decline_dates.append(feed_st_time.date())
        minutes.append(feeded_time.total_seconds()/60)
    
    if decline_dates:
        # Generate x and y (using total seconds)
        x_dates_num = mdates.date2num(decline_dates)

        # 將日期數值平移，讓最早的日期對應 feed_count 的第1次投餵
        x = np.array(x_dates_num - x_dates_num[0]) 
        # x = np.array(feed_count)
        y = np.array(minutes)
        
        # least square method, f(t) = at + b
        n = len(x)
        t = np.sum(x)
        t2 = np.sum(x**2)
        mt = np.sum(y)
        t_mt = np.sum(x*y)

        if (n*t2-t**2) != 0:
            decline_a = (n*t_mt-t*mt)/(n*t2-t**2)
            decline_b = (mt - decline_a*t)/n
        else:        
            decline_a = float('nan')
            decline_b = float('nan')

        decline_trends=decline_a*x+decline_b
    else:
        print("decline_dates is empty")

    from matplotlib import font_manager
    font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    font_prop = font_manager.FontProperties(fname=font_path)

    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False  # 避免負號顯示為方框

    fig, ax1 = plt.subplots(figsize=(math.ceil(duration * 2) if duration >= 60 else (130 if duration >= 30 else 15), 26 if duration >= 60 else (40 if duration >= 30 else 10)), dpi=50)

    locator = mdates.DayLocator() 
    formatter = mdates.DateFormatter('%-m/%-d') 
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(formatter)

    # 第一個 Y 軸：水花面積
    ax1.tick_params(axis='x', labelsize=42 if duration >= 60 else (100 if duration >= 30 else 18)) 
    ax1.tick_params(axis='y', labelcolor='tab:blue', labelsize=48 if duration >= 60 else (100 if duration >= 30 else 18)) 
    ax1.plot(dates, ripple_areas, 'o', color='tab:blue', label="平均水花面積值", markersize=40 if duration >= 60 else 15)
    ax1.plot(dates, predict_trends, '-', color='tab:blue', linewidth=20 if duration >= 60 else (10 if duration >= 30 else 4), label=f"水花面積趨勢: y={a:.0f}t+{b:.0f}")

    original_morning_dates = [r[0].date() for r in ripple_result]
    original_morning_ripple_areas = [r[1] for r in ripple_result]
    ax1.scatter(original_morning_dates, original_morning_ripple_areas, color='black', s=30, label='原始水花面積資料點')

    if a/b > 0.01:
        plt.figtext(0.5, 0.92, f'食慾成長程度={a/b:.3f}>1%, 食慾增加', color='red', fontsize=64 if duration >= 60 else (100 if duration >= 30 else 18), fontweight='bold',  ha="center", fontproperties=font_prop)
    elif a/b < -0.01:
        plt.figtext(0.5, 0.92, f'食慾成長程度={a/b:.3f}<1%, 食慾下降', color='red', fontsize=64 if duration >= 60 else (100 if duration >= 30 else 18), fontweight='bold',  ha="center", fontproperties=font_prop)
    else:
        plt.figtext(0.5, 0.92, f'食慾成長程度={a/b:.3f}≈1%, 食慾持平', color='red', fontsize=64 if duration >= 60 else (100 if duration >= 30 else 18), fontweight='bold',  ha="center", fontproperties=font_prop)
        
    ax2 = ax1.twinx()
    ax2.tick_params(axis='y', labelcolor='tab:orange', labelsize=48 if duration >= 60 else (90 if duration >= 30 else 18)) 
    if len(decline_dates) > 0:
        ax2.plot(decline_dates, minutes, 'o', color='tab:orange', label="明顯餵食水花時間長度(分鐘)", markersize=40 if duration >= 60 else 15)
        ax2.plot(decline_dates, decline_trends, '-', color='tab:orange', linewidth=20 if duration >= 60 else (10 if duration >= 30 else 4), label=f"明顯水花時長趨勢: y={decline_a:.2f}t+{decline_b:.2f}")

    ax1.set_xlabel('日期', fontsize = 72 if duration >= 60 else (100 if duration >= 30 else 32), fontweight='bold')
    ax1.set_ylabel('水花面積', fontsize = 72 if duration >= 60 else (90 if duration >= 30 else 32), fontweight='bold', color='tab:blue')
    ax2.set_ylabel('明顯餵食水花時間長度(分鐘)', fontsize = 72 if duration >= 60 else (100 if duration >= 30 else 32), fontweight='bold', color='tab:orange')
    plt.xlim(query_date, selected_date)
    plt.title(f'{period} 水花面積趨勢圖', fontsize = 90 if duration >= 60 else (120 if duration >= 30 else 24), fontweight='bold')
    plt.subplots_adjust(top=0.9)

    ax1.legend(loc='upper left', fontsize = 48 if duration >= 60 else (100 if duration >= 30 else 18))
    ax2.legend(loc='upper right', fontsize = 48 if duration >= 60 else (100 if duration >= 30 else 18))

    plt.grid(True)
    plt.tight_layout()

    save_path = f"trendchart_{period}_{query_date.strftime('%Y%m%d')}_{selected_date.strftime('%Y%m%d')}.png"
    plt.savefig(save_path, format='png')
    print(f"Trend chart saved to {save_path}")
    plt.close(fig)

    return save_path

def generate_trendchart(ripple_result, feeding_result, query_date, selected_date, duration):
    ripple_morning_result = []
    ripple_afternoon_result = []
    feeding_morning_result = []
    feeding_afternoon_result = []
    min_date = ripple_result[0][0].date()
    max_date = ripple_result[-1][0].date()
    
    for r in ripple_result: 
        timestamp, ripple_area = r
        result_date = timestamp.date()
        if 0 < timestamp.hour < 12:
            ripple_morning_result.append((timestamp, ripple_area))
        else:
            ripple_afternoon_result.append((timestamp, ripple_area))

    for r in feeding_result: 
        st, use_time = r
        if 0 < st.hour < 12:
            feeding_morning_result.append((st, use_time))
        else:
            feeding_afternoon_result.append((st, use_time))

    morning_trendchart = plot_trendchart('上午 0:00-11:59', ripple_morning_result, feeding_morning_result, query_date, selected_date, duration, min_date, max_date)
    afternoon_trendchart = plot_trendchart('下午 12:00-23:59', ripple_afternoon_result, feeding_afternoon_result, query_date, selected_date, duration, min_date, max_date)

    return morning_trendchart, afternoon_trendchart


if __name__ == "__main__":
    cursor = connection.cursor()

    databaseName = input("請輸入 databaseName: ") 
    start_date = input("請輸入開始日期 (格式: YYYYMMDD): ")
    start_date = datetime.datetime.strptime(start_date, "%Y%m%d") 
    end_date = input("請輸入結束日期 (格式: YYYYMMDD): ")
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d") 
    next_day = end_date + timedelta(days=1)

    base64_img = ''
    morning_trendchart = '' 
    afternoon_trendchart = '' 
    duration = (next_day - start_date).days
    print(duration)

    sql = f"select update_time, ripple_area from {databaseName}.ripple_history where update_time between %s and %s order by update_time asc"
    cursor.execute(sql, (start_date, next_day))
    ripple_result = list(cursor.fetchall())

    sql = f"SELECT start_time, use_time FROM {databaseName}.original_feeding_logs WHERE use_time > %s and start_time between %s and %s order by start_time asc"
    cursor.execute(sql, (10, start_date, next_day))
    feeding_result = list(cursor.fetchall())
    
    print(f"Ripple result:  {ripple_result[:1]} ~ {ripple_result[-1:]}")
    print(f"Feeding result: {feeding_result[:1]} ~ {feeding_result[-1:]}")

    print("generate_heatmap")
    base64_img = generate_heatmap(ripple_result, start_date, duration)
    print("generate_trendchart")
    morning_trendchart, afternoon_trendchart = generate_trendchart(ripple_result, feeding_result, start_date, end_date, duration)

    cursor.close()
    connection.close()