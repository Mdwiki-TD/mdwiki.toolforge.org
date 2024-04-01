<?php
// https://mdwiki.toolforge.org/update_md.php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Define the command mappings
$commands = [
    'api' => 'update_api.sh',
    'td' => 'update_td.sh',
    'mdcore' => 'update_mdcore.sh',
    'html' => 'update_html.sh', 
];

// Default command
$command = "sh /data/project/mdwiki/shs/update_mdcore.sh";

// Check if any query parameter is set
foreach ($commands as $param => $script) {
    if (!empty($_GET[$param])) {
        $command = "sh /data/project/mdwiki/shs/$script";
        break;
    }
}

// Display command command
echo "<br>$command<br>";

// Execute the command and display the result
$result = shell_exec($command);

echo "<pre>";
echo $result;
echo "</pre>";
?>
