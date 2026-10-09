<?php

if (isset($_GET['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

if (substr(__DIR__, 0, 2) == 'I:') {
    include_once 'I:/MD_TOOLS/mdwiki.toolforge.org/PHP_REPOS/fix_refs_repo/src/work.php';
} else {
    include_once __DIR__ . '/../fix_refs/work.php';
    include_once __DIR__ . '/../vendor/autoload.php';
}

include_once __DIR__ . '/FixRefsController.php';
include_once __DIR__ . '/get_text.php';
