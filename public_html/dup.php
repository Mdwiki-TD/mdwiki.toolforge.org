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
                <input class='btn btn-outline-primary' type='submit' name='start' value='Start' />
            </h4>
        </div>
    </form>
    HTML;
} else {
    // Define command
    // $faf = "kubectl exec -q mdwiki-6fd7885d59-sn5pl -- /bin/sh -c /data/project/mdwiki/public_html/dup.sh";
	
    $faf = "kubectl create job dup --output=json --image=busybox -- public_html/dup.sh";

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
