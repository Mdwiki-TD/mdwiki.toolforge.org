<?php
// Include header
require('header.php');

// Output HTML structure
print_h3_title("Fix duplicate redirects.");

// Process request parameters
$start = $_REQUEST['start'] ?? '';
$test = $_REQUEST['test'] ?? '';

// Handle form submission or execute command
if ($start == '') {
    echo <<<HTML
    <form action='dup.php' method='POST'>
        <div class='col-lg-12'>
            <h4 class='aligncenter'>
                <input class='btn btn-primary' type='submit' name='start' value='Start' />
            </h4>
        </div>
    </form>
    HTML;
} else {
    // Define command
    $faf = "/usr/bin/toolforge jobs run fixduplict --image python3.9 --command \"/data/project/mdwiki/local/bin/python3 core8/pwb.py mdpy/dup save\"";

    // Output command if in test mode
    if ($test != '') {
        echo $faf;
    }

    // Execute command and output result
    $result = shell_exec($faf);
    echo $result;
}

// Include footer
require 'footer.php';
?>
