<?php

// https://cxserver.wikimedia.org/v2/page/en/ar/Hippocrates_(disambiguation)
header("Content-type: application/json");
header("Access-Control-Allow-Origin: http://localhost:300");

if (isset($_GET['test'])) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
}

include_once __DIR__ . '/req.php';

$title = $_GET['title'] ?? '';

$HTML_text = "";
$revid = "";

if ($title != '') {
    $tab = get_parse_text($title);
    $HTML_text = $tab[0];
    $revid = $tab[1];
}

// Decode HTML_text using htmlentities
$HTML_text = htmlentities($HTML_text, ENT_QUOTES, 'UTF-8');

// Prepare JSON data
$jsonData = [
    "sourceLanguage" => "mdwiki",
    "title" => $title,
    "revision" => $revid,
    "segmentedContent" => $HTML_text
];

// Encode data as JSON with appropriate options
$jsonOutput = json_encode($jsonData, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);

// Output the JSON
echo $jsonOutput;
