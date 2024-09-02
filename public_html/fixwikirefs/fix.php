<?php
include_once __DIR__ . '/../bots/python.php';
//---
// the root path is the first part of the split file path
$pathParts = explode('public_html', __FILE__);
$root_paath = $pathParts[0];
$root_paath = str_replace('\\', '/', $root_paath);
// echo "root_paath:$root_paath<br>";
// ---
function get_results($title, $lang, $movedots, $infobox, $test)
{
    //---
    global $root_paath;
    //---
    $title2 = str_replace('+', '_', $title);
    $title2 = str_replace(' ', '_', $title2);
    $title2 = str_replace('"', '\\"', $title2);
    $title2 = str_replace("'", "\\'", $title2);
    $title2 = rawurlencode($title2);
    //---
    $mv = '';
    if ($movedots != '') $mv .= 'movedots';
    if ($infobox != '')  $mv .= ' infobox';
    //---
    $ccc = "returnfile -page:$title2 -lang:$lang $mv";
    //---
    $params = array(
        'dir' => $root_paath . "/pybot/wprefs",
        'localdir' => $root_paath . "/pybot/wprefs",
        'pyfile' => 'bot1.py',
        'other' => $ccc,
        'test' => $test
    );
    //---
    $result = do_py($params);
    //---
    return $result;
}

function get_text_results($text, $lang)
{

    global $root_paath;
    //---
    $test = $_GET['test'] ?? '';
    //---
    // write $text to file
    $file_name = rand(10000, 99999) . '.txt';
    $file_name = "texts/$file_name";
    // ---
    file_put_contents(__DIR__ . "/$file_name", $text);
    //---
    $ccc = "returnfile -file:$file_name -lang:$lang";
    //---
    $params = array(
        'dir' => $root_paath . "/pybot/wprefs",
        'localdir' => $root_paath . "/pybot/wprefs",
        'pyfile' => 'bot1.py',
        'other' => $ccc,
        'test' => $test
    );
    //---
    $result = do_py2($params);
    //---
    return $result;
}
