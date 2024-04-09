<?php

namespace ViewsTable;
use function Functions\fix_name_space;

function get_title_views($title, $lang) {
    $views = 0;
    // ---
    $target = fix_name_space($title, $lang);
    // ---
    $hrefjson = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/' . $lang . '.wikipedia/all-access/all-agents/' . rawurlencode($target) . '/daily/2015070100/2030010100';
    // ---
    $req = file_get_contents($hrefjson) ?? '';
    if (empty($req)) {
        return 0;
    }
    // ---
    $data = json_decode($req, true);
    // ---
    if (is_null($data)) {
        return 0;
    }
    $items = $data['items'] ?? [];
    // ---
    // echo "<br>data:" . json_encode($data);
    // ---
    if (count($items) > 0) {
        $views = array_sum(array_column($items, 'views'));
        // echo "<br>$target: $views";
    }
    // ---
    return $views;
}
function get_views_for_lang($lang, $titles) : array {
    // ---
    // for each title use get_title_views($title, $lang)
    $data = [];
    foreach ($titles as $title) {
        $data[$title] = get_title_views($title, $lang);
    }
    // ---
    return $data;
}

function get_views_data($get_lang, $langs_keys, $langs_to_titles) : array {
    if ($get_lang != '') {
        $langs_keys = [$get_lang];
    }
    // ---
    $langs_to_t_v = [];
    // ---
    foreach ($langs_keys as $lang) {
        $titles = $langs_to_titles[$lang] ?? [];
        $langs_to_t_v[$lang] = get_views_for_lang($lang, $titles);
    }
    // ---
    // echo "<br>langs_to_t_v: " . json_encode($langs_to_t_v);
    // ---
    return $langs_to_t_v;
}