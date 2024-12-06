<?php
// Include header
require('header.php');
//---
// the root path is the first part of the split file path
$pathParts = explode('public_html', __FILE__);
$ROOT_PATH = $pathParts[0];
//---
// Output HTML structure
print_h3_title("Fix duplicate redirects.");

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
    // $faf = "kubectl exec -q mdwiki-6fd7885d59-sn5pl -- /bin/sh -c $ROOT_PATH/public_html/dup.sh";

    $faf = "kubectl create job dup --output=json --image=busybox -- public_html/dup.sh";

    // Output command if in test mode
    if (!empty($test)) {
        echo $faf;
    }

    // Execute command and output result
    $result = shell_exec($faf);
    echo $result;
}

// Include footer
require 'footer.php';
?>
