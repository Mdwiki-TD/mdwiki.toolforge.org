<?php

function echox($s = '')
{
    if (isset($_GET['tx'])) {
        echo $s;
    }
}

if ($_SERVER['SERVER_NAME'] === 'localhost') {
    $host = 'localhost:3306';
    $dbname = 'mv';
    $user = 'root';
    $password = 'root11';
} else {
    $ts_pw = posix_getpwuid(posix_getuid());
    $ts_mycnf = parse_ini_file($ts_pw['dir'] . "/replica.my.cnf");
    $host = 'tools.db.svc.wikimedia.cloud';
    $dbname = $ts_mycnf['user'] . "__vi";
    $user = $ts_mycnf['user'];
    $password = $ts_mycnf['password'];
    unset($ts_mycnf, $ts_pw);
}

// الاتصال بقاعدة البيانات
try {
    $db = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $user, $password);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    echox("Error connecting to database: " . $e->getMessage());
    exit;
}

// $db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
// $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

// إنشاء جدول `errors` لتسجيل المسارات الخاطئة إذا لم يكن موجودًا
$sql = "CREATE TABLE IF NOT EXISTS errors (
        path VARCHAR(512) NOT NULL PRIMARY KEY,
        visits INT NOT NULL DEFAULT 1,
        UNIQUE KEY `path` (`path`)
)";
try {
    $db->exec($sql);
} catch (PDOException $e) {
    echox("Error creating errors table: " . $e->getMessage());
    exit;
}

$path = $_SERVER['REQUEST_URI'];
// $path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

$path = mb_substr($path, 0, 512);

echox("Path: " . $path . "<br/>");

$sql = "INSERT INTO errors (path, visits)
        VALUES (?, 1)
        ON DUPLICATE KEY UPDATE visits = visits + 1";
try {
    $stmt = $db->prepare($sql);
    $stmt->bindParam(1, $path, PDO::PARAM_STR);
    $stmt->execute();
} catch (PDOException $e) {
    echox('Error upserting visit count: ' . $e->getMessage());
    exit;
}

// إغلاق الاتصال بقاعدة البيانات
$db = null;
