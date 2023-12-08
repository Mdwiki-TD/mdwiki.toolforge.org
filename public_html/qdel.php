<?php
require('header.php');

echo <<<HTML
    <div class="card-header aligncenter" style="font-weight:bold;">
            <h3>qdels</h3>
    </div>
    <div class="card-body">
HTML;

$job = isset($_GET['job']) ? $_GET['job'] : '';
$qstat = isset($_GET['qstat']) ? $_GET['qstat'] : '';

if (!empty($job)) {
    $result = shell_exec("qdel $job");
    echo $result;
} elseif (!empty($qstat)) {
    $result = shell_exec($qstat);
    print_r($result);
} else {
    header('Location: index.php');
    exit();
}

require('foter.php');
?>
