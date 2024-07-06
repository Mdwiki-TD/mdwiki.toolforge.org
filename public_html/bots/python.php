<?php
//---
/*
require 'bots/python.php';
$result = do_py($params);

/////////
$params = array(
    'dir' => '',
    'localdir' => '',
    'pyfile' => '',
    'other' => '',
    'test' => $_REQUEST['test']
);
$params['other'] .= '';
$url = "bots/python.php?" . http_build_query( $params );
//---
$output = file_get_contents($url);
*/
//---
// the root path is the first part of the split file path
$pathParts = explode('public_html', __FILE__);
$ROOT_PATH = $pathParts[0];
//---

$test   = $_REQUEST['test'] ?? '';
if ($test != '') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};
//---
function do_py($params) {
    //---
    global $ROOT_PATH, $test;
    //---
    $dir        = $params['dir'] ?? '';
    $localdir   = $params['localdir'] ?? '';
    $pyfile     = $params['pyfile'] ?? '';
    $other      = $params['other'] ?? '';
    //---
    $my_dir = $dir;
    //---
    if ( $_SERVER['SERVER_NAME'] == 'localhost' ) $my_dir = $localdir;
    //---
    if ($pyfile != '' && $my_dir != '') {
        $command = "$ROOT_PATH/local/bin/python3 $my_dir/$pyfile $other";
        //---
        if ( $_SERVER['SERVER_NAME'] == 'localhost' or $test != '' ) { 
            echo "<h6>$command</h6>";
        };
        //---
        // Passing the command to the function
        $cmd_output = shell_exec($command);
        //---
        return $cmd_output;
    };
    return '';
};
?>