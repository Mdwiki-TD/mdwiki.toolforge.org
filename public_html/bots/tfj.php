<?php
//---
/*
include_once  'bots/tfj.php';
// $result = do_tfj(array( 'name' => "", 'command' => $command));

/////////
$params = array(
    'name' => '',
    'command' => ''
);
//---
*/
//---
$root_path = trim(getenv('HOME') ?? '') ?: 'I:/mdwiki';
//---
$test   = $_REQUEST['test'] ?? '';
if ($test != '') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};
//---

function make_sh_file_2($string)
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
    return $filepath;
}

function make_command($params)
{
    //---
    global $root_path;
    //---
    $dir        = $params['dir'] ?? '';
    $pyfile     = $params['pyfile'] ?? '';
    $other      = $params['other'] ?? '';
    //---
    $my_dir = $dir;
    //---
    if ($pyfile != '' && $my_dir != '') {
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
        return $command;
    };
    return '';
};


function do_tfj_sh($params, $name) {
    //---
    global $test;
    //---
    $command    = make_command($params);
    //---
    if ($name != '' && $command != '') {
        $escapedCommand = escapeshellcmd($command);
        $toolforge = "toolforge jobs run $name --image python3.9 --command \"$escapedCommand\"";
        //---
        // write commnd to sh file
        $file = make_sh_file_2($toolforge);
        //---
        $sh_command = "sh $file";
        //---
        if ( $_SERVER['SERVER_NAME'] == 'localhost' or $test != '' ) {
            echo "<h6>$toolforge</h6>";
            echo "<h6>$sh_command</h6>";
        };
        //---
        // Passing the toolforge command to the function
        $cmd_output = shell_exec($sh_command);
        //---
        return $cmd_output;
    };
    return '';
};


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
        // write commnd to sh file
        $file = make_sh_file_2($toolforge);
        //---
        $sh_command = "sh $file";
        //---
        // Passing the toolforge command to the function
        $cmd_output = shell_exec($sh_command);
        //---
        return $cmd_output;
    };
    return '';
};
