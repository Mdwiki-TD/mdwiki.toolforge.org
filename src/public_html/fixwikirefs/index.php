<?php

include_once __DIR__ . '/../header.php';
include_once __DIR__ . '/include.php';

use function FixWikiRefs\Fix\get_results_new;
use function FixWikiRefs\SavePage\make_save_result;
use function FixWikiRefs\SavePage\published_alert;

function print_form($title, $lang, $save, $movedots, $infobox, $test, $user_name, $sourcetitle = '', $mdwiki_revid = '', $text = '')
{
    // Escape all inputs
    $title = htmlspecialchars($title, ENT_QUOTES, 'UTF-8');
    $lang = htmlspecialchars($lang, ENT_QUOTES, 'UTF-8');
    $user_name = htmlspecialchars($user_name, ENT_QUOTES, 'UTF-8');
    $sourcetitle = htmlspecialchars($sourcetitle, ENT_QUOTES, 'UTF-8');
    $mdwiki_revid = htmlspecialchars($mdwiki_revid, ENT_QUOTES, 'UTF-8');
    $text = htmlspecialchars($text, ENT_QUOTES, 'UTF-8');

    $testinput = (!empty($_GET['test'] ?? '')) ? '<input type="hidden" name="test" value="1" />' : '';
    //---
    $save_checked  = ($save != "") ? 'checked' : '';
    //---
    $start_icon = "<input class='btn btn-outline-primary' type='submit' value='start'>";
    // ---
    if ($user_name == '') $start_icon = '<a role="button" class="btn btn-primary" href="/auth/login.php">Log in</a>';
    // ---
    return <<<HTML
            <form action='/fixwikirefs.php' method='GET'>
                $testinput
                <div class='container'>
                    <div class='row'>
                        <div class='col-md-4'>
                            <div class='input-group mb-3'>
                                <div class='input-group-prepend'>
                                    <span class='input-group-text'>Langcode</span>
                                </div>
                                <input class='form-control' type='text' id='lang' name='lang' value='$lang' placeholder="e.g., en, ar" required />
                            </div>
                            <div class='input-group mb-3'>
                                <div class='input-group-prepend'>
                                    <span class='input-group-text'>Wikipedia title</span>
                                </div>
                                <input class='form-control' type='text' id='title' name='title' value='$title' required />
                            </div>
                        </div>
                        <div class='col-md-4'>
                            <div class='input-group mb-3'>
                                <div class='input-group-prepend'>
                                    <span class='input-group-text'>MDWiki Source Title</span>
                                </div>
                                <input class='form-control' type='text' id='sourcetitle' name='sourcetitle' value='$sourcetitle' />
                            </div>
                            <div class='input-group mb-3'>
                                <div class='input-group-prepend'>
                                    <span class='input-group-text'>MDWiki Revision ID</span>
                                </div>
                                <input class='form-control' type='text' id='revid' name='revid' value='$mdwiki_revid' />
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
                        <div class='col-md-1'>
                            <h4 class='aligncenter'>
                                $start_icon
                            </h4>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="text" class="form-label">Text Content</label>
                        <textarea class="form-control" id="text" name="text" rows="5">$text</textarea>
                    </div>
                </div>
            </form>
    HTML;
}

function make_result_form($new, $newtext)
{
    $summary = "Fix references, Expand infobox #mdwiki .toolforge.org.";
    //---
    return <<<HTML
        <form id='editform' name='editform' method='POST' action='$new' target='_blank'>
            <input type='hidden' value='' name='wpEdittime'/>
            <input type='hidden' value='' name='wpStarttime'/>
            <input type='hidden' value='' name='wpScrolltop' id='wpScrolltop'/>
            <input type='hidden' value='12' name='parentRevId'/>
            <input type='hidden' value='wikitext' name='model'/>
            <input type='hidden' value='text/x-wiki' name='format'/>
            <input type='hidden' value='1' name='wpUltimateParam'/>
            <input type='hidden' name='wpSummary' value='$summary'>
            <input type='hidden' id='wikitext-old' value=''>
            <div class="mb-3">
                <label for="wikitext-new" class="form-label fw-semibold">
                    📝 New Wikitext
                </label>
                <textarea id="wikitext-new" class="form-control" name="wpTextbox1" rows="5">$newtext</textarea>
            </div>
            <div class='editOptions aligncenter'>
                <input id='wpPreview' type='submit' class='btn btn-outline-primary' tabindex='5' title='[p]' accesskey='p' name='wpPreview' value='Preview changes'/>
                <input id='wpDiff' type='submit' class='btn btn-outline-primary' tabindex='7' name='wpDiff' value='show changes' accesskey='v' title='show changes.'>
                <div class='editButtons'>
                </div>
            </div>
        </form>
    HTML;
}

