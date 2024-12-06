<?php
if (isset($_GET['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};
//---
include_once __DIR__ . '/../header.php';
//---
if (strpos(__FILE__, "I:\\") !== false) {
    include_once __DIR__ . '/../../../auth/auth/send_edit.php';
    include_once __DIR__ . '/../../../auth/auth/access_helps.php';
} else {
    include_once __DIR__ . '/auth/auth/send_edit.php';
    include_once __DIR__ . '/auth/auth/access_helps.php';
};
//---
include_once __DIR__ . '/fix.php';
//---
use function OAuth\SendEdit\auth_do_edit;
use function OAuth\AccessHelps\get_access_from_db;
//---
print_h3_title("Fix references in Wikipedia's: <a href='https://hashtags.wmcloud.org/?query=mdwiki' target='_blank'>#mdwiki</a>");
//---
// https://hashtags.wmcloud.org/graph/?query=mdwiki&project=&startdate=&enddate=&search_type=or&user=

function endsWith($string, $endString)
{
    $len = strlen($endString);
    return substr($string, -$len) === $endString;
};

function saveit($title, $lang, $text)
{
    global $username;
    // ---
    $summary = "Fix references, Expand infobox #mdwiki .toolforge.org.";
    // ---
    $access = get_access_from_db($username);
    // ---
    if ($access == null) {
        return false;
    };
    // ---
    $access_key = $access['access_key'];
    $access_secret = $access['access_secret'];
    // ---
    $result = auth_do_edit($title, $text, $summary, $lang, $access_key, $access_secret);
    // ---
    $Success = $result['edit']['result'] == 'Success';
    // ---
    return $Success;
}

function worknew($title, $lang, $save, $test, $movedots, $infobox)
{
    $site = "$lang.wikipedia.org";
    //---
    $new = "https://$site/w/index.php?title=$title&action=submit";
    $articleurl = "https://$site/w/index.php?title=$title";
    //---
    $text_re =  <<<HTML
        <h3>
            page: <a target='_blank' href='$articleurl'>$title</a>
        </h3>
    HTML;
    //---
    $summary = "Fix references, Expand infobox #mdwiki .toolforge.org.";
    //---
    $form = <<<HTML
        <form id='editform' name='editform' method='POST' action='$new'>
        <input type='hidden' value='' name='wpEdittime'/>
        <input type='hidden' value='' name='wpStarttime'/>
        <input type='hidden' value='' name='wpScrolltop' id='wpScrolltop'/>
        <input type='hidden' value='12' name='parentRevId'/>
        <input type='hidden' value='wikitext' name='model'/>
        <input type='hidden' value='text/x-wiki' name='format'/>
        <input type='hidden' value='1' name='wpUltimateParam'/>
        <input type='hidden' name='wpSummary' value='$summary'>
        <input type='hidden' id='wikitext-old' value=''>
    HTML;
    //---
    $resultb = get_results($title, $lang, $movedots, $infobox, $test);
    $resultb = trim($resultb);
    //---
    $t3 = endsWith($resultb, '.txt');
    //---
    if ($test) $text_re .= "results:({$resultb})<br>";
    //---
    $edit_link = <<<HTML
        <a type='button' target='_blank' class='btn btn-outline-primary' href='$new'>Open edit new tab.</a>
        <a type='button' target='_blank' class='btn btn-outline-primary' href='$articleurl'>Open page new tab.</a>
    HTML;
    //---
    $edt_link_row = <<<HTML
        <div class='aligncenter'>
            <div class='col-sm'>
                $edit_link
            </div>
        </div>
    HTML;
    //---
    if ($resultb == 'no changes') {
        $text_re .= "no changes";
        $text_re .= $edt_link_row;
    } elseif ($resultb == "notext") {
        $text_re .= "text == ''";
        $text_re .= $edt_link_row;
        // } elseif ($resultb == "ok") { $text_re .= ("save done.");
    } elseif ($t3 || $test) {
        //---
        $newtext = '';
        if ($resultb != "") $newtext = file_get_contents($resultb);
        //---
        $form = $form . <<<HTML
            <div class='form-group'>
                <label for='find'>new text:</label>
                <textarea id='wikitext-new' class='form-control' name='wpTextbox1'>$newtext</textarea>
            </div>
            <div class='editOptions aligncenter'>
                <input id='wpPreview' type='submit' class='btn btn-outline-primary' tabindex='5' title='[p]' accesskey='p' name='wpPreview' value='Preview changes'/>
                <input id='wpDiff' type='submit' class='btn btn-outline-primary' tabindex='7' name='wpDiff' value='show changes' accesskey='v' title='show changes.'>
                <div class='editButtons'>
                </div>
            </div>
        </form>
        HTML;
        //---
        if ($save != "") {
            $save2 = saveit($title, $lang, $newtext);
            if ($save2) {
                $text_re .= 'changes has published';
            } else {
                $text_re .= 'Changes are not published, try to do it manually.';
                $text_re .= $form;
            }
        } else {
            $text_re .= $form;
        };
        //---
    } else {
        $text_re .= $resultb;
        $text_re .= $edt_link_row;
    };
    //---
    return $text_re;
};

function print_form($title, $lang, $save, $movedots, $infobox, $test, $username)
{
    $testinput = ($test != '') ? '<input type="hidden" name="test" value="1" />' : '';
    //---
    $title2 = add_quotes($title);
    $save_checked  = ($save != "") ? 'checked' : '';
    //---
    $start_icon = "<input class='btn btn-outline-primary' type='submit' value='start'>";
    // ---
    if ($username == '') $start_icon = '<a role="button" class="btn btn-primary" href="/auth/index.php?a=login">Log in</a>';
    // ---
    return <<<HTML
        <form action='fixwikirefs.php' method='GET'>
            $testinput
            <div class='container'>
                <div class='row'>
                    <div class='col-md-4'>
                        <div class='input-group mb-3'>
                            <div class='input-group-prepend'>
                                <span class='input-group-text'>Langcode</span>
                            </div>
                            <input class='form-control' type='text' name='lang' value='$lang' required />
                        </div>
                        <div class='input-group mb-3'>
                            <div class='input-group-prepend'>
                                <span class='input-group-text'>Title</span>
                            </div>
                            <input class='form-control' type='text' id='title' name='title' value=$title2 required />
                        </div>
                    </div>
                    <div class='col-md-3'>
                        <div class='form-check form-switch'>
                            <input class='form-check-input' type='checkbox' id='save' name='save' value='1' $save_checked>
                            <label class='check-label' for='save'>Auto save</label>
                        </div>

                        <div class='form-check form-switch'>
                            <input class='form-check-input' type='checkbox' id='movedots' name='movedots' value='1' $movedots>
                            <label class='form-check-label' for='movedots'>Move dots after references</label>
                        </div>

                        <div class='form-check form-switch'>
                            <input class='form-check-input' type='checkbox' id='infobox' name='infobox' value='1' $infobox>
                            <label class='form-check-label' for='infobox'>Expand Infobox</label>
                        </div>
                    </div>
                    <div class='col-md-5'>
                        <h4 class='aligncenter'>
                            $start_icon
                        </h4>
                    </div>
                </div>
            </div>
        </form>
    HTML;
    //---
}

$test       = $_GET['test'] ?? '';
$title      = $_GET['title'] ?? '';
$save       = isset($_GET['save']) ? 'save' : '';
$movedots   = isset($_GET['movedots']) ? 'checked' : '';
$infobox    = isset($_GET['infobox']) ? 'checked' : '';
$lang       = isset($_GET['lang']) ? trim($_GET['lang']) : '';

echo print_form($title, $lang, $save, $movedots, $infobox, $test, $username);
// ---
echo "</div></div>";
//---
$new_tt = "";
//---
if (!empty($title) && !empty($lang) && $lang != 'en' && !empty($username)) {
    $new_tt = worknew($title, $lang, $save, $test, $movedots, $infobox);
};
//---
echo <<<HTML
<hr />
    <div class='card'>
        <div class="card-header aligncenter" style="font-weight:bold;">
            <h3>
                page: <a target='_blank' href="https://$lang.wikipedia.org/w/index.php?title=$title">$title</a>
            </h3>
        </div>
        <div class='card-body'>
            $new_tt
        </div>
    </div>
HTML;
// ---
echo "</div></div>";
//---
require __DIR__ . '/../footer.php';
