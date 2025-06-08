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
use function FixWikiRefs\SavePage\make_save_result;
use function FixWikiRefs\SavePage\published_success_alert;
use function FixWikiRefs\SavePage\published_danger_alert;
use function FixWikiRefs\Form\make_result_form;
//---
echo <<<HTML
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Fix references in Wikipedia's: <a href='https://hashtags.wmcloud.org/?query=mdwiki' target='_blank'>#mdwiki</a></h3>
    </div>
    <!-- padding bottom 0 -->
    <div class="card-body pb-0">
HTML;

function worknew($title, $lang, $save, $test, $sourcetitle, $movedots, $infobox)
{
    $site = "$lang.wikipedia.org";
    //---
    $new = "https://$site/w/index.php?title=$title&action=submit";
    $articleurl = "https://$site/w/index.php?title=$title";
    //---
    $text_re = "";
    //---
    $resultb = get_results_new($sourcetitle, $title, $lang);
    //---
    if ($test) $text_re .= "results:({$resultb})<br>";
    //---
    $edt_link_row = <<<HTML
        <div class='aligncenter'>
            <div class='col-sm'>
                <a type='button' target='_blank' class='btn btn-outline-primary' href='$new'>Open edit new tab.</a>
                <a type='button' target='_blank' class='btn btn-outline-primary' href='$articleurl'>Open page new tab.</a>
            </div>
        </div>
    HTML;
    //---
    if ($resultb == 'no changes') {
        $text_re .= "no changes";
        $text_re .= $edt_link_row;
        return $text_re;
    }
    // ---
    if ($resultb == "notext") {
        $text_re .= "text == ''";
        $text_re .= $edt_link_row;
        return $text_re;
    }
    // ---
    $newtext = $resultb;
    //---
    if (!empty($save)) {
        return make_save_result($title, $lang, $newtext, $new);
    }
    //---
    $text_re .= make_result_form($new, $newtext);
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
echo "<!-- x --></div></div><!-- x -->";
//---
$new_tt = "";
//---
if (!empty($title) && !empty($lang) && $lang != 'en' && !empty($user_name)) {
    $new_tt = worknew($title, $lang, $save, $test, $sourcetitle, $movedots, $infobox);
    echo <<<HTML
        <!-- <hr /> -->
            <div class='card mt-3'>
                <div class="card-header aligncenter" style="font-weight:bold;">
                    <h3>
                        <i class="bi bi-file-earmark-text"></i>
                        <a target='_blank' href="https://$lang.wikipedia.org/w/index.php?title=$title">$title</a>
                    </h3>
                </div>
                <div class='card-body'>
                    $new_tt
                </div>
            </div>
        HTML;
};
// ---
echo "</div></div>";
//---
echo <<<HTML
    <script>
        // attach autocomplete behavior to input field
        $("#title").autocomplete({
            source: function(request, response) {
                // make AJAX request to Wikipedia API
                $.ajax({
                    url: "https://" + $("#lang").val() + ".wikipedia.org/w/api.php",
                    headers: {
                        'Api-User-Agent': "Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
                    },
                    dataType: "jsonp",
                    data: {
                        action: "query",
                        list: "prefixsearch",
                        format: "json",
                        pssearch: request.term,
                        psnamespace: 0,
                        psbackend: "CirrusSearch",
                        cirrusUseCompletionSuggester: "yes"
                    },
                    success: function(data) {
                        // extract titles from API response and pass to autocomplete
                        response($.map(data.query.prefixsearch, function(item) {
                            return item.title;
                        }));
                    }
                });
            }
        });
    </script>
    HTML;
//---
require __DIR__ . '/footer.php';
