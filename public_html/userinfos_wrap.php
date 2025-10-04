<?php

ini_set('session.use_strict_mode', '1');
//---
if (substr(__DIR__, 0, 2) == 'I:') {
    include_once 'I:/mdwiki/auth_repo/oauth/user_infos.php';
} else {
    include_once __DIR__ . '/auth/oauth/user_infos.php';
}

if (!empty($GLOBALS['global_username'] ?? "")) {
    $global_username = $GLOBALS['global_username'];
} else {
    $GLOBALS['global_username'] = '';
}
