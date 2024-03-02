<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Define the command for /usr/bin/toolforge jobs
$command = "sh /data/project/mdwiki/shs/update_mdcore.sh";

if (!empty($_GET['td'])) {
    $command = "sh /data/project/mdwiki/shs/update_td.sh";
}
if (!empty($_GET['api'])) {
    $command = "sh /data/project/mdwiki/shs/update_api.sh";
}
// Display command command
echo "<br>$command<br>";

// Execute the command and display the result
$result = shell_exec($command);

echo "<pre>";
echo $result;
echo "</pre>";
?>
