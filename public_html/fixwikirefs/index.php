<?php
if (isset($_GET['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};
//---
include_once __DIR__ . '/../header.php';
include_once __DIR__ . '/include.php';
//---
use function FixWikiRefs\Form\print_form;
use function FixWikiRefs\Fix\get_results_new;
use function FixWikiRefs\SavePage\saveit;
//---
echo <<<HTML
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Fix references in Wikipedia's: <a href='https://hashtags.wmcloud.org/?query=mdwiki' target='_blank'>#mdwiki</a></h3>
    </div>
    <div class="card-body">
HTML;

function worknew($title, $lang, $save, $test, $sourcetitle, $movedots, $infobox)
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
    $resultb = get_results_new($sourcetitle, $title, $lang);
    $resultb = trim($resultb);
    //---
    $newtext = '';
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
    } else {
        //---
        $newtext = $resultb;
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
        }
    };
    //---
    return $text_re;
}

$test       = $_GET['test'] ?? '';
$title      = $_GET['title'] ?? '';
$save       = isset($_GET['save']) ? 'save' : '';
$movedots   = isset($_GET['movedots']) ? 'checked' : '';
$infobox    = isset($_GET['infobox']) ? 'checked' : '';
$lang       = isset($_GET['lang']) ? trim($_GET['lang']) : '';
$sourcetitle       = isset($_GET['sourcetitle']) ? trim($_GET['sourcetitle']) : '';
// ---
$user_name = (isset($GLOBALS['global_username']) && $GLOBALS['global_username'] != '') ? $GLOBALS['global_username'] : '';
// ---
echo print_form($title, $lang, $save, $movedots, $infobox, $test, $user_name);
// ---
echo "</div></div>";
//---
$new_tt = "";
//---
if (!empty($title) && !empty($lang) && $lang != 'en' && !empty($user_name)) {
    $new_tt = worknew($title, $lang, $save, $test, $sourcetitle, $movedots, $infobox);
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
