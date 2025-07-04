<?php
if (isset($_GET['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};

include_once __DIR__ . '/../../header.php';
include_once __DIR__ . '/../include.php';
//---
echo <<<HTML
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Fix references in Wikipedia's:</h3>
    </div>
    <div class="card-body">
HTML;
//---
$text       = $_POST['text'] ?? '';
$lang       = $_POST['lang'] ?? '';
$lang = trim($lang);
// ---
$testinput = (!empty($_GET['test'] ?? '')) ? '<input type="hidden" name="test" value="1" />' : '';
//---
echo <<<HTML
    <form action='do_text.php' method='POST'>
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
                </div>
                <div class='col-md-4'>
                    <h4 class='aligncenter'>
                    <input class='btn btn-outline-primary' type='submit' value='start'>
                    </h4>
                </div>
                <div class='col-md-12'>
                    <div class='input-group mb-3'>
                        <div class='input-group-prepend'>
                            <span class='input-group-text'>text</span>
                        </div>
                        <textarea id='text' class='form-control' name='text'>$text</textarea>
                    </div>
                </div>
            </div>
        </div>
    </form>
HTML;

echo "</div></div>";
//---
require __DIR__ . '/../../footer.php';
