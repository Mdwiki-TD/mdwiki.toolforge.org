<?php
// Only display errors and startup errors if 'test' is set in the request
if (isset($_GET['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
	ini_set('display_errors', '1');
	ini_set('display_startup_errors', '1');
	error_reporting(E_ALL);
}

// Get the 'cat' parameter from the request, defaulting to 'all' if it's not present
// $langs = ["af"];
$langs = ["af", "ar", "es", "fa", "ha", "it", "ja", "or", "pl", "sq"];

$get_lang = $_GET['lang'] ?? '';


// Initialize an array to hold our various counts
$numbers = [
	'Files' => 0,
	'Languages' =>  0,
	'Views' =>  0,
];

// Count the number of Files (each link is an article)
$numbers['Files'] = 0;

// $main_cat = 'Translated_from_MDWiki';
$main_cat = 'Files_imported_from_NC_Commons';
if (isset($_GET['cat'])) {
	$main_cat = $_GET['cat'];
}

function get_views_data_by_lang($lang) {
	global $main_cat;
	$endpoint = "https://pageviews.wmcloud.org/massviews/api.php";
    // ---
    $params = [
		"project" => "$lang.wikipedia.org",
		"category" => $main_cat
	];
    // ---
    // result example: [{"title":"Chondrosarcoma_of_the_nasal_septum_(Radiopaedia_165701-135935_Sagittal_2).jpeg","ns":6}]
    // ---
	$url = $endpoint . '?' . http_build_query($params);
    // ---
	$req = file_get_contents($url);
	// ---
	$data = json_decode($req, true);
	// ---
	$data2 = [];
	// ---
	// add "File:" to each title if ns == 6
	foreach ($data as $key => $value) {
		$data2[$key] = $value;
		$data2[$key]['title'] = ($value['ns'] == 6) ? "File:" . $value['title'] : $value['title'];
	}
	// ---
	return $data2;
}
function get_views_data($get_lang, $langs) {
	global $numbers;
	if ($get_lang != '') {
		$langs = [$get_lang];
	}
	$views_data = [];
	foreach ($langs as $lang) {
		$views_data[$lang] = get_views_data_by_lang($lang);
		$numbers['Files'] += count($views_data[$lang]);
	}

	return $views_data;
}

$views_data = get_views_data($get_lang, $langs);

$titles_by_lang = [];

// echo json_encode($views_data);
// ---
foreach ($views_data as $lang => $table) {
	$titles_by_lang[$lang] = [];
	$titles_by_lang[$lang]['views'] = 0;
	$titles_by_lang[$lang]['titles'] = [];
	foreach ($table as $_ => $tab) {
		// echo json_encode($tab);
		$title = $tab['title'];
		$views = $tab['views'] ?? 0;
		// ---
		if (!array_key_exists($lang, $titles_by_lang)) {
			$titles_by_lang[$lang] = ['titles' => [], 'views' => 0];
		};
		// ---
		$titles_by_lang[$lang]['titles'][$title] = ['title' => $title, 'lang' => $lang, 'views' => $views];
		$titles_by_lang[$lang]['views'] += $views;
		// ---
	}
}
// ---
# sum views from each lang
$numbers['Views'] = array_sum(array_column($titles_by_lang, 'views'));
// ---
$top_langs = array_map(function ($data) {
	return count($data['titles']);
}, $titles_by_lang);
// ---
$numbers['Languages'] = count($titles_by_lang);