<?php
require 'header.php';
print_h3_title("Find and replace.");
//---
require 'bots/tfj.php';
// $result = do_tfj(array( 'name' => "", 'command' => $command));
//---
// Initialize variables with default values
$listtype   = $_REQUEST['listtype'] ?? '';
$test       = $_REQUEST['test'] ?? '';
$find       = $_REQUEST['find'] ?? '';
$replace    = $_REQUEST['replace'] ?? '';
$number     = $_REQUEST['number'] ?? '';
$code       = $_REQUEST['code'] ?? '';

// Function to generate radio button
function generateRadioButton($id, $name, $value, $label, $checked = '') {
    return <<<HTML
        <div class='custom-control custom-radio custom-control-inline'>
            <input type='radio' class='custom-control-input' id='$id' name='$name' value='$value' $checked>
            <label class='custom-control-label' for='$id'>$label</label>
        </div>
    HTML;
}

// Function to generate the form
function generateForm($find, $replace, $number, $code, $test) {
    $codeNote = ($code != '' && $code != 'james#99') ? "<span style='font-size:12pt;color:red'>! ($code) is the wrong code.</span>" : '';

    $findRow = <<<HTML
        <div class='form-group'>
            <label for='find'>Find:</label>
            <textarea class='form-control' cols='40' rows='6' id='find' name='find' required>$find</textarea>
        </div>
    HTML;

    $replaceRow = <<<HTML
        <div class='form-group'>
            <label for='replace'>Replace with:</label>
            <textarea class='form-control' cols='40' rows='6' id='replace' name='replace' placeholder='(write empty to replace it with empty value.)' required>$replace</textarea>
        </div>
    HTML;

    $input_1 = <<<HTML
        <div class='input-group mb-3'>
            <div class='input-group-prepend'>
                <span class='input-group-text'>Number of replacements</span>
            </div>
            <input class='form-control' type='number' name='number' value='$number' placeholder='max'/>
        </div>
        <div class='input-group mb-3'>
            <div class='input-group-prepend'>
                <span class='input-group-text'>Code</span>
            </div>
            <input class='form-control' type='text' name='code' value='$code' required/>$codeNote
        </div>
    HTML;

    $test_1 = ($test != '') ? generateRadioButton('c1', 'test', '1', 'Test', '') : '';

    $input_2 =
        generateRadioButton('customRadio2', 'listtype', 'newlist', 'Use API search', 'checked') .
        generateRadioButton('customRadio', 'listtype', 'oldlist', 'Work in all pages') .
        $test_1;

    echo <<<HTML
        <form action='replace.php' method='POST'>
            <div class='container-fluid'>
                <div class='row'>
                    <div class='col-sm'>$findRow</div>
                    <div class='col-sm'>$replaceRow</div>
                </div> 
                <div class='row'>
                    <div class='col-sm'>$input_1</div>
                    <div class='col-sm'>$input_2</div>
                </div>
                <div class='col-lg-12'>
                    <h4 class='aligncenter'>
                        <input class='btn btn-outline-primary' type='submit' value='send'>
                    </h4>
                </div>
            </div>
        </form>
    HTML;
}

// Function to write to a file
function writeToFile($file, $text) {
    $myfile = fopen('find/' . $file, 'w');
    fwrite($myfile, $text);
    fclose($myfile);
}

// Function to perform the replacement
function performReplacement($find, $replace, $number, $listtype, $test) {
    $nn = rand();

    if ($find != '' && $replace != '') {
        writeToFile($nn . '_find.txt', $find);
        writeToFile($nn . '_replace.txt', $replace);
    }

    $rann = '-rand:' . $nn . ' -number:' . $number;

    if ($listtype == 'newlist') {
        $rann .= ' newlist';
    }

    $command = "/data/project/mdwiki/local/bin/python3 core8/pwb.py mdpy/replace1 $rann";
    // $sii = "/usr/bin/toolforge jobs run replace$nn --image python3.9 --command \"$command\"";

    echo <<<HTML
        <span style='font-size:15pt;color:green'>
        <br>
        The bot will start the replacements in seconds.
        <br>
        Log will be <a href="replace-log.php?id=$nn"><b>Here.</b></a>
        </span>
        <br>
    HTML;

    // $result = shell_exec($sii);
    // ---
    $result = do_tfj(array( 'name' => "replace$nn", 'command' => $command));
    // ---
    echo $result;
}

// Main logic

if ($find == '' || $replace == '' || $code == '' || ($code != '' && $code != 'james#99')) {
    generateForm($find, $replace, $number, $code, $test);
} else {
    performReplacement($find, $replace, $number, $listtype, $test);
}

require 'footer.php';
?>
