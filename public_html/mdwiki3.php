<?php
require 'header.php';
//---
print_h3_title("Med updater");
//---
$test  = $_GET['test'] ?? '';
$save  = isset($_GET['save']) ? 'checked' : '';
$title = $_GET['title'] ?? '';
//---
$href = '';
$url = '';
//---
if ($title != '') {
    $encoded_title = rawurlencode(str_replace(' ', '_', $title));
    $href = 'https://mdwiki.org/wiki/$encoded_title';
    $url = "<a target='_blank' href='$href'>$title</a>";
}
// ---
// the root path is the first part of the split file path
$pathParts = explode('public_html', __FILE__);
$ROOT_PATH = $pathParts[0];
// echo "ROOT_PATH:$ROOT_PATH<br>";
// ---
echo <<<HTML
    <div class="card-body">
        <form action='mdwiki3.php' method='GET'>
            <div class='container-fluid'>
                <div class='row'>
                    <div class='col-md-3'>
                        <div class='input-group mb-3'>
                            <div class='input-group-prepend'>
                                <span class='input-group-text'>Title</span>
                            </div>
                            <input class='form-control' type='text' id='title' name='title' value='$title' required/>
                        </div>
                    </div>
                    <div class='col-md-2'>
                        <div class='form-check form-switch'>
                            <input class='form-check-input' type='checkbox' id='save' name='save' value='1' $save>
                            <label class='form-check-label' for='save'>Auto save</label>
                        </div>
                    </div>
                    <div class='col-md-2'>
                        <input class='btn btn-outline-primary' type='submit' value='send' />
                    </div>
                </div>
                <div class='input-group'>

                </div>
            </div>
        </form>
HTML;
//---
function strstartswith($text, $start) {
    return strpos($text, $start) === 0;
};
//---
function endsWith($string, $endString) {
    $len = strlen($endString);
    return substr($string, -$len) === $endString;
};
//---
require 'bots/python.php';
//---
function get_results($title) {
    //---
    global $save, $ROOT_PATH, $test;
    //---
    $title2 = str_replace( '+' , '_' , $title );
    $title2 = str_replace( ' ' , '_' , $title2 );
    $title2 = str_replace( '"' , '\\"' , $title2 );
    $title2 = str_replace( "'" , "\\'" , $title2 );
    $title2 = rawurlencode($title2);
    //---
    $sa = ($save != '') ? ' save' : '';
    //---
    $ccc = "-page:$title2 from_toolforge $sa";
    //---
    $params = array(
        'dir' => "$ROOT_PATH/pybot/newupdater",
        'localdir' => '../newupdater',
        'pyfile' => 'med.py',
        'other' => $ccc,
        'test' => $test
    );
    //---
    $result = do_py_sh($params);
    //---
    return $result;
}
//---
function worknew($title) {
    //---
    global $save, $ROOT_PATH;
    //---
    $articleurl = 'https://mdwiki.org' . '/w/index.php?title=' . $title;
    $new = 'https://mdwiki.org' . '/w/index.php?title=' . $title . '&action=submit';
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
        <input type='hidden' name='wpSummary' value='mdwiki changes.'>
        <input type='hidden' id='wikitext-old' value=''>
    HTML;
    //---
    $resultb = get_results($title);
    $resultb = trim($resultb);
    //---
    $t3 = endsWith( $resultb , '.txt' );
    //---
    if (isset($_REQUEST['test'])) echo "results:($resultb)<br>";
    //---
    $edit_link = <<<HTML
        <a type='button' target='_blank' class='btn btn-outline-primary' href='$new'>Open edit new tab.</a>
        <a type='button' target='_blank' class='btn btn-outline-primary' href='$articleurl'>Open page new tab.</a>
    HTML;
    //---
    $edt_link_row = <<<HTML
    <div class='col-sm'>
        $edit_link
    </div>
    HTML;
    //---
    if ($resultb == 'no changes') {
        echo "no changes";
        echo $edt_link_row;
    } elseif ($resultb == "notext") {
        echo "text == ''";
        echo $edt_link_row;
    } elseif ($t3 || isset($_REQUEST['test'])) {
        //---
        $newtext = '';
        if ($resultb != "") $newtext = file_get_contents( $resultb );
        //---
        $form = $form . <<<HTML
            <div class='form-group'>
                <label for='find'>new text:</label>
                <textarea class='form-control' rows='10' name='wpTextbox1'>$newtext</textarea>
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
            if ($resultb == "True") {
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
//---
if ($title != '') {
    worknew($title);
};
//---
require 'footer.php';
//---
