<?php
// find: ^(\$[^ ]+\s*=\s*)\$_REQUEST\[(['"][^'"]+['"])\]\s*\?\?
// replace: $1$_GET[$2] ?? $_POST[$2] ??

if (isset($_GET['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}
include_once __DIR__ . '/../header.php';
//---
// Output HTML structure
echo <<<HTML
    <div class="card">
        <div class="card-header aligncenter" style="font-weight:bold;">
            <h3>Fix duplicate redirects.</h3>
        </div>
        <div class="card-body">
HTML;

// Process request parameters
$start = $_POST['start'] ?? '';
$test  = $_GET['test'] ?? $_POST['test'] ?? '';

$testinput = (!empty($test)) ? '<input type="hidden" name="test" value="1" />' : '';
//---
$start_icon = "<input class='btn btn-outline-primary' type='submit' name='start' value='start'>";
// ---
if (empty($GLOBALS['global_username'])) $start_icon = '<a role="button" class="btn btn-primary" href="/auth/index.php?a=login">Log in</a>';
// ---
// Handle form submission or execute command
if (empty($start) || empty($GLOBALS['global_username'])) {
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

    // TODO: Load or validate the script path for fix_duplicate.sh
    // and use the Kubernetes API client to create the job, for example:
    // $job = $client->batchV1()->createNamespacedJob($namespace, $jobSpec);
    // Handle errors and log responses accordingly.

    // Output command if in test mode
    if (!empty($test)) {
        echo $faf;
    }

    // Execute command and output result
    $result = shell_exec($faf);
    echo $result;
}
echo <<<HTML
    </div>
HTML;

// Include footer
include_once __DIR__ . '/../footer.php';
