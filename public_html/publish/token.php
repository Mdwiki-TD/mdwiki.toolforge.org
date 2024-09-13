<?php

header('Content-Type: application/json; charset=utf-8');
header("Access-Control-Allow-Origin: *");

include_once __DIR__ . '/../Translation_Dashboard/vendor_load.php';

include_once __DIR__ . '/config.php';
include_once __DIR__ . '/helps.php';
include_once __DIR__ . '/get_token.php';

use function Publish\GetToken\get_cxtoken;
use function Publish\Helps\get_access_from_db;
use function Publish\Helps\del_access_from_db;

$wiki    = $_GET['wiki'] ?? '';
$user    = $_GET['user'] ?? '';
$ty      = $_GET['ty'] ?? '';

if (empty($wiki) || empty($user)) {
    print(json_encode(['error' => ['code' => 'no data', 'info' => 'wiki or user is empty']], JSON_PRETTY_PRINT));
    exit(1);
}

$access = get_access_from_db($user);

if ($access == null) {
    $cxtoken = ['error' => ['code' => 'no access', 'info' => 'no access'], 'username' => $user];
    // exit(1);
} else {
    $access_key = $access['access_key'];
    $access_secret = $access['access_secret'];

    $cxtoken = get_cxtoken($wiki, $access_key, $access_secret) ?? ['error' => 'no cxtoken'];
}

$err = $cxtoken['csrftoken_data']["error"]["code"] ?? null;
if ($err == "mwoauth-invalid-authorization-invalid-user") {
    del_access_from_db($user);
    $cxtoken["del_access"] = true;
}

print(json_encode($cxtoken, JSON_PRETTY_PRINT));
