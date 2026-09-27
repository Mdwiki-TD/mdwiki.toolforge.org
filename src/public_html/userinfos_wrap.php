<?php


if (substr(__DIR__, 0, 2) == 'I:') {
    include_once 'I:/MD_TOOLS/mdwiki.toolforge.org/PHP_REPOS/auth_repo/src/oauth/user_infos.php';
} else {
    ini_set('session.use_strict_mode', '1');
    include_once __DIR__ . '/auth/oauth/user_infos.php';
}
