<?php
if (isset($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};
try {
    header('Content-Type: application/json');
} catch (Exception $e) {
    echo "";
}

include_once __DIR__ . '/include.php';

use function Publish\Helps\pub_test_print;
use function Publish\DoEdit\publish_do_edit;
use function Publish\Helps\get_access_from_db;
use function Publish\AddToDb\InsertPageTarget;
use function Publish\AddToDb\retrieveCampaignCategories;
use function Publish\WD\LinkToWikidata;
use function Publish\TextFix\DoChangesToText;

/*
$t_Params = [
    'title' => $title->getPrefixedDBkey(),
    'text' => $wikitext,
    'user' => $user_name,
    'summary' => $summary,
    'target' => $params['to'],
    'sourcetitle' => $params['sourcetitle'],
];
*/

function get_revid($sourcetitle)
{
    // ---
    // read all_pages_revids.json file
    try {
        $json = json_decode(file_get_contents(__DIR__ . '/all_pages_revids.json'), true);
        $revid = $json[$sourcetitle] ?? "";
        return $revid;
    } catch (Exception $e) {
        pub_test_print($e->getMessage());
    }
    // ---
    return "";
}

function make_summary($revid, $sourcetitle, $to)
{
    return "Created by translating the page [[:mdwiki:Special:Redirect/revision/$revid|$sourcetitle]] to:$to #mdwikicx";
}

function to_do($tab, $dir)
{
    if (!is_dir(__DIR__ . "/$dir")) {
        mkdir(__DIR__ . "/$dir", 0755, true);
    }
    try {
        // dump $tab to file in folder to_do
        $file_name = __DIR__ . "/$dir/" . rand(0, 999999999) . '.json';
        file_put_contents($file_name, json_encode($tab, JSON_PRETTY_PRINT));
    } catch (Exception $e) {
        pub_test_print($e->getMessage());
    }
}

$sourcetitle = $_REQUEST['sourcetitle'] ?? '';
$title    = $_REQUEST['title'] ?? '';
$user     = $_REQUEST['user'] ?? '';
$lang     = $_REQUEST['target'] ?? '';
$text     = $_REQUEST['text'] ?? '';
$campaign = $_REQUEST['campaign'] ?? '';

$summary  = $_REQUEST['summary'] ?? '';
$revid    = $_REQUEST['revid'] ?? '';

$revid    = get_revid($sourcetitle);
$summary  = make_summary($revid, $sourcetitle, $lang);

// $username = get_from_cookie('username');

$access = get_access_from_db($user);

$tab = [
    'title' => $title,
    'summary' => $summary,
    'lang' => $lang,
    'user' => $user,
    'campaign' => $campaign,
    'result' => "",
    'edit' => [],
    'sourcetitle' => $sourcetitle

];
// ---
$to_do_dir = "to_do";
// ---

if ($access == null) {
    $ee = ['code' => 'noaccess', 'info' => 'noaccess'];
    $editit = ['error' => $ee, 'edit' => ['error' => $ee, 'username' => $user], 'username' => $user];
    $to_do_dir = "errors";
} else {
    $access_key = $access['access_key'];
    $access_secret = $access['access_secret'];
    // ---
    // $text = fix_wikirefs($text, $lang);
    $text = DoChangesToText($sourcetitle, $text, $lang, $revid);
    // ---
    $editit = publish_do_edit($title, $text, $summary, $lang, $access_key, $access_secret);
    // ---
    $Success = $editit['edit']['result'] ?? '';
    // ---
    $tab['result'] = $Success;
    // ---
    if ($Success === 'Success') {
        // ---
        $camp_to_cat = retrieveCampaignCategories();
        $cat         = $camp_to_cat[$campaign] ?? '';
        // ---
        try {
            $is_user_page = InsertPageTarget($sourcetitle, 'lead', $cat, $lang, $user, "", $title);
            // ---
            $editit['LinkToWikidata'] = LinkToWikidata($sourcetitle, $lang, $user, $title, $access_key, $access_secret);
        } catch (Exception $e) {
            pub_test_print($e->getMessage());
        }
        // ---
    } else {
        $to_do_dir = "errors";
    }
}
$tab['edit'] = $editit;
to_do($tab, $to_do_dir);

pub_test_print("\n<br>");
pub_test_print("\n<br>");

print(json_encode($editit, JSON_PRETTY_PRINT));

// file_put_contents(__DIR__ . '/editit.json', json_encode($editit, JSON_PRETTY_PRINT));
