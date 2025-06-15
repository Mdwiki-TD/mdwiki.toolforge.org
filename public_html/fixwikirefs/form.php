<?php

namespace FixWikiRefs\Form;

if (isset($_GET['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

/*

use function FixWikiRefs\Form\print_form;
use function FixWikiRefs\Form\make_result_form;

*/
function print_form($title, $lang, $save, $movedots, $infobox, $test, $user_name)
{
    // Escape all inputs
    $title = htmlspecialchars($title, ENT_QUOTES, 'UTF-8');
    $lang = htmlspecialchars($lang, ENT_QUOTES, 'UTF-8');
    $user_name = htmlspecialchars($user_name, ENT_QUOTES, 'UTF-8');

    $testinput = ($test != '') ? '<input type="hidden" name="test" value="1" />' : '';
    //---
    $save_checked  = ($save != "") ? 'checked' : '';
    //---
    $start_icon = "<input class='btn btn-outline-primary' type='submit' value='start'>";
    // ---
    if ($user_name == '') $start_icon = '<a role="button" class="btn btn-primary" href="/auth/index.php?a=login">Log in</a>';
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
                            <input class='form-control' type='text' id='lang' name='lang' value='$lang' required />
                        </div>
                        <div class='input-group mb-3'>
                            <div class='input-group-prepend'>
                                <span class='input-group-text'>Title</span>
                            </div>
                            <input class='form-control' type='text' id='title' name='title' value='$title' required />
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
