<?php

// https://mdwiki.org/w/rest.php/v1/page/Sympathetic_crashing_acute_pulmonary_edema/html
// https://mdwiki.org/w/rest.php/v1/revision/1420795/html

header("Content-type: application/json");
header("Access-Control-Allow-Origin: *");

if (isset($_GET['test'])) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
}
require __DIR__ . '/req.php';

$title    = $_GET['title'] ?? '';
$revision = $_GET['revision'] ?? '';
$returntext = $_GET['returntext'] ?? '';

$HTML_text = "";
$revid = "";

if ($title != '' || $revision != '') {
    $HTML_text = get_text_html($title, $revision);
    if ($HTML_text != '') {
        // encode $text
        // $HTML_text = htmlentities($HTML_text, ENT_QUOTES, 'UTF-8');
        $HTML_text = utf8_encode($HTML_text);
    };
}
if ($returntext != '') {
    echo $HTML_text;
    exit;
}
// Decode HTML_text using htmlentities

$jsonData = [
    "sourceLanguage" => "en",
    "title" => $title,
    "revision" => $revid,
    "segmentedContent" => $HTML_text
];

// Encode data as JSON with appropriate options
// $jsonOutput = json_encode($jsonData, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
$jsonOutput = json_encode($jsonData);

// Output the JSON
echo $jsonOutput;
