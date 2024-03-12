// all pages
var sessionTimeout = 5 * 60 * 1000;  // 5 minutes in milliseconds

function resetSessionTimer() {
    clearTimeout(sessionTimeoutID);
    sessionTimeoutID = setTimeout(logout, sessionTimeout);
}

function logout() {
    window.location.href = '/logout';  // Redirect to the logout route
    alert('系統閒置時間過久，已為您自動登出!')
}

var sessionTimeoutID = setTimeout(logout, sessionTimeout);

// Listen for user activity events to reset the session timer
window.addEventListener('mousemove', resetSessionTimer);
window.addEventListener('keydown', resetSessionTimer);

if (window.location.pathname.includes('choose_ripple_frame.html')) {
    window.removeEventListener('mousemove', resetSessionTimer);
    window.removeEventListener('keydown', resetSessionTimer);
}

//
// home.html
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

// sidebar control
// 點擊按鈕收縮或展開 sidebar
$(document).ready(function() {
    $("#sidebar-btn").click(function() {
        $("#sidebar-item").toggleClass("collapsed"); 
        $("#sidebar").toggleClass("collapsed");
    });
});

// 獲取按鈕和要控制的 div 元素
var toggleButton = document.getElementById("sidebar-btn");
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

// port 3030
// field_logs.html 
pool_data = []
$(document).ready(function(){
$('#pool_ID').change(
function(){
    var selected = document.getElementById("pool_ID").value;
    var newPoolData = document.getElementById("pool_tbody");
    // console.log("pool_ID =" + selected);
    var data = {
    "pool_ID": selected,
    "pool_data": pool_data
    }
    // console.log("data = " + JSON.stringify(data));
    $.ajax({
    url : 'http://34.81.183.159:3030/field_logs',
    type : 'POST', 
    data : JSON.stringify(data),
    contentType : 'application/json; charset=utf-8', // 要送到server的資料型態
    dataType : 'json', // 預期從server接收的資料型態
    success : function(data) {
        // console.log("傳送成功" + JSON.stringify(data));
        var colCount = $("#pool_tbody tr").length;
        for (var i = 0; i < colCount; i++){
            newPoolData.deleteRow(0);
        }
        newPoolData.insertRow(0);
        var dataArray = Object.values(data);
        var pool_data = dataArray[1];
        var r = pool_data.length;
        var c = pool_data[0].length;
        for (var i = 0; i < r; i++){
        var newRow = newPoolData.insertRow(i+1);
        for (var j = 0; j < c; j++){
            var newCell = newPoolData.rows[i+1].insertCell(j);
            newCell.innerHTML = pool_data[i][j];
        }
        }
    },
    error: function (xhr, type){
        console.log("傳送失敗" + xhr + type);
    }
    });
})
})

// port 8080
// field_logs.html
pool_data = []
$(document).ready(function(){
$('#pool_ID').change(
function(){
    var selected = document.getElementById("pool_ID").value;
    var newPoolData = document.getElementById("pool_tbody");
    // console.log("pool_ID =" + selected);
    var data = {
    "pool_ID": selected,
    "pool_data": pool_data
    }
    // console.log("data = " + JSON.stringify(data));
    $.ajax({
    url : 'http://34.81.183.159:8080/field_logs',
    type : 'POST', 
    data : JSON.stringify(data),
    contentType : 'application/json; charset=utf-8', // 要送到server的資料型態
    dataType : 'json', // 預期從server接收的資料型態
    success : function(data) {
        // console.log("傳送成功" + JSON.stringify(data));
        var colCount = $("#pool_tbody tr").length;
        for (var i = 0; i < colCount; i++){
            newPoolData.deleteRow(0);
        }
        newPoolData.insertRow(0);
        var dataArray = Object.values(data);
        var pool_data = dataArray[1];
        var r = pool_data.length;
        var c = pool_data[0].length;
        for (var i = 0; i < r; i++){
        var newRow = newPoolData.insertRow(i+1);
        for (var j = 0; j < c; j++){
            var newCell = newPoolData.rows[i+1].insertCell(j);
            newCell.innerHTML = pool_data[i][j];
        }
        }
    },
    error: function (xhr, type){
        console.log("傳送失敗" + xhr + type);
    }
    });
})
})

