<?php

header("Content-type: application/json");
$data = [];
// ---
$cat  = $_GET['cat'] ?? '';
$lang = $_GET['lang'] ?? '';
// ---
$url = '';
// ---
if ($cat != '' && $lang != '') {
    $url = "https://pageviews.wmcloud.org/massviews/api.php?project=$lang.wikipedia.org&category=$cat";
}
// ---
if ($url != '') {
    $content = file_get_contents($url);
    // ---
    $files = [];
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
    echo json_encode($files);
} else {
    echo json_encode($data);
}

