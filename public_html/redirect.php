<?php

require('header.php');

echo <<<HTML
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Create redirects.</h3>
    </div>
    <div class="card-body">
HTML;
//---
$test       = $_REQUEST['test'] ?? '';
$title      = $_REQUEST['title'] ?? '';
$titlelist  = $_REQUEST['titlelist'] ?? '';
//---
// the root path is the first part of the split file path
$pathParts = explode('public_html', __FILE__);
$ROOT_PATH = $pathParts[0];

require 'bots/tfj.php';
//---
function printForm($title, $titlelist, $test)
{
    global $username;
    // ---
    $start_icon = "<input class='btn btn-outline-primary' type='submit' value='send'>";
    // ---
    if (empty($username)) $start_icon = '<a role="button" class="btn btn-primary" href="/auth/index.php?a=login">Log in</a>';
    // ---
    $testinput = (!empty($test)) ? '<input type="hidden" name="test" value="1" />' : '';
    //---
    $rows = <<<HTML
        <div class='col-lg-12'>
            <div class='form-group'>
                <div class='input-group mb-3'>
                    <div class='input-group-prepend'>
                        <span class='input-group-text'>Title:</span>
                    </div>
                    <input class='form-control' type='text' id='title' name='title' value='$title'/>
                </div>
            </div>
        </div>
        <div class='col-lg-12'>
            <h3 class='aligncenter'>or</h3>
        </div>
        <div class='col-lg-12'>
            <div class='form-group'>
                <div class='input-group mb-3'>
                    <div class='input-group-prepend'>
                        <span class='input-group-text'>List of titles:</span>
                    </div>
                    <textarea class='form-control' cols='20' rows='7' id='titlelist' name='titlelist'>$titlelist</textarea>
                </div>
            </div>
        </div>
        <div class='col-lg-12'>
            <h4 class='aligncenter'>
                $start_icon
            </h4>
        </div>
    HTML;

    echo <<<HTML
        <form action='redirect.php' method='POST'>
            $testinput
            <div class='container'>
                <div class='container'>
                    <div class='row'>
                        $rows
                    </div>
                </div>
            </div>
        </form>
    HTML;
}
function get_results($aargs)
{
    //---
    global $test;
    //---
    $ccc = " mdpy/red $aargs save";
    //---
    $params = array(
        'dir' => "core8",
        'localdir' => "core8",
        'pyfile' => 'pwb.py',
        'other' => $ccc,
        'test' => $test
    );
    //---
    $result = do_tfj_sh($params, "redirect");
    //---
    return $result;
}
function createRedirects($title, $titlelist, $test)
{
    //---
    global $ROOT_PATH;
    //---

    //echo $_SERVER['SERVER_NAME'];
    echo "<span style='font-size:15pt;color:green'>";
    echo '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';

    $file = "$ROOT_PATH/public_html/texts/redirectlist.txt";

    if (!empty($title)) {
        $pythonCommand = "-page2:" . rawurlencode($title);
        echo '<span class="">The Bot will create redirects for ' . rawurldecode($title) . ' in seconds.</span>';
    } else {
        $myfile = fopen($file, "w");
        fwrite($myfile, $titlelist);
        fclose($myfile);
        $pythonCommand = "-file:$file";
        echo '<span class="">The Bot will create redirects for titles in the list in seconds.</span>';
    }

    echo '</span>';
    echo "<br>";

    $result = get_results($pythonCommand);
    // ---
    echo $result;
}

if ((empty($title) && empty($titlelist)) || empty($username)) {
    printForm($title, $titlelist, $test);
} else {
    createRedirects($title, $titlelist, $test);
}

require 'footer.php';
