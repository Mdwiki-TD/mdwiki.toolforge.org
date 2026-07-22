<?php

namespace FixWikiRefs\SavePage;

use function RefsOAuth\MdwikiSql\fetch_query;
use function RefsOAuth\SendEdit\auth_make_edit;
use function FixWikiRefs\Form\make_result_form;

use Defuse\Crypto\Crypto;
use Defuse\Crypto\Key;

function decode_value($value, $key_type = "cookie")
{
    if (empty(trim($value))) return "";

    $cookieKeyString = getenv('COOKIE_KEY') ?: $_ENV['COOKIE_KEY'] ?? '';
    $decryptKeyString = getenv('DECRYPT_KEY') ?: $_ENV['DECRYPT_KEY'] ?? '';

    $use_key_String  = ($key_type === "decrypt") ? $decryptKeyString : $cookieKeyString;
    $use_key = $use_key_String ? Key::loadFromAsciiSafeString($use_key_String) : null;

    if ($use_key === null) return "";

    try {
        return Crypto::decrypt($value, $use_key);
    } catch (\Exception $e) {
        return "";
    }
}

function get_access_from_db($user)
{
    $user = trim($user);

    $query = <<<SQL
        SELECT access_key, access_secret
        FROM access_keys
        WHERE user_name = ?;
    SQL;

    $result = fetch_query($query, [$user]);


    if (!$result) {
        return null;
    }

    $result = $result[0];
    // ---
    return [
        'access_key' => decode_value($result['access_key'], "decrypt"),
        'access_secret' => decode_value($result['access_secret'], "decrypt")
    ];
}
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
    $access = get_access_from_db($user_name);
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

function published_alert($text, $type)
{
    $alert_classes = ['success', 'info', 'warning', 'danger'];
    $class = in_array($type, $alert_classes) ? $type : 'info';
    return <<<HTML
        <div class="container-fluid">
            <div class="row justify-content-center">
                <div class="col-md-9 col-12">
                    <div class="alert alert-$type d-flex align-items-center" role="alert">
                        $text
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
        $newrevid = $save2['edit']['newrevid'] ?? '0';
        // ---
        $result .= published_success_alert($lang, $newrevid, $title);
    } else {
        // ---
        $aleart = published_alert("Changes are not published, try to do it manually. Error: $error_code ($error_info)", "danger");
        // ---
        $result .= $aleart;
        $result .= make_result_form($new, $newtext);
    }
    // ---
    return $result;
}
