<?php
if (isset($_GET['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}
include_once __DIR__ . '/../header.php';
include_once __DIR__ . '/bots/tfj.php';
include_once __DIR__ . '/bots/file_bots.php';

use function BOTS\TFJ\do_tfj_sh;
use function BOTS\FILE_BOTS\dump_to_file;

$test       = $_GET['test'] ?? $_POST['test'] ?? '';
$title      = $_GET['title'] ?? $_POST['title'] ?? '';
$titlelist  = $_GET['titlelist'] ?? $_POST['titlelist'] ?? '';
//---
// the root path is the first part of the split file path
$ROOT_PATH = explode('public_html', __FILE__)[0];

function printForm($title, $titlelist, $test)
{
    $start_icon = "<input class='btn btn-outline-primary' type='submit' value='send'>";
    // ---
    if (empty($GLOBALS['global_username'])) $start_icon = '<a role="button" class="btn btn-primary" href="/auth/index.php?a=login">Log in</a>';
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
function createRedirects($title, $titlelist)
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
        $filename = dump_to_file($titlelist, $file);
        // ---
        $pythonCommand = "-file:$filename";
        // ---
        echo '<span class="">The Bot will create redirects for titles in the list in seconds.</span>';
    }

    echo '</span>';
    echo "<br>";

    $result = get_results($pythonCommand);
    // ---
    echo $result;
}

echo <<<HTML
    <div class="card">
        <div class="card-header aligncenter" style="font-weight:bold;">
            <h3>Create redirects.</h3>
        </div>
        <div class="card-body">
HTML;
//---
if ((empty($title) && empty($titlelist)) || empty($GLOBALS['global_username'])) {
    printForm($title, $titlelist, $test);
} else {
    createRedirects($title, $titlelist);
}
echo <<<HTML
    </div>
HTML;
//---

include_once __DIR__ . '/../footer.php';
