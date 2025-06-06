<?php

namespace Prior;

require 'header.php';
require 'graph.php';
require 'prior_leaders.php';
require 'top/lead_help.php';
require 'top/index.php';
require 'top/langs.php';

use function TopIndex\generateLeaderboardTable;
use function TopLangs\make_lang_tab;

// Enable error reporting for debugging (Only if 'test' request parameter is set)
if (isset($_REQUEST['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
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

require 'foter.php';
