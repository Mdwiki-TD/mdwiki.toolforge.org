<?php
// find: ^\$([^ ]+)\s*=\s*\$_REQUEST\[(['"][^'"]+['"])\]\s*\?\?\s*['"]['"];$
// replace: $1 = $_REQUEST[$2] ?? '';

include_once __DIR__ . '/header.php';
//---
// Output HTML structure
echo <<<HTML
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Fix duplicate redirects.</h3>
    </div>
    <div class="card-body">
HTML;

// Process request parameters
$start = $_REQUEST['start'] ?? '';
$test  = $_REQUEST['test'] ?? '';

$testinput = (!empty($test)) ? '<input type="hidden" name="test" value="1" />' : '';
//---
// global $username;
// ---
$start_icon = "<input class='btn btn-outline-primary' type='submit' name='start' value='start'>";
// ---
if (empty($username)) $start_icon = '<a role="button" class="btn btn-primary" href="/auth/index.php?a=login">Log in</a>';
// ---
// Handle form submission or execute command
if (empty($start) || empty($username)) {
    echo <<<HTML
    <form action='dup.php' method='POST'>
        $testinput
        <div class='col-lg-12'>
            <h4 class='aligncenter'>
                $start_icon
            </h4>
        </div>
    </form>
    HTML;
} else {
    // Define command
    echo "starting....";

    $faf = "kubectl create job dup0 --output=json --image=busybox -- public_html/fix_duplicate.sh";

    // Output command if in test mode
    if (!empty($test)) {
        echo $faf;
    }

    // Execute command and output result
    $result = shell_exec($faf);
    echo $result;
}

// Include footer
include_once __DIR__ . '/footer.php';
