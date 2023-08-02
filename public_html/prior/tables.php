<?PHP
//---
if (isset($_REQUEST['test'])) {
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);
};
//---
$get_lang = $_REQUEST['lang'] ?? 'all';
//---
$numbers = [
	'Articles' => [],
	// 'Langlinks' =>  [],
	'Languages' =>  [],
	'Translations' =>  [],
	'Translators' =>  [],
	'Views' =>  0,
	'Words' => 0
];
//---
$tables = array(
	'tab_new' => &$tab_new
);
//---
foreach ($tables as $key => &$value) {
	$file = file_get_contents("Tables/{$key}.json");
	$value = json_decode($file, true);
}
//---
$links_by_section = $tab_new['links'];
//---
$numbers['Articles'] = count($links_by_section);
//---
$translates = $tab_new['translates'];
//---
$md_titles_to_section = [];
//---
foreach ($links_by_section as $key => $table) {
	$md_titles_to_section[$key] = $table['section'];
}
//---
$translates_by_lang = [];
//---
$translators = [];
$translators_views = [];
$translators_words = [];
//---
foreach ($translates as $key => $value) {
	// {"mdtitle": "Furosemide","target": "","lang": "th","views": 41123,"words": 253,"translator": "Horus","tr_type": "translator"}
	//---
	$lang   = $value['lang'];
	$target = $value['target'];
	//---
	if (!isset($translates_by_lang[$lang]))	$translates_by_lang[$lang] = ['titles' => [], 'views' => 0, 'words' => 0];
	//---
	$words = $value['words'];
	$views = $value['views'];
	//---

	//---
	if ($get_lang !== $lang && $get_lang !== 'all') continue;
	//---
	$translates_by_lang[$lang]['titles'][$value['mdtitle']] = $value;
	//---
	$translates_by_lang[$lang]['views'] += $views;
	$translates_by_lang[$lang]['words'] += $words;
	//---
	$numbers['Views'] += $views;
	$numbers['Words'] += $words;
	//---
	if ($value['translator'] !== '') {
		if (!isset($translators[$value['translator']])) 	$translators[$value['translator']] = array();
		$translators[$value['translator']][] = $value;
		//---
		if (!isset($translators_views[$value['translator']]))	$translators_views[$value['translator']] = 0;
		$translators_views[$value['translator']] += $views;
		//---
		if (!isset($translators_words[$value['translator']]))	$translators_words[$value['translator']] = 0;
		$translators_words[$value['translator']] += $words;
	};
	//---
}
//---
$numbers['Translations'] = count($translates);
if ($get_lang !== 'all') {
	$numbers['Translations'] = count($translates_by_lang[$get_lang]['titles']);
}
//---
$numbers['Languages']   = count($translates_by_lang);
$numbers['Translators'] = count($translators);
//---
$top_translators = [];
//---
// get top 10 translators by count of translations
foreach ($translators as $key => $value) {
	$top_translators[$key] = count($value);
}
//---
arsort($top_translators);
//---
$top_translators = array_slice($top_translators, 0, 156);
//---
?>