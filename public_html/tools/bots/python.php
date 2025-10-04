<?php

namespace BOTS\Python;
/*
usage:
include_once __DIR__ . '/bots/python.php';

use function BOTS\Python\do_py;

*/

if (isset($_GET['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}
//---
/*
include_once __DIR__ . '/bots/python.php';
$result = do_py($params);

/////////
$params = array(
    'dir' => '',
    'localdir' => '',
    'pyfile' => '',
    'other' => '',
    'test' => $_GET['test']
);
$params['other'] .= '';
$url = "bots/python.php?" . http_build_query( $params );
//---
$output = file_get_contents($url);
*/
//---
$root_path = trim(getenv('HOME') ?? '') ?: 'I:/mdwiki';
//---
// include_once __DIR__ . '/tfj.php';
//---
function do_py2($params)
{
    //---
    global $root_path;
    //---
    $dir        = $params['dir'] ?? '';
    $localdir   = $params['localdir'] ?? '';
    $pyfile     = $params['pyfile'] ?? '';
    $other      = $params['other'] ?? '';
    //---
    $py3 = $root_path . "/local/bin/python3";
    //---
    $my_dir = $dir;
    //---
    if ($_SERVER['SERVER_NAME'] == 'localhost') {
        $my_dir = $localdir;
        $py3 = "python3";
    };
    //---
    if ($pyfile != '' && $my_dir != '') {
        $command = $py3 . " $my_dir/$pyfile $other";
        //---
        // replace // with /
        $command = str_replace('//', '/', $command);
        //---
        // Passing the command to the function
        $cmd_output = @shell_exec($command);
        //---
        return ["command" => $command, "output" => $cmd_output];
    };
    return [];
}

function do_py($params, $do_test = true, $return_commaand = false)
{
    //---
    global $root_path;
    //---
    $dir        = $params['dir'] ?? '';
    $localdir   = $params['localdir'] ?? '';
    $pyfile     = $params['pyfile'] ?? '';
    $other      = $params['other'] ?? '';
    //---
    $py3 = $root_path . "/local/bin/python3";
    //---
    $my_dir = $dir;
    //---
    if ($_SERVER['SERVER_NAME'] == 'localhost') {
        $my_dir = $localdir;
        $py3 = "python3";
    };
    //---
    if ($pyfile != '' && $my_dir != '') {
        $command = $py3 . " $my_dir/$pyfile $other";
        //---
        // replace // with /
        $command = str_replace('//', '/', $command);
        //---
        if ($do_test == true) {
            if ($_SERVER['SERVER_NAME'] == 'localhost' || ($_GET['test'] ?? "") != '') {
                echo "<h6>$command</h6>";
            };
        };
        //---
        // Passing the command to the function
        $cmd_output = @shell_exec($command);
        //---
        if ($return_commaand == true) {
            return ["command" => $command, "output" => $cmd_output];
        }
        //---
        return $cmd_output;
    };
    return '';
}

function make_sh_file($string)
{
    //---
    // create sh file in sh folder
    $dir = __DIR__ . '/sh';
    // randome title

    $filename = uniqid() . '.sh';

    $filepath = $dir . '/' . $filename;
    //---
    $myfile = fopen($filepath, "w") or die("Unable to open file!");
    // ---
    // change permission
    chmod($filepath, 0755);
    // ---
    $text = "#!/bin/bash" . "\n";
    $text .= 'export PATH=$HOME/openssl/bin:$HOME/local/bin:$HOME/local/bin:/usr/local/bin:/usr/bin:/bin' . "\n";
    $text .= 'export PYWIKIBOT_DIR=$HOME/core8' . "\n";
    $text .= 'cd $PWD' . "\n" . "\n" . $string . "\n";
    //---
    fwrite($myfile, $text);
    fclose($myfile);
    //---
    return  $filepath;
}

function do_py_sh($params)
{
    //---
    global $root_path;
    //---
    if ($_SERVER['SERVER_NAME'] == 'localhost') {
        return do_py($params);
    };
    //---
    $dir        = $params['dir'] ?? '';
    $pyfile     = $params['pyfile'] ?? '';
    $other      = $params['other'] ?? '';
    //---
    $my_dir = $dir;
    //---
    if ($pyfile != '' && $my_dir != '') {
        //---
        // $root_path
        //---
        $uu = "$my_dir/$pyfile";
        //---
        if ($uu == "core8/pwb.py" || $uu == "c8/pwb.py") {
            $uu = $root_path . "/" . $uu;
        }
        //---
        $command = "python3 $uu $other";
        //---
        // replace // with /
        $command = str_replace('//', '/', $command);
        //---
        // write commnd to sh file
        $file = make_sh_file($command);
        //---
        $sh_command = "sh $file";
        //---
        if ($_SERVER['SERVER_NAME'] == 'localhost' || ($_GET['test'] ?? "") != '') {
            echo "<h6>$command</h6>";
            echo "<h6>$sh_command</h6>";
        };
        //---
        // Passing the command to the function
        $cmd_output = @shell_exec($sh_command);
        //---
        return $cmd_output;
    };
    return '';
}
