<?php
if (isset($_GET['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};

include_once __DIR__ . '/../Translation_Dashboard/actions/functions.php';
include_once __DIR__ . '/../Translation_Dashboard/actions/mdwiki_api.php';
include_once __DIR__ . '/../Translation_Dashboard/Tables/tables.php';
include_once __DIR__ . '/../Translation_Dashboard/Tables/langcode.php';
include_once __DIR__ . '/../Translation_Dashboard/translate/en_api.php';
//---
include_once __DIR__ . '/get_missing.php';
//---
// header json
header('Content-type: application/json');
//---
use function MI\GetMissing\get_miss;

$code = $_GET['code'] ?? '';
$cat = $_GET['cat'] ?? '';

$result = get_miss($code, $cat);

echo json_encode($result);