// jsgrid table
var dataset = [
    { 
    "魚池編號": "1",
    "規格<br>(尾/公斤)": 100.0,
    "紀錄魚群總重<br>(公斤)": 300.0, 
    "預估魚群總重<br>(公斤)": 300.0, 
    "換肉率": 0.0, 
    "死亡數量": 0, 
    "更新時間": "2023-03-01 12:30:00" 
    },
    { 
    "魚池編號": "1",
    "規格<br>(尾/公斤)": 50.0,
    "紀錄魚群總重<br>(公斤)": 600.0, 
    "預估魚群總重<br>(公斤)": 600.0, 
    "換肉率": 2.0,
    "死亡數量": 100,
    "更新時間": "2023-04-01 12:30:00" 
    },
    { 
    "魚池編號": "2",
    "規格<br>(尾/公斤)": 120.0,
    "紀錄魚群總重<br>(公斤)": 300.0, 
    "預估魚群總重<br>(公斤)": 300.0, 
    "換肉率": 0.0, 
    "死亡數量": 0, 
    "更新時間": "2023-03-01 12:30:00" 
    },
    { 
    "魚池編號": "2",
    "規格<br>(尾/公斤)": 100.0,
    "紀錄魚群總重<br>(公斤)": 400.0, 
    "預估魚群總重<br>(公斤)": 400.0, 
    "換肉率": 1.5, 
    "死亡數量": 100, 
    "更新時間": "2023-03-10 12:30:00" 
    },
    { 
    "場域編魚池編號號": "2",
    "規格<br>(尾/公斤)": 100.0,
    "紀錄魚群總重<br>(公斤)": 600.0, 
    "預估魚群總重<br>(公斤)": 600.0, 
    "換肉率": 1.1, 
    "死亡數量": 100, 
    "更新時間": "2023-04-01 12:30:00" 
    }
];

var feeding_logs_dataset = [
    { "魚池編號": "1",
    "投餌機編號": "1",
    "投餌時間": "2023-04-01 13:00:00", 
    "耗時(分鐘)": 30.0, 
    "投餌料號": "test", 
    "投餌量(公克)": 100000 
    },
    { "魚池編號": "1",
    "投餌機編號": "2",
    "投餌時間": "2023-04-02 13:00:00", 
    "耗時(分鐘)": 30.0, 
    "投餌料號": "test", 
    "投餌量(公克)": 100000 
    },
    { "魚池編號": "1",
    "投餌機編號": "1",
    "投餌時間": "2023-04-03 13:00:00", 
    "耗時(分鐘)": 30.0, 
    "投餌料號": "test", 
    "投餌量(公克)": 100000 
    },
    { "魚池編號": "1",
    "投餌機編號": "1",
    "投餌時間": "2023-04-04 13:00:00", 
    "耗時(分鐘)": 30.0, 
    "投餌料號": "test", 
    "投餌量(公克)": 100000 
    },
    { "魚池編號": "1",
    "投餌機編號": "1",
    "投餌時間": "2023-04-05 13:00:00", 
    "耗時(分鐘)": 30.0, 
    "投餌料號": "test", 
    "投餌量(公克)": 100000 
    },
    { "魚池編號": "1",
    "投餌機編號": "2",
    "投餌時間": "2023-04-06 13:00:00", 
    "耗時(分鐘)": 30.0, 
    "投餌料號": "test", 
    "投餌量(公克)": 100000 
    }
];

