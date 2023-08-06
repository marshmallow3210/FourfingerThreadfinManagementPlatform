function displayDateTime() {
    const now = new Date(); // 獲取當前日期和時間
    const date = now.toLocaleDateString(); // 獲取日期部分
    const time = now.toLocaleTimeString(); // 獲取時間部分

    // 更新 HTML 元素的內容
    document.getElementById('current_date').textContent = date;
    document.getElementById('current_time').textContent = time;
}

// 每秒更新一次時間
setInterval(displayDateTime, 1000);