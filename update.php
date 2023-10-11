<?php
$db_config = [
    'host' => '34.81.183.159',
    'user' => 'lab403',
    'password' => '66386638',
    'database' => 'fishDB'
];

// 獲取指令
$mode = $_POST['mode'];
$angle = $_POST['angle'];
$period = $_POST['period'];
$amount = $_POST['amount'];
$fetch_interval = $_POST['fetch_interval'];

// 建立連線
$mysqli = new mysqli($db_config['host'], $db_config['user'], $db_config['password'], $db_config['database']);

if ($mysqli->connect_error) {
    die('Connection Failed：' . $mysqli->connect_error);
}

// update
$query = "UPDATE decision SET mode='$mode', angle='$angle', period='$period', amount='$amount', fetch_interval='$fetch_interval' WHERE id='1'";

if ($mysqli->query($query) === TRUE) {
    echo "Data update SUCCESSFULLY。";
} else {
    echo "Data update UNSECCESSFULLY： " . $mysqli->error;
}
echo "<p><a href='http://34.81.183.159/fishDB/decision.html'>返回原本的網頁</a></p>";
$mysqli->close();
?>
