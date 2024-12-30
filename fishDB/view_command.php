<?php
require_once("config.php");

// 查詢當前指令
$sql = "SELECT * FROM decision";
$result = $mysqli->query($sql);

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {

        echo "<p>8888模式: " . $row["mode"] . "</p>";
        echo "<p>投餌角度: " . $row["angle"] . "</p>";
        echo "<p>投餌時長: " . $row["period"] . "</p>";
        echo "<p>投料量: " . $row["amount"] . "</p>";
        echo "<p>指令更新頻率: " . $row["fetch_interval"] . "</p>";
    }
} else {
    echo "沒有找到指令";
}

echo "<p><a href='http://.../arDB/simple_control/main.html'>返回原本的網頁</a></p>";
$mysqli->close();
?>
