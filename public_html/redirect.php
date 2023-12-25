<?php

require('header.php');

print_h3_title("Create redirects.");
//---
require 'bots/tfj.php';
// $result = do_tfj(array( 'name' => "", 'command' => $command));
//---
$test       = $_REQUEST['test'] ?? '';
$title      = $_REQUEST['title'] ?? '';
$titlelist  = $_REQUEST['titlelist'] ?? '';

function printTitleInput($id, $label, $name, $value) {
    echo <<<HTML
        <div class='col-lg-12'>
            <div class='form-group'>
                <div class='input-group mb-3'>
                    <div class='input-group-prepend'>
                        <span class='input-group-text'>$label:</span>
                    </div>
                    <input class='form-control' type='text' id='$id' name='$name' value='$value'/>
                </div>
            </div>
        </div>
    HTML;
}

function printTextAreaInput($id, $name, $value) {
    echo <<<HTML
        <div class='col-lg-12'>
            <div class='form-group'>
                <div class='input-group mb-3'>
                    <div class='input-group-prepend'>
                        <span class='input-group-text'>$name:</span>
                    </div>
                    <textarea class='form-control' cols='20' rows='7' id='$id' name='$name'>$value</textarea>
                </div>
            </div>
        </div>
    HTML;
}

function printSubmitButton() {
    echo <<<HTML
    <div class='col-lg-12'>
        <h4 class='aligncenter'>
            <input class='btn btn-primary' type='submit' value='send'>
        </h4>
    </div>
HTML;
}

function printForm($title, $titlelist, $test) {
	$testinput = ($test != '') ? '<input type="hidden" name="test" value="1" />' : '';
    echo <<<HTML
        <form action='redirect.php' method='POST'>
            $testinput
            <div class='container'>
                <div class='container'>
                    <div class='row'>
    HTML;

    printTitleInput('title', 'Title', 'title', $title);
    echo <<<HTML
        <div class='col-lg-12'>
            <h3 class='aligncenter'>or</h3>
        </div>
    HTML;
    printTextAreaInput('titlelist', 'List of titles', $titlelist);
    printSubmitButton();

    echo <<<HTML
                        </div>
                    </div>
                </div>
            </div>
        </form>
    HTML;
}

function createRedirects($title, $titlelist, $test) {

    //echo $_SERVER['SERVER_NAME'];
    echo "<span style='font-size:15pt;color:green'>";
    echo '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';

    $file = '/data/project/mdwiki/public_html/texts/redirectlist.txt';

    if ($title != '') {
        $pythonCommand = "-page2:" . rawurlencode($title);
        echo '<span class="">The Bot will create redirects for ' . rawurldecode($title) . ' in seconds.</span>';
    } else {
        $myfile = fopen($file, "w");
        fwrite($myfile, $titlelist);
        fclose($myfile);
        $pythonCommand = "-file:$file";
        echo '<span class="">The Bot will create redirects for titles in the list in seconds.</span>';
    }

    $command = "/data/project/mdwiki/local/bin/python3 core8/pwb.py mdpy/red $pythonCommand save";
    // $toolforgeCommand = "/usr/bin/toolforge jobs run redirectx --image python3.9 --command \"$command\"";

    echo '</span>';
    echo "<br>";

    // $result = shell_exec($toolforgeCommand);
    // ---
    $result = do_tfj(array( 'name' => "redirectx", 'command' => $command));
    // ---
    echo $result;
}

if ($title == '' && $titlelist == '') {
    printForm($title, $titlelist, $test);
} else {
    createRedirects($title, $titlelist, $test);
}

require 'footer.php';
?>