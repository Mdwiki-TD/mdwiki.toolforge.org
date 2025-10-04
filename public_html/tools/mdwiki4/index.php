<?php
if (isset($_GET['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

function endsWith($string, $endString)
{
    $len = strlen($endString);
    return substr($string, -$len) === $endString;
};

function do_py_new($params)
{
    //---
    $root_path = getenv('HOME') ?: 'I:/mdwiki';
    //---
    $dir        = $params['dir'] ?? '';
    $localdir   = $params['localdir'] ?? '';
    $pyfile     = $params['pyfile'] ?? '';
    $other      = $params['other'] ?? '';
    //---
    $py3 = $root_path . "/local/bin/python3";
    //---
    $my_dir = $dir;
    //---
    if ($_SERVER['SERVER_NAME'] == 'localhost') {
        $my_dir = $localdir;
        $py3 = "python3";
    };
    //---
    $cmd_output = "";
    $command = "";
    //---
    if ($pyfile != '' && $my_dir != '') {
        $command = $py3 . " $my_dir/$pyfile $other";
        //---
        // replace // with /
        $command = str_replace('//', '/', $command);
        //---
        // Passing the command to the function
        $cmd_output = shell_exec($command);
    };
    // ---
    return [$cmd_output, $command];
}

function get_results($title, $save)
{
    //---
    $root_path = getenv('HOME') ?: 'I:/mdwiki';
    //---
    $titlex = str_replace(['+', ' '], '_', $title);
    // $titlex = str_replace('"', '\\"', $titlex);
    // $titlex = str_replace("'", "\\'", $titlex);
    $titlex = rawurlencode($titlex);
    //---
    $sa = (!empty($save)) ? ' save' : '';
    //---
    $ccc = "-page:$titlex from_toolforge $sa";
    //---
    $params = array(
        'dir' => $root_path . "/pybot/newupdater",
        'localdir' => $root_path . "/pybot/newupdater",
        'pyfile' => 'med.py',
        'other' => $ccc
    );
    //---
    return do_py_new($params);
}

function generateEditForm($title, $newtext = '')
{
    //---
    $site = "mdwiki.org";
    $new = "https://$site/w/index.php?title=$title&action=submit";
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
    if (!empty($newtext)) {
        $form .= <<<HTML
            <div class='form-group'>
                <label for='find'>new text:</label>
                <textarea id='wikitext-new' class='form-control' name='wpTextbox1' rows='5'>$newtext</textarea>
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
    //---
    return $form;
}

function make_title_form($test, $title, $save_checked)
{
    $title3 = htmlspecialchars($title, ENT_QUOTES, 'UTF-8');
    // ---
    $start_icon = "<input class='btn btn-outline-primary' type='submit' value='send' />";
    // ---
    if (empty($GLOBALS['global_username'])) $start_icon = '<a role="button" class="btn btn-primary" href="/auth/index.php?a=login">Log in</a>';
    // ---
    $testinput = (!empty($test)) ? '<input type="hidden" name="test" value="1" />' : '';
    //---
    return <<<HTML
        <form action='mdwiki4.php' method='GET'>
            $testinput
            <div class='container'>
                <div class='row'>
                    <div class='col-md-4'>
                        <div class='input-group mb-3'>
                            <div class='input-group-prepend'>
                                <span class='input-group-text'>Title</span>
                            </div>
                            <input class='form-control' type='text' id='title' name='title' value="$title3" required />
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
}

function worknew($title, $test, $save)
{
    [$resultb, $command] = get_results($title, $save) ?? '';
    //---
    $resultHtml = '';
    //---
    if ($_SERVER['SERVER_NAME'] == 'localhost' || $test != '') {
        $resultHtml .= "<h6>$command</h6>";
    };
    //---
    $resultb = trim($resultb);
    //---
    $t3 = endsWith($resultb, '.txt');
    //---
    if ($test) {
        $resultHtml .= "results:<br>";
        $resultHtml .= "<pre>" . htmlspecialchars($resultb, ENT_QUOTES, 'UTF-8') . "</pre>";
    }
    //---
    $site = "mdwiki.org";
    //---
    $new = "https://$site/w/index.php?title=$title&action=submit";
    $articleurl = "https://$site/w/index.php?title=$title";
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
        $resultHtml .= "no changes";
        $resultHtml .= $edt_link_row;
    } elseif ($resultb == "save ok") {
        $resultHtml .= "<div class='alert alert-success'>Changes has published</div>";
    } elseif ($resultb == "notext") {
        $resultHtml .= "text == ''";
        $resultHtml .= $edt_link_row;
    } elseif (!$t3) {
        $resultHtml .= "<pre>" . htmlspecialchars($resultb, ENT_QUOTES, 'UTF-8') . "</pre>";
        $resultHtml .= $edt_link_row;
    }
    // ---
    if ($t3 || $test) {
        //---
        $newtext = $t3 ? file_get_contents($resultb) : '';
        //---
        $form = generateEditForm($title, $newtext);
        //---
        if (!empty($save)) {
            $resultHtml .= "<div class='alert alert-warning'>Changes are not published, try to do it manually.</div>";
        }
        //---
        $resultHtml .= $form;
    }
    //---
    return $resultHtml;
}

$test         = $_GET['test'] ?? '';
$title        = $_GET['title'] ?? '';
$save         = isset($_GET['save']) ? 'save' : '';
$save_checked = isset($_GET['save']) ? 'checked' : '';
//---
$title_form = make_title_form($test, $title, $save_checked);
// ---
echo <<<HTML
    <div class="card">
        <div class="card-header aligncenter" style="font-weight:bold;">
            <h3>Med updater</h3>
        </div>
        <div class="card-body">
            $title_form
        </div>
    </div>
    <hr />
HTML;
// ---
$result = "";
// ---
if (empty($GLOBALS['global_username'])) {
    $result = "<div class='alert alert-warning'>log in!!</div>";
};
// ---
if (!empty($title) && !empty($GLOBALS['global_username'])) {
    $result = worknew($title, $test, $save);
};
// ---
echo <<<HTML
    <div class='card'>
        <div class="card-header aligncenter" style="font-weight:bold;">
            <h3>
                page: <a target='_blank' href="https://mdwiki.org/w/index.php?title=$title">$title</a>
            </h3>
        </div>
        <div class='card-body'>
            $result
        </div>
    </div>
HTML;
