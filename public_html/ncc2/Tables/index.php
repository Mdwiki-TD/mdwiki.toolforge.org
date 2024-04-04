<?php

if (isset($_GET['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};
require 'tables/views.php';

use function ViewsTable\get_views_data;

function get_jsonl_data(): array {
    // read file nc_files.jsonl
    $json = file_get_contents(__DIR__ . '/nc_files.jsonl');
    $data = [];
    foreach (explode("\n", $json) as $line) {
        $line = trim($line);
        if ($line != '') {
            $line_js = json_decode($line, true);
            $lang = $line_js['lang'];
            // ---
            if (!isset($data[$lang])) {
                $data[$lang] = [];
            }
            // ---
            $title = $line_js['title'];
            $data[$lang][] = $title;
        }
    }

    return $data;
}

// $main_cat = 'Translated_from_MDWiki';
$main_cat = 'Files_imported_from_NC_Commons';
$get_lang = $_GET['lang'] ?? '';

$data_oo = get_jsonl_data();

// use array_unique to remove duplicates
$langs_to_titles = array_map('array_unique', $data_oo);

$langs_keys = array_keys($langs_to_titles);

$langs_count_views = [];

// Initialize an array to hold our various counts
$numbers = [
    'Files' => 0,
    'Languages' =>  0,
    'Views' =>  0,
];

// ---
$numbers['Languages'] = count($langs_keys);

$langs_to_titles_views = get_views_data($get_lang, $langs_keys, $langs_to_titles);
// ---
foreach ($langs_to_titles_views as $lang => $tits) {
    // ---
    // echo "<br>lang: $lang, tits: " . json_encode($tits);
    // ---
    $vis = array_sum(array_values($tits));
    // ---
    $langs_count_views[$lang] = $vis;
    // $numbers['Views'] += $vis;
}
// ---
// $langs_count_views["af"] = 500;
// ---
$numbers['Views'] = array_sum($langs_count_views);
// ---
foreach ($langs_to_titles as $lang => $table) {
    $numbers['Files'] += count($table);
}
// ---
$langs_count_files = array_map('count', $langs_to_titles);
// ---
// echo "<br>langs_to_titles: " . json_encode($langs_to_titles);
// echo "<br>langs_count_files: " . json_encode($langs_count_files);
// echo "<br>langs_count_views: " . json_encode($langs_count_views);
// echo "<br>numbers: " . json_encode($numbers);
// echo "<br>langs_to_titles_views: " . json_encode($langs_to_titles_views);
// ---
