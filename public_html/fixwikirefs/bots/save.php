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
use function FixWikiRefs\SavePage\make_save_result;
use function FixWikiRefs\SavePage\published_success_alert;
use function FixWikiRefs\SavePage\published_danger_alert;

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

function published_success_alert($lang, $newrevid, $title)
{
    return <<<HTML
        <div class="container-fluid">
            <div class="row justify-content-center">
                <div class="col-md-9 col-12">
                    <div class="alert alert-success d-flex align-items-center" role="alert">
                        <i class="bi bi-check-circle-fill me-2"></i> Changes have been published.
                        <div class="ms-auto d-flex gap-2">
                            <a href="https://$lang.wikipedia.org/w/index.php?title=Special:Diff/$newrevid" target="_blank" class="btn btn-outline-primary btn-sm">
                                <i class="bi bi-file-earmark-text me-1"></i> Diff
                            </a>
                            <a href="https://$lang.wikipedia.org/w/index.php?title=$title&action=history" target="_blank" class="btn btn-outline-primary btn-sm">
                                <i class="bi bi-clock-history me-1"></i> History
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    HTML;
}

function published_danger_alert($error_code, $error_info)
{
    return <<<HTML
        <div class="container-fluid">
            <div class="row justify-content-center">
                <div class="col-md-9 col-12">
                    <div class="alert alert-danger d-flex align-items-center" role="alert">
                        Changes are not published, try to do it manually. Error: $error_code ($error_info)
                    </div>
                </div>
            </div>
        </div>
    HTML;
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
    // if (isset($_GET['test'])) { var_export(json_encode($save2, JSON_PRETTY_PRINT)); }
    // ---
    $Success = isset($save2['edit']['result']) && $save2['edit']['result'] == 'Success';
    // ---
    if ($Success) {
        // '{ "edit": { "result": "Success", "pageid": 7613329, "title": "Anemia na gravidez", "contentmodel": "wikitext", "oldrevid": 70215097, "newrevid": 70257752, "newtimestamp": "2025-06-08T00:30:18Z" } }'
        // ---
        $newrevid = $save2['edit']['newrevid'];
        // ---
        $result .= published_success_alert($lang, $newrevid, $title);
    } else {
        // var_export(json_encode($save2['error'], JSON_PRETTY_PRINT));
        // ---
        $aleart = published_danger_alert($error_code, $error_info);
        // ---
        $result .= $aleart;
        $result .= make_result_form($new, $newtext);
    }
    // ---
    return $result;
}
