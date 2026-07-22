<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

include_once __DIR__ . '/../auth/vendor_load.php';

use Defuse\Crypto\Key;

$file = __DIR__ . '/mdwiki-secret-key.txt';

echo "$file\n";

if (file_exists($file)) {
    die('Key already exists, will not overwrite.');
}

$key = Key::createNewRandomKey();

file_put_contents($file, $key->saveToAsciiSafeString());

chmod($file, 0600);
