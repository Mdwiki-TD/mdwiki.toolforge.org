<?php

header('Content-Type: application/json');

include_once __DIR__ . '/include.php';

use function FixWikiRefs\Fix\get_results_new;

$text = $_POST['text'] ?? '';
$lang = $_POST['lang'] ?? '';
$mdwiki_revid = $_POST['revid'] ?? $_POST['mdwiki_revid'] ?? '';

if ($text != '' && $lang != '') {
    //---
    [$err, $resultb] = get_results_new("!", "!", $lang, $mdwiki_revid, $text);
    // ---
    $newtext = trim($resultb);
    // ---
    echo json_encode(['newtext' => $newtext, 'result' => "", 'command' => "", "err" => $err]);
} else {
    echo json_encode(['error' => 'text or lang is empty', 'text' => $text, 'lang' => $lang]);
}
