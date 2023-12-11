<?php

require('header.php');

echo <<<HTML
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Create redirects.</h3>
    </div>
    <div class="card-body">
HTML;

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

function printForm() {
    global $title, $titlelist;
    echo <<<HTML
        <form action='redirect.php' method='POST'>
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

function createRedirects() {
    global $title, $titlelist;

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
    $toolforgeCommand = "toolforge jobs run redirectx --command '$command' --image python3.9";

    echo '</span>';
    print "<br>";

    if (isset($_REQUEST['test'])) {
        print $toolforgeCommand;
    }

    $result = shell_exec($toolforgeCommand);
    print $result;
}

if ($title == '' && $titlelist == '') {
    printForm();
} else {
    createRedirects();
}

echo '</div>';
require 'foter.php';
?>