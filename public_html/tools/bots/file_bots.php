<?php

namespace BOTS\FILE_BOTS;
/*
usage:
include_once __DIR__ . '/bots/file_bots.php';

use function BOTS\FILE_BOTS\dump_to_file;

*/

function dump_to_file($titlelist, $filepath)
{
    //---
    // Ensure directory exists
    if (!is_dir(dirname($filepath))) {
        mkdir(dirname($filepath), 0755, true);
    }
    //---
    $myfile = fopen($filepath, "w");
    //---
    // if (!$myfile) { die("Error: Unable to create temporary file"); }
    //---
    fwrite($myfile, $titlelist);
    fclose($myfile);
    //---
    return $filepath;
}
