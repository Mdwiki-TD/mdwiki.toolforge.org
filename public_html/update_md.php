<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Define the command for /usr/bin/toolforge jobs
$command = "sh /data/project/mdwiki/update_mdcore.sh";

if (!empty($_GET['o'])) {
    $command = "sh /data/project/mdwiki/public_html/update_md.sh";
}
// Display command command
echo "<br>$command<br>";

// Execute the command and display the result
$result = shell_exec($command);

echo "<pre>";
echo $result;
echo "</pre>";
?>