function worknew($title, $lang, $save, $test, $sourcetitle, $mdwiki_revid, $movedots, $infobox)
{
    $site = "$lang.wikipedia.org";

    $new = "https://$site/w/index.php?title=$title&action=submit";
    $articleurl = "https://$site/w/index.php?title=$title";

    $text_re = "";

    [$err, $resultb] = get_results_new($sourcetitle, $title, $lang, $mdwiki_revid);

    if ($test) $text_re .= "results:({$resultb})<br>";

    $edt_link_row = <<<HTML
        <div class='aligncenter'>
            <div class='col-sm'>
                <a type='button' target='_blank' class='btn btn-outline-primary' href='$new'>Open edit new tab.</a>
                <a type='button' target='_blank' class='btn btn-outline-primary' href='$articleurl'>Open page new tab.</a>
            </div>
        </div>
    HTML;

    if (!empty($err)) {
        $text_re .= published_alert($err, "warning");
        $text_re .= $edt_link_row;
        return $text_re;
    };

    if ($resultb == "redirect") {
        // $text_re .= "text == ''";
        $text_re .= published_alert("Page is redirect", "warning");
        $text_re .= $edt_link_row;
        return $text_re;
    }

    if ($resultb == 'no changes') {
        $text_re .= published_alert("No changes", "warning");
        $text_re .= $edt_link_row;
        return $text_re;
    }

    if ($resultb == "notext") {
        // $text_re .= "text == ''";
        $text_re .= published_alert("No text", "warning");
        $text_re .= $edt_link_row;
        return $text_re;
    }

    $newtext = $resultb;

    if (!empty($save)) {
        return make_save_result($title, $lang, $newtext, $new);
    }

    $text_re .= make_result_form($new, $newtext);

    return $text_re;
}

echo <<<HTML
    <div class="card">
        <div class="card-header aligncenter" style="font-weight:bold;">
            <h3>Fix references in Wikipedia's: <a href='https://hashtags.wmcloud.org/?query=mdwiki' target='_blank'>#mdwiki</a></h3>
        </div>
        <!-- padding bottom 0 -->
        <div class="card-body pb-0">
HTML;

$test         = $_GET['test'] ?? '';
$title        = $_GET['title'] ?? '';
$save         = isset($_GET['save']) ? 'save' : '';
$movedots     = isset($_GET['movedots']) ? 'checked' : '';
$infobox      = isset($_GET['infobox']) ? 'checked' : '';
$lang         = isset($_GET['lang']) ? trim($_GET['lang']) : '';
$sourcetitle  = isset($_GET['sourcetitle']) ? trim($_GET['sourcetitle']) : (isset($_GET['source_title']) ? trim($_GET['source_title']) : '');
$mdwiki_revid = $_GET['revid'] ?? $_GET['mdwiki_revid'] ?? "";
$text         = $_GET['text'] ?? $_POST['text'] ?? '';

$user_name = (isset($GLOBALS['global_username']) && $GLOBALS['global_username'] != '') ? $GLOBALS['global_username'] : '';

echo print_form($title, $lang, $save, $movedots, $infobox, $test, $user_name, $sourcetitle, $mdwiki_revid, $text);

echo "<!-- x --></div></div><!-- x -->";

$new_tt = "";

if (!empty($title) && !empty($lang) && $lang != 'en' && !empty($user_name)) {
    $new_tt = worknew($title, $lang, $save, $test, $sourcetitle, $mdwiki_revid, $movedots, $infobox);
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

echo "</div></div>";

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

include_once __DIR__ . '/footer.php';
