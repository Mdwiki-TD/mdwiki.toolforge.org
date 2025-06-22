<?php

namespace Prior;

include_once __DIR__ . '/header.php';
include_once 'graph.php';
include_once 'prior_leaders.php';
include_once 'top/lead_help.php';
include_once 'top/index.php';
include_once 'top/langs.php';

use function TopIndex\generateLeaderboardTable;
use function TopLangs\make_lang_tab;

// Enable error reporting for debugging (Only if 'test' request parameter is set)
if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

$langs = $_REQUEST['lang'] ?? '';

echo <<<HTML
    <div class="container">
        <div class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle"></i> This is a draft that requires further verification.
        </div>
    </div>
HTML;

// Display the appropriate top page based on 'lang' request parameter

if ($langs !== '') {
    make_lang_tab();
} else {
    generateLeaderboardTable();
}

echo '<script>$("#prior").addClass("active");</script>';

include_once 'foter.php';
