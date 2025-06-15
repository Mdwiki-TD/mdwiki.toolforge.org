<?php
include_once __DIR__ . '/header.php';
// include_once __DIR__ . '/bots/python.php';
//---
function add_quote($str)
{
    // if str have ' then use "
    // else use '
    $value = "'$str'";
    if (preg_match("/[\']+/", $str)) $value = '"' . $str . '"';
    return $value;
}
//---
echo <<<HTML
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Med updater</h3>
    </div>
    <div class="card-body">
HTML;
//---
$test       = $_GET['test'] ?? '';
$title      = $_GET['title'] ?? '';
$save       = isset($_GET['save']) ? 'save' : '';
$save_checked  = isset($_GET['save']) ? 'checked' : '';
//---
$href = '';
$url = '';
//---
if (!empty($title)) {
    $encoded_title = rawurlencode(str_replace(' ', '_', $title));
    $href = 'https://mdwiki.org/wiki/$encoded_title';
    $url = "<a target='_blank' href='$href'>$title</a>";
}
// ---
// the root path is the first part of the split file path
$pathParts = explode('public_html', __FILE__);
$root_paath = $pathParts[0];
$root_paath = str_replace('\\', '/', $root_paath);
// ---
if (strpos($root_paath, "I:/") !== false) {
    $root_paath = "I:/mdwiki/";
}
// ---
$title2 = add_quote($title);
// ---
$test  = $_GET['test'] ?? '';
$testinput = (!empty($test)) ? '<input type="hidden" name="test" value="1" />' : '';
//---
$start_icon = "<input class='btn btn-outline-primary' type='submit' value='send' />";
// ---
if (empty($username)) $start_icon = '<a role="button" class="btn btn-primary" href="/auth/index.php?a=login">Log in</a>';
// ---
function strstartswith($text, $start)
{
    return strpos($text, $start) === 0;
}

function endsWith($string, $endString)
{
    $len = strlen($endString);
    return substr($string, -$len) === $endString;
};
function do_py($params, $do_test = true, $return_commaand = false)
{
    //---
    global $root_paath;
    //---
    $dir        = $params['dir'] ?? '';
    $localdir   = $params['localdir'] ?? '';
    $pyfile     = $params['pyfile'] ?? '';
    $other      = $params['other'] ?? '';
    //---
    $test = isset($_REQUEST['test']) ? $_REQUEST['test'] : '';
    //---
    $py3 = $root_paath . "/local/bin/python3";
    //---
    $my_dir = $dir;
    //---
    if ($_SERVER['SERVER_NAME'] == 'localhost') {
        $my_dir = $localdir;
        $py3 = "python3";
    };
    //---
    if ($pyfile != '' && $my_dir != '') {
        $command = $py3 . " $my_dir/$pyfile $other";
        //---
        // replace // with /
        $command = str_replace('//', '/', $command);
        //---
        if ($do_test == true) {
            if ($_SERVER['SERVER_NAME'] == 'localhost' || $test != '') {
                echo "<h6>$command</h6>";
            };
        };
        //---
        // Passing the command to the function
        $cmd_output = shell_exec($command);
        //---
        if ($return_commaand == true) {
            return ["command" => $command, "output" => $cmd_output];
        }
        //---
        return $cmd_output;
    };
    return '';
}

function get_results($title)
{
    //---
    global $save, $root_paath, $test;
    //---
    $title2 = str_replace('+', '_', $title);
    $title2 = str_replace(' ', '_', $title2);
    $title2 = str_replace('"', '\\"', $title2);
    $title2 = str_replace("'", "\\'", $title2);
    $title2 = rawurlencode($title2);
    //---
    $sa = (!empty($save)) ? ' save' : '';
    //---
    $ccc = "-page:$title2 from_toolforge $sa";
    //---
    $params = array(
        'dir' => $root_paath . "/pybot/newupdater",
        'localdir' => $root_paath . "/pybot/newupdater",
        'pyfile' => 'med.py',
        'other' => $ccc,
        'test' => $test
    );
    //---
    $result = do_py($params);
    //---
    return $result;
}

function worknew($title)
{
    //---
    global $save, $test;
    //---
    $site = "mdwiki.org";
    //---
    $new = "https://$site/w/index.php?title=$title&action=submit";
    $articleurl = "https://$site/w/index.php?title=$title";
    //---
    $summary = "mdwiki changes.";
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
    $resultb = get_results($title) ?? '';
    //---
    $resultb = trim($resultb);
    //---
    $t3 = endsWith($resultb, '.txt');
    //---
    if ($test) echo "results:({$resultb})<br>";
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
        echo "no changes";
        echo $edt_link_row;
    } elseif ($resultb == "notext") {
        echo "text == ''";
        echo $edt_link_row;
        // } elseif ($resultb == "save ok") { echo ("save done.");
    } elseif ($t3 || $test) {
        //---
        $newtext = '';
        if (!empty($resultb)) $newtext = file_get_contents($resultb);
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
        if (!empty($save)) {
            if ($resultb == "save ok") {
                echo 'changes has published';
            } else {
                echo 'Changes are not published, try to do it manually.';
                echo $form;
            };
        } else {
            echo $form;
        };
        //---
    } else {
        echo $resultb;
        echo $edt_link_row;
    };
    //---
};

echo <<<HTML
    <form action='mdwiki4.php' method='GET'>
        $testinput
        <div class='container'>
            <div class='row'>
                <div class='col-md-4'>
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

echo "</div></div>";

echo <<<HTML
<hr />
    <div class='card'>
        <div class="card-header aligncenter" style="font-weight:bold;">
            <h3>
                page: <a target='_blank' href="https://mdwiki.org/w/index.php?title=$title">$title</a>
            </h3>
        </div>
        <div class='card-body'>
HTML;

if (empty($username)) {
    echo 'log in!!';
};
if (!empty($title) && !empty($username)) {
    worknew($title);
};

echo "</div></div>";

include_once __DIR__ . '/footer.php';
