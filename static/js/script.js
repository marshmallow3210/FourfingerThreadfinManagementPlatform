// 顯示當前日期與時間
function displayDateTime() {
    const now = new Date(); // 獲取當前日期和時間
    const date = now.toLocaleDateString();
    const time = now.toLocaleTimeString();

    // 更新 HTML 元素的內容
    document.getElementById('current_date').textContent = date;
    document.getElementById('current_time').textContent = time;
}

// 每秒更新一次時間
setInterval(displayDateTime, 1000);


// 點擊按鈕收縮或展開sidebar
$(document).ready(function() {
    $("#sidebar_button").click(function() {
        $("#sidebar-item").toggleClass("show-element"); // 切換 .show-element 類別
        $("#sidebar").toggleClass("collapsed");
    });
});

// 獲取按鈕和要控制的 div 元素
var toggleButton = document.getElementById("sidebar_button");
var sidebarDiv = document.getElementById("sidebar");

// 添加點擊事件監聽器
toggleButton.addEventListener("click", function() {
    // 切換 div 的顯示狀態
    if (sidebarDiv.classList.contains("hidden")) {
        // 如果 div 是隱藏的，則顯示它
        sidebarDiv.classList.remove("hidden");
    } else {
        // 如果 div 是顯示的，則隱藏它
        sidebarDiv.classList.add("hidden");
    }
});
