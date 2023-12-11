<?php

// Set error reporting if the 'test' parameter is not empty
if (!empty($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

// Get the base path
$path = explode('/public_html', __FILE__)[0];
$path_escaped = escapeshellarg($path . '/pybot/update_mdcore.sh');

// Define the command for toolforge jobs
$command = "toolforge jobs run updatemd --command '$path_escaped' --image mariadb";

// Display the command
echo "<br>$command<br>";

// Execute the command and display the result
$result = shell_exec($command);
echo $result;

?>
