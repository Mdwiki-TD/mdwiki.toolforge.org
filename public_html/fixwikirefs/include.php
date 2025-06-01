<?php
if (isset($_GET['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}
//---
$auth_dir = __DIR__ . '/../auth/auth';
if (!is_dir($auth_dir)) {
    $auth_dir = __DIR__ . '/../../../auth/auth';
}
//---
include_once $auth_dir . '/send_edit.php';
include_once $auth_dir . '/access_helps.php';
include_once $auth_dir . '/access_helps_new.php';
//---
$work_file_path = __DIR__ . '/../fix_refs/work.php';
if (!file_exists($work_file_path)) {
    $work_file_path = __DIR__ . '/../../../fix_refs_repo/work.php';
}
//---
include_once $work_file_path;
//---
include_once __DIR__ . '/form.php';
include_once __DIR__ . '/bots/save.php';
include_once __DIR__ . '/bots/get_text.php';
include_once __DIR__ . '/bots/new_fix.php';
