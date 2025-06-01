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
use function FixWikiRefs\Form\make_result_form;

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
        error_log("Failed to get access from any database for user: $user_name");
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
    return $result;
}

function make_save_result($title, $lang, $newtext, $new)
{
    // ---
    $result = "";
    // ---
    $save2 = saveit($title, $lang, $newtext);
    // ---
    $error_code = ($save2['error']['code'] ?? '') ?? '';
    $error_info = ($save2['error']['info'] ?? '') ?? '';
    // ---
    $Success = isset($save2['edit']['result']) && $save2['edit']['result'] == 'Success';
    // ---
    if ($Success) {
        $result .= '<div class="alert alert-success" role="alert">Changes has published.</div>';
    } else {
        // var_export(json_encode($save2['error'], JSON_PRETTY_PRINT));
        // ---
        $aleart = <<<HTML
            <div class="alert alert-danger" role="alert">
                Changes are not published, try to do it manually. Error: $error_code ($error_info)
            </div>
        HTML;
        // ---
        $result .= $aleart;
        $result .= make_result_form($new, $newtext);
    }
    // ---
    return $result;
}
