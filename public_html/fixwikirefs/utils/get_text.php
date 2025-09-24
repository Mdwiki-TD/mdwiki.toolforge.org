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

$usr_agent = 'WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)';


function from_api($title, $lang)
{
    global $usr_agent;
    $url = "https://{$lang}.wikipedia.org/w/api.php";
    $data = [
        "action" => "query",
        "format" => "json",
        "prop" => "revisions|info",
        "titles" => $title,
        "utf8" => 1,
        "formatversion" => "2",
        "rvprop" => "content",
        "rvslots" => "*"
    ];
    // echo $url . '?' . http_build_query($data) . "<br>";

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_USERAGENT, $usr_agent);

    $response = curl_exec($ch);

    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);

    curl_close($ch);

    if ($response === false || $httpCode !== 200) {
        error_log("Failed to fetch from API: $curlError, HTTP code: $httpCode");
        return '';
    }
    $json = json_decode($response, true);

    $pages = $json['query']['pages'] ?? [];
    // ---
    foreach ($pages as $page) {
        $redirect = $page['redirect'] ?? '';
        // ---
        if (!empty($redirect)) {
            // It's a redirect page
            return 'redirect';
        }
        // ---
        $text = $page['revisions'][0]['slots']['main']['*'] ?? '';
        // ---
        if (!empty($text)) {
            return $text;
        }
        // ---
    }
    // ---
    return '';
}

function from_rest($title, $lang)
{
    global $usr_agent;
    $title = str_replace("/", "%2F", $title);

    $url = "https://{$lang}.wikipedia.org/w/rest.php/v1/page/{$title}";

    $ch = curl_init($url);

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_USERAGENT, $usr_agent);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);

    $output = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);

    if ($output === false) {
        error_log("Failed to fetch from REST API: $curlError");
        return '';
    }
    $json = json_decode($output, true);
    // var_export(json_encode($json, JSON_PRETTY_PRINT));

    if (isset($json['source'])) {
        return $json['source'];
    }

    if ($httpCode !== 200) {
        error_log("REST API returned HTTP code: $httpCode");
    }

    return '';
}

function get_wikipedia_text($title, $lang)
{
    if (empty($title) || empty($lang)) {
        return '';
    }
    // ---
    // Normalize title for both methods
    $title = trim($title);
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
