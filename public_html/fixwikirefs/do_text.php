<?php
header('Content-Type: application/json');

include_once __DIR__ . '/fix.php';

function endsWith($string, $endString)
{
    $len = strlen($endString);
    return substr($string, -$len) === $endString;
};

$text = $_POST['text'] ?? '';
$lang = $_POST['lang'] ?? '';

// $text = $_REQUEST['text'] ?? '';
// $lang = $_REQUEST['lang'] ?? '';

$newtext = "";

if ($text != '' && $lang != '') {
    //---
    $resultb = get_text_results($text, $lang);
    // ---
    // ["command" => $ccc, "output" => $result];
    $command = $resultb['command'] ?? '';
    $resultb = $resultb['output'] ?? '';
    // ---
    $command = trim($command);
    $resultb = trim($resultb);
    // ---
    $t3 = endsWith($resultb, '.txt');
    //---
    if ($t3) {
        $newtext = file_get_contents($resultb);
    };
    //---
    echo json_encode(['newtext' => $newtext, 'result' => $resultb, 'command' => $command]);
} else {
    echo json_encode(['error' => 'text or lang is empty', 'text' => $text, 'lang' => $lang]);
}
