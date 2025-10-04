<?php
// https://mdwiki.toolforge.org/update_md.php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
//---
// the root path is the first part of the split file path
$ROOT_PATH = explode('public_html', __FILE__)[0];
//---
// Define the command mappings
$commands = [
    'api' => 'update_api.sh',
    'td' => 'update_td.sh',
    'pybot' => 'update_pybot.sh',
    'html' => 'update_html.sh',
];

// Default command
$command = "sh $ROOT_PATH/shs/update_pybot.sh";

// Check if any query parameter is set
foreach ($commands as $param => $script) {
    if (!empty($_GET[$param])) {
        $command = "sh $ROOT_PATH/shs/$script";
        break;
    }
}

// Display command command
echo "<br>$command<br>";

// Execute the command and display the result
$result = @shell_exec($command);

echo "<pre>";
echo $result;
echo "</pre>";
