<?php

namespace FixWikiRefs\Form;

if (isset($_GET['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

/*

use function FixWikiRefs\Form\print_form;

*/
function quotes($str)
{
    // if str have ' then use "
    // else use '
    $value = "'$str'";
    if (preg_match("/[\']+/", $str)) $value = '"' . $str . '"';
    return $value;
};

function print_form($title, $lang, $save, $movedots, $infobox, $test, $user_name)
{
    $testinput = ($test != '') ? '<input type="hidden" name="test" value="1" />' : '';
    //---
    $title2 = quotes($title);
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
