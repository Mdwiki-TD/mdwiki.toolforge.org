<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$cache_key = "cxategory_members_";
$cache_ttl = 15;

$now = time();

$items = apcu_fetch($cache_key);

if ($items === false) {
    $items = ['items' => 1000, "in_cache" => time()];
    apcu_store($cache_key, $items, $cache_ttl);
}

$items['now'] = $now;

$data = json_encode($items);

echo json_encode($data);
