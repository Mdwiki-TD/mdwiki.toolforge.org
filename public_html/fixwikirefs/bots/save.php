<?php

namespace FixWikiRefs\SavePage;

if (isset($_GET['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}
/*
usage:

use function FixWikiRefs\SavePage\saveit;

*/

use function OAuth\SendEdit\auth_make_edit;
use function OAuth\AccessHelps\get_access_from_dbs;
use function OAuth\AccessHelpsNew\get_access_from_dbs_new;

function saveit($title, $lang, $text)
{
    $user_name = (isset($GLOBALS['global_username']) && $GLOBALS['global_username'] != '') ? $GLOBALS['global_username'] : '';
    // ---
    if ($user_name == '') {
        return false;
    }
    // ---
    $summary = "Fix references, Expand infobox #mdwiki .toolforge.org.";
    // ---
    $access = get_access_from_dbs_new($user_name);
    // ---
    if ($access == null) {
        $access = get_access_from_dbs($user_name);
    }
    // ---
    if ($access == null) {
        return false;
    };
    // ---
    $access_key = $access['access_key'];
    $access_secret = $access['access_secret'];
    // ---
    $result = auth_make_edit($title, $text, $summary, $lang, $access_key, $access_secret);
    // ---
    $Success = ($result['edit']['result'] ?? '') == 'Success';
    // ---
    return $Success;
}
