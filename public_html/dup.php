<?php
// Include header
require('header.php');

// Output HTML structure
echo <<<HTML
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Fix duplicate redirects.</h3>
    </div>
    <div class="card-body">
HTML;

// Process request parameters
$start = $_REQUEST['start'] ?? '';
$test = $_REQUEST['test'] ?? '';

// Handle form submission or execute command
if ($start == '') {
    echo "
    <form action='dup.php' method='POST'>
        <div class='col-lg-12'>
            <h4 class='aligncenter'>
                <input class='btn btn-primary' type='submit' name='start' value='Start' />
            </h4>
        </div>
    </form>";
} else {
    // Define command
    $faf = "toolforge jobs run fixduplict --command '/data/project/mdwiki/local/bin/python3 core8/pwb.py mdpy/dup save' --image python3.9";

    // Output command if in test mode
    if ($test != '') {
        echo $faf;
    }

    // Execute command and output result
    $result = shell_exec($faf);
    echo $result;
}

echo '</div>';

// Include footer
require 'foter.php';
?>
