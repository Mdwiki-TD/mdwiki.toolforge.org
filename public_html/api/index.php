<?php

if (isset($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}
if (!isset($_GET['get'])) {
    header('Location: /api/test/index.php');
    // include_once __DIR__ . '/test/index.php';
    exit();
}

include_once __DIR__ . '/api_cod/request.php';
