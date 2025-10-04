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

// the root path is the first part of the split file path
$ROOT_PATH = explode('public_html', __FILE__)[0];
//---
$test       = $_GET['test'] ?? $_POST['test'] ?? '';
$from       = $_GET['from'] ?? $_POST['from'] ?? '';
$title      = $_GET['title'] ?? $_POST['title'] ?? '';
$titlelist  = $_GET['titlelist'] ?? $_POST['titlelist'] ?? '';
//---
$authorized_users = ['Doc James', 'Mr. Ibrahem']; // Consider moving this to a configuration file
$valid_user = in_array($GLOBALS['global_username'] ?? '', $authorized_users);

function get_results($aargs)
{
    //---
    global $test;
    //---
    $ccc = " mdpy/imp $aargs save";
    //---
    $params = array(
        'dir' => "core8",
        'localdir' => "core8",
        'pyfile' => 'pwb.py',
        'other' => $ccc,
        'test' => $test
    );
    //---
    $result = do_tfj_sh($params, "import");
    //---
    return $result;
}

//---
function make_form($test, $title, $titlelist)
{
    global $valid_user;
    // ---
    $codeNote = (!$valid_user && !empty($GLOBALS['global_username'])) ? "<span style='font-size:12pt;color:red'> Access denied.</span>" : '';
    // ---
    $start_icon = (empty($GLOBALS['global_username'])) ? '<a role="button" class="btn btn-primary" href="/auth/index.php?a=login">Log in</a>' : "";
    // ---
    if ($valid_user) {
        $start_icon = "<input class='btn btn-outline-primary' type='submit' value='send'>";
    }
    // ---
    $testinput = (!empty($test)) ? '<input type="hidden" name="test" value="1" />' : '';
    // ---
    return <<<HTML
        <form action='import-history.php' method='POST'>
            $testinput
            <div class='container'>
                <div class='container'>
                    <div class='row'>
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
                            <div class='input-group mb-3'>
                                $codeNote
                            </div>
                        </div>
                        <div class='col-lg-12'>
                            <h4 class='aligncenter'>
                                $start_icon
                            </h4>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    HTML;
    //---
}


echo <<<HTML
    <div class="card">
        <div class="card-header aligncenter" style="font-weight:bold;">
            <h3>Import history from enwiki</h3>
        </div>
        <div class="card-body">
HTML;
//---
if ((empty($titlelist) && empty($title)) || !$valid_user) {
    //---
    echo make_form($test, $title, $titlelist);
    //---
} else {
    //---
    echo "starting...";
    //---
    $command = "";
    //---
    $text = "";
    //---
    if (!empty($title)) {
        $command .= " -page:" . rawurlencode($title) . ' -from:' . rawurlencode($from);
        //---
        $text .= 'The Bot will import ' . rawurldecode($title) . ' history';
        //---
        if (!empty($from)) $text .= ' from (' . rawurldecode($from) . ') in seconds.';
        //---
        $text .= ' in seconds.';
        //---
    } else {
        //---
        $filename = "$ROOT_PATH/public_html/texts/importlist.txt";
        //---
        $filee = dump_to_file($titlelist, $filename);
        //---
        $command .= " -file:" . $filee;
        //---
        $text .= 'The Bot will import history for titles in the list in seconds.';
        //---
    };
    $text = "<span style='font-size:15pt;color:green'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$text</span>";
    //---
    echo "<br>";
    //---
    $result = get_results($command);
    //---
    echo $result;
    //---
}
echo "</div>";

include_once __DIR__ . '/../footer.php';
//---
