<?php
// Only display errors and startup errors if 'test' is set in the request
if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
	ini_set('display_errors', '1');
	ini_set('display_startup_errors', '1');
	error_reporting(E_ALL);
}

// Get the 'cat' parameter from the request, defaulting to 'all' if it's not present

$get_lang = $_GET['lang'] ?? 'all';
$get_cat  = $_GET['cat'] ?? 'all';

// Initialize an array to hold our various counts
$numbers = [
	'Articles' => 0,
	'Languages' =>  0,
	'LangLinks' =>  0,
	'Views' =>  0,
];

// Read the JSON file into an associative array
$file = file_get_contents("Tables/views.json");
$views_data = json_decode($file, true);

// Count the number of articles (each link is an article)
$numbers['Articles'] = count($views_data);

$md_titles_to_cat = [];
$titles_by_lang = [];
$translators_views = [];

// ---
foreach ($views_data as $mdtitle => $table) {
	foreach ($table as $langcode => $tab) {
		$title = $tab['title'] ?? "";
		$views = $tab['views'] ?? "";
		// ---
		if (!array_key_exists($langcode, $titles_by_lang)) {
			$titles_by_lang[$langcode] = ['titles' => [], 'views' => 0];
		};
		// ---
		$titles_by_lang[$langcode]['titles'][$title] = ['mdtitle' => $mdtitle, 'title' => $title, 'lang' => $langcode, 'views' => $views];
		$titles_by_lang[$langcode]['views'] += $views;
		// ---
	}
}
// ---
# sum views from each lang
$numbers['Views'] = array_sum(array_column($titles_by_lang, 'views'));
// ---
$numbers['LangLinks'] = array_sum(array_map(function ($data) {
	return count($data['titles']);
}, $titles_by_lang));
// ---
$translators = [];
// Identify the top translators by number of
$top_translators = array_map('count', $translators);
arsort($top_translators);
$top_translators = array_slice($top_translators, 0, 156, true);

// count top langs by number of titles count($titles_by_lang[$get_cat]['titles'])

$top_langs = array_map(function ($data) {
	return count($data['titles']);
}, $titles_by_lang);
// ---
$numbers['Languages'] = count($titles_by_lang);
