<?php
if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

if (!isset($_GET['get'])) {
    header("Location: api/test.html");
    exit();
}

$path = __DIR__ . '/api/index.php';

if (!file_exists($path)) {
    // I:\mdwiki\TD_API
    $path = __DIR__ . '/../../TD_API/index.php';
}

include_once $path;
