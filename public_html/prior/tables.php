<?php
// Only display errors and startup errors if 'test' is set in the request
if (isset($_REQUEST['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
	ini_set('display_errors', '1');
	ini_set('display_startup_errors', '1');
	error_reporting(E_ALL);
}

// Get the 'lang' parameter from the request, defaulting to 'all' if it's not present

$get_lang = $_REQUEST['lang'] ?? 'all';

// Initialize an array to hold our various counts
$numbers = [
	'Articles' => 0,
	// 'Langlinks' =>  [],
	'Languages' =>  0,
	'Translations' =>  0,
	'Translators' =>  0,
	'Views' =>  0,
	'Words' => 0
];

// Read the JSON file into an associative array
$file = file_get_contents("Tables/tab_new.json");
$tab_new = json_decode($file, true);

// Extract the links and translations from the data
$links_by_section = $tab_new['links'];
$translations = $tab_new['translates'];

// Count the number of articles (each link is an article)
$numbers['Articles'] = count($links_by_section);


$md_titles_to_section = [];
foreach ($links_by_section as $key => $table) {
	$md_titles_to_section[$key] = $table['section'];
}

// Initialize arrays to hold our processed data
$translates_by_lang = [];
$translators = [];
$translators_views = [];
$translators_words = [];

function is_ip_address(string $ip_address): bool
{
	// Check if the string is a valid IPv4 address.
	if (filter_var($ip_address, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
		return true;
	}

	// Check if the string is a valid IPv6 address.
	elseif (filter_var($ip_address, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6)) {
		return true;
	}

	return false;
}

// Process each translation
foreach ($translations as $key => $value) {
	// {"mdtitle": "Furosemide","target": "","lang": "th","views": 41123,"words": 253,"translator": "Horus","tr_type": "translator"}
	$lang   = $value['lang'];
	$target = $value['target'];

	// Initialize this language's data if it hasn't been already
	if (!array_key_exists($lang, $translates_by_lang)) {
		$translates_by_lang[$lang] = ['titles' => [], 'views' => 0, 'words' => 0];
	}

	$views = $value['views'];
	$words = $value['words'];
	$translator = $value['translator'];

	// chceck if translator is ip address
	if (is_ip_address($translator)) {
		continue;
	}

	// Skip this translation if we're not looking at 'all' languages and this translation's language doesn't match our filter
	if ($get_lang !== $lang && $get_lang !== 'all') continue;

	// Add this translation's data to the language's totals
	$translates_by_lang[$lang]['titles'][$value['mdtitle']] = $value;
	$translates_by_lang[$lang]['views'] += $views;
	$translates_by_lang[$lang]['words'] += $words;

	// Add this translation's data to the overall totals
	$numbers['Views'] += $views;
	$numbers['Words'] += $words;

	// Process this translation's translator, if it has one
	if (!empty($translator)) {
		// Initialize this translator's data if it hasn't been already
		if (!array_key_exists($translator, $translators)) {
			$translators[$translator] = [];
			$translators_views[$translator] = 0;
			$translators_words[$translator] = 0;
		}

		// Add this translation to the translator's list and its data to the translator's totals
		$translators[$translator][] = $value;
		$translators_views[$translator] += $views;
		$translators_words[$translator] += $words;
	}
}

// Update the overall translation, language, and translator counts
$numbers['Translations'] = count($translations);
if ($get_lang !== 'all') {
	$numbers['Translations'] = count($translates_by_lang[$get_lang]['titles']);
}
$numbers['Languages'] = count($translates_by_lang);
$numbers['Translators'] = count($translators);

// Identify the top translators by number of translations
$top_translators = array_map('count', $translators);

arsort($top_translators);
$top_translators = array_slice($top_translators, 0, 156, true);
