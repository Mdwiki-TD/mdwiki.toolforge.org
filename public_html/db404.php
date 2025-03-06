<?php
function echox($s = '') {
    if (isset($_GET['tx'])) {
        echo $s;
    }
}

if ($_SERVER['SERVER_NAME'] === 'localhost') {
    $host = 'localhost:3306';
    $dbname = 'vi';
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
    $db = new PDO("mysql:host=$host;dbname=$dbname", $user, $password);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    echox("Error connecting to database: " . $e->getMessage());
    exit;
}

// إنشاء جدول `errors` لتسجيل المسارات الخاطئة إذا لم يكن موجودًا
$sql = "CREATE TABLE IF NOT EXISTS errors (
    path VARCHAR(512) NOT NULL PRIMARY KEY,
    visits INT NOT NULL DEFAULT 1
)";
try {
    $db->exec($sql);
} catch (PDOException $e) {
    echox("Error creating errors table: " . $e->getMessage());
    exit;
}

$path = $_SERVER['REQUEST_URI'];
// $path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
echox("Path: " . $path . "<br/>");

// التحقق مما إذا كان المسار موجودًا بالفعل
$sql = "SELECT visits FROM errors WHERE path = ?";

try {
    $stmt = $db->prepare($sql);
    $stmt->bindParam(1, $path, PDO::PARAM_STR);
    $stmt->execute();
    $result = $stmt->fetch(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    echox("Error checking for path: " . $e->getMessage());
    exit;
}

if ($result) {
    // تحديث عدد الزيارات إذا كان المسار مسجلاً من قبل
    $visits = (int) $result['visits'] + 1;

    $sql = "UPDATE errors SET visits = ? WHERE path = ?";
    $stmt = $db->prepare($sql);
    $stmt->bindParam(1, $visits, PDO::PARAM_INT);
    $stmt->bindParam(2, $path, PDO::PARAM_STR);

    try {
        $stmt->execute();
    } catch (PDOException $e) {
        echox("Error updating visit count: " . $e->getMessage());
        exit;
    }
} else {
    // إدراج مسار جديد إذا لم يكن مسجلاً من قبل
    $sql = "INSERT INTO errors (path, visits) VALUES (?, 1)";
    $stmt = $db->prepare($sql);
    $stmt->bindParam(1, $path, PDO::PARAM_STR);

    try {
        $stmt->execute();
    } catch (PDOException $e) {
        echox("Error inserting new path: " . $e->getMessage());
        exit;
    }
}

// إغلاق الاتصال بقاعدة البيانات
$db = null;
?>
