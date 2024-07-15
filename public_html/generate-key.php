<?php

require_once('Translation_Dashboard/vendor/autoload.php');

use Defuse\Crypto\Key;

if (file_exists('mdwiki-secret-key.txt')) {
    die('Key already exists, will not overwrite.');
}
$key = Key::createNewRandomKey();
file_put_contents('mdwiki-secret-key.txt', $key->saveToAsciiSafeString());
chmod('mdwiki-secret-key.txt', 0600);
