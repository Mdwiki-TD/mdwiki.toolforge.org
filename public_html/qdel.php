<?php
require('header.php');

print_h3_title("qdels");
//---
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

require('footer.php');
?>
