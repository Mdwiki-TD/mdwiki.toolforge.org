<?php
//---
/*
require 'bots/tfj.php';
// $result = do_tfj(array( 'name' => "", 'command' => $command));

/////////
$params = array(
    'name' => '',
    'command' => ''
);
//---
*/
//---
$test   = $_REQUEST['test'] ?? '';
if ($test != '') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};
//---
function do_tfj($params) {
    //---
    global $test;
    //---
    $name       = $params['name'] ?? '';
    $command    = $params['command'] ?? '';
    //---
    if ($name != '' && $command != '') {
        $escapedCommand = escapeshellcmd($command);
        $toolforge = "/usr/bin/toolforge jobs run $name --image python3.9 --command \"$escapedCommand\"";
        //---
        if ( $_SERVER['SERVER_NAME'] == 'localhost' or $test != '' ) { 
            echo "<h6>$toolforge</h6>";
        };
        //---
        // Passing the toolforge command to the function
        $cmd_output = shell_exec($toolforge);
        //---
        return $cmd_output;
    };
    return '';
};
?>