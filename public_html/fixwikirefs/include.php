<?php

if (isset($_GET['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

if (substr(__DIR__, 0, 2) == 'I:') {
    include_once 'I:/mdwiki/fix_refs_repo/work.php';
} else {
    include_once __DIR__ . '/../fix_refs/work.php';
}

include_once __DIR__ . '/../vendor/autoload.php';
include_once __DIR__ . '/form.php';
include_once __DIR__ . '/utils/database.php';
include_once __DIR__ . '/utils/send_edit.php';
include_once __DIR__ . '/utils/save.php';
include_once __DIR__ . '/utils/get_text.php';
include_once __DIR__ . '/utils/new_fix.php';
