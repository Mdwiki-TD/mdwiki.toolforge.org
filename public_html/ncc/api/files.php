<?php

header("Content-type: application/json");
$data = [];
// ---
function get_cat_members($cat, $lang)
{
    $files = [];
    // ---    
    if ($cat == '' || $lang == '') {
        return [];
    };
    // ---
    $url = "https://pageviews.wmcloud.org/massviews/api.php?project=$lang.wikipedia.org&category=$cat";
    // ---
    $content = file_get_contents($url);
    // ---
    $data = json_decode($content, true);
    // [{"title":"Chondrosarcoma_of_the_nasal_septum_(Radiopaedia_165701-135935_Sagittal_2).jpeg","ns":6}]
    // ---
    foreach ($data as $key => $tab) {
        // if ns == 6 : title = "File:$title"
        $title = $tab['title'];
        $title = ($tab['ns'] == 6) ? "File:$title" : $title;
        // ---
        $files[] = $title;
    }
    // ---
    return $files;
}
// ---
function get_langs($cat)
{
    $addlenth = $_GET['addlenth'] ?? '';
    // ---
    $langs_by_cat = [];
    $langs_by_cat["Files_imported_from_NC_Commons"] = ["af", "ar"];
    $langs_by_cat["Translated_from_MDWiki"] = ["af", "ar", "es", "fa", "ha", "it", "ja", "or", "pl", "sq"];
    // ---
    $langs = $langs_by_cat[$cat] ?? [];
    // ---
    if ($addlenth != '') {
        $data = [];
        // add lenth of get_cat_members($cat, $lang) to each language
        foreach ($langs as $key => $lang) {
            $data[$lang] = count(get_cat_members($cat, $lang));
        }
        // ---
        $langs = $data;
    }
    // ---
    return $langs;
}
// ---
$cat    = $_GET['cat'] ?? '';
$lang   = $_GET['lang'] ?? '';
$action = $_GET['action'] ?? '';
// ---
$data = [];
// ---
switch ($action) {
    case 'get_cat_members':
        $data = get_cat_members($cat, $lang);
        break;

    case 'get_views':
        $url = '';
        break;

    case 'get_langs':
        $data = get_langs($cat);
        break;

    default:
        $data = [];
        break;
}
// ---
echo json_encode($data);
