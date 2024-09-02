<?php
if (isset($_GET['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};

include_once __DIR__ . '/../header.php';
// include_once __DIR__ . '/../Translation_Dashboard/publish/helps.php';
include_once __DIR__ . '/fix.php';
//---
print_h3_title("Fix references in Wikipedia's:");
$test       = $_GET['test'] ?? '';
//---
$text       = $_POST['text'] ?? '';
$lang       = $_POST['lang'] ?? '';
$lang = trim($lang);
// ---
$testinput = ($test != '') ? '<input type="hidden" name="test" value="1" />' : '';
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
require __DIR__ . '/../footer.php';
