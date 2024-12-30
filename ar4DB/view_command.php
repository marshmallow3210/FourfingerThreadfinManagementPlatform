<?php
$db_config = [
    'host' => '34.81.183.159',
    'user' => 'lab403',
    'password' => '66386638',
    'database' => 'ar4DB'
];

// 建立連線
$mysqli = new mysqli($db_config['host'], $db_config['user'], $db_config['password'], $db_config['database']);

if ($conn->connect_error) {
    die("DB連線失敗: " . $conn->connect_error);
}

// 查詢當前指令
$sql = "SELECT * FROM decision";
$result = $mysqli->query($sql);

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {

        echo "<p>模式: " . $row["mode"] . "</p>";
        echo "<p>投餌角度: " . $row["angle"] . "</p>";
        echo "<p>投餌時長: " . $row["period"] . "</p>";
        echo "<p>投料量: " . $row["amount"] . "</p>";
        echo "<p>指令更新頻率: " . $row["fetch_interval"] . "</p>";
    }
} else {
    echo "沒有找到指令";
}

echo "<p><a href='http://34.81.183.159/ar4DB/main.html'>返回原本的網頁</a></p>";
$mysqli->close();
?>
