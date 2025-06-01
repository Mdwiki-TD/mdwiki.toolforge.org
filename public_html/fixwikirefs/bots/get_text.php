<?php

namespace FixWikiRefs\WikiText;

if (isset($_GET['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

/*
usage:

use function FixWikiRefs\WikiText\get_wikipedia_text; // get_wikipedia_text($title, $lang)

*/

function from_api($title, $lang)
{
    $url = "https://{$lang}.wikipedia.org/w/api.php";
    $data = [
        'action' => 'query',
        'format' => 'json',
        'prop' => 'revisions',
        'rvslots' => '*',
        'rvprop' => 'content',
        'titles' => $title,
    ];

    // echo $url . '?' . http_build_query($data) . "<br>";

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    $response = curl_exec($ch);
    curl_close($ch);

    $json = json_decode($response, true);

    $pages = $json['query']['pages'] ?? [];
    // ---
    foreach ($pages as $page) {
        $text = $page['revisions'][0]['slots']['main']['*'] ?? '';
        if (!empty($text)) {
            return $text;
        }
    }
    // ---
    return '';
}

function from_rest($title, $lang)
{
    $usr_agent = 'WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)';

    $title = str_replace("/", "%2F", $title);

    $url = "https://{$lang}.wikipedia.org/w/rest.php/v1/page/{$title}";

    $ch = curl_init($url);

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_USERAGENT, $usr_agent);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);

    $output = curl_exec($ch);
    curl_close($ch);

    $json = json_decode($output, true);
    // var_export(json_encode($json, JSON_PRETTY_PRINT));

    if (isset($json['source'])) {
        return $json['source'];
    }
    return '';
}

function get_wikipedia_text($title, $lang)
{
    // replace / with "%2F"
    // ---
    $text = "";
    // ---
    $text = from_api($title, $lang);
    // ---
    if (empty($text)) {
        $text = from_rest($title, $lang);
    }
    // ---
    return $text;
}