// field logs jsgrid
$("#field_logs").jsGrid({
    width: "100%",
    height: "400px",

    inserting: true,
    editing: true,
    sorting: true,
    paging: true,
    autoload: true,
    controller: {
        loadData: function() {
            var d = $.Deferred();
            $.ajax({
                url: "/api/database",
                dataType: "json",
                type: "GET"
            }).done(function(response) {
                d.resolve(response);
            });

            return d.promise();
        },
        updateItem: function(item) {
            var d = $.Deferred();
            // console.log("updateItem:", item);
            $.ajax({
                url: "/api/database",
                data: JSON.stringify(item),
                type: "PUT",
                dataType: "json",
                contentType: "application/json",
            }).done(function(response) {
                d.resolve(response);
            });
            return d.promise();
        },
        deleteItem: function(item) {
            var d = $.Deferred();
            $.ajax({
                url: "/api/database",
                data: item,
                type: "DELETE",
            }).done(function(response) {
                d.resolve(response);
            });
            return d.promise();
        },
        insertItem: function(item) {
            var d = $.Deferred();
            $.ajax({
                url: "/api/database",
                data: JSON.stringify(item),
                dataType: "json",
                contentType: "application/json",
                type: "POST",
            }).done(function(response) {
                d.resolve(response);
            });
            return d.promise();
        },


    },

    fields: [
        { 
            name: "場域編號", 
            type: "text", 
            width: 40, 
            validate: "required" 
        },
        { 
            name: "規格<br>(尾/公斤)",
            type: "number",
            width: 40 
        },
        { name: "紀錄魚群總重<br>(公斤)",
            type: "number",
            width: 40 
        },
        { 
            name: "預估魚群總重<br>(公斤)", 
            type: "number", 
            width: 40 
        },
        { 
            name: "換肉率", 
            type: "number", 
            width: 30, 
            itemTemplate: function(value) {
            return value.toFixed(2);
        },
        },
        { 
            name: "死亡數量", 
            type: "number", 
            width: 30 
        },
        { 
            name: "更新時間", 
            type: "text", 
            width: 60,
            sorting: true
        },
        { 
            type: "control", 
            width: 20 
        }
    ]
});

// feeding logs jsgrid
$("#feeding_logs").jsGrid({
width: "100%",
height: "400px",

inserting: true,
editing: true,
sorting: false,
paging: false,
autoload: true,
controller: {
    loadData: function() {
        var d = $.Deferred();
        $.ajax({
            url: "/api/feedingdatabase",
            dataType: "json",
            type: "GET"
        }).done(function(response) {
            d.resolve(response);
        });

        return d.promise();
    },
    updateItem: function(item) {
        var d = $.Deferred();
        // console.log("updateItem:", item);
        $.ajax({
            url: "/api/feedingdatabase",
            data: JSON.stringify(item),
            type: "PUT",
            dataType: "json",
            contentType: "application/json",
        }).done(function(response) {
            d.resolve(response);
        });
        return d.promise();
    },
    deleteItem: function(item) {
        var d = $.Deferred();
        $.ajax({
            url: "/api/feedingdatabase",
            data: item,
            type: "DELETE",
        }).done(function(response) {
            d.resolve(response);
        });
        return d.promise();
    },
    insertItem: function(item) {
        var d = $.Deferred();
        $.ajax({
            url: "/api/feedingdatabase",
            data: JSON.stringify(item),
            dataType: "json",
            contentType: "application/json",
            type: "POST",
        }).done(function(response) {
            d.resolve(response);
        });
        return d.promise();
    },


    },
    fields: [
        { 
        name: "場域編號", 
        type: "text", 
        width: 40, 
        validate: "required" 
        },
        { 
        name: "投餌機編號",
        type: "text", 
        width: 40 
        },
        { 
        name: "投餌時間", 
        type: "text", 
        width: 60,
        sorting: true
        },
        { name: "耗時(分鐘)",
        type: "number",
        width: 30 
        },
        { 
        name: "投餌料號", 
        type: "text", 
        width: 40 
        },
        { 
        name: "投餌量(公克)", 
        type: "number", 
        width: 30 
        },
        { 
        type: "control", 
        width: 20 
        }
    ]


});

