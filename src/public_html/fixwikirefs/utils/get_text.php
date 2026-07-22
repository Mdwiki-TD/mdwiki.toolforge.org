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


function test_print_o($s)
{
    if (isset($_COOKIE['test']) && $_COOKIE['test'] == 'x') {
        return;
    }
    $print_t = (isset($_REQUEST['test']) || isset($_COOKIE['test'])) ? true : false;

    if ($print_t && gettype($s) == 'string') {
        echo "\n<br>\n$s";
    } elseif ($print_t) {
        echo "\n<br>\n";
        print_r($s);
    }
}

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
    // echo $url . '?' . http_build_query($data, '', '&', PHP_QUERY_RFC3986) . "<br>";

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data, '', '&', PHP_QUERY_RFC3986));
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_USERAGENT, $usr_agent);

    $response = curl_exec($ch);

    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    //---
    $url2 = $url . '?' . http_build_query($data, '', '&', PHP_QUERY_RFC3986);
    // ---
    // remove "&format=json" from $url2 then make it link <a href="$url2">
    $url2 = str_replace('&format=json', '', $url2);
    $url2 = "<a target='_blank' href='$url2'>$url2</a>";
    //---
    test_print_o("post_url: (http_code: $httpCode) $url2");
    // ---
    curl_close($ch);

    if ($response === false || $httpCode !== 200) {
        error_log("Failed to fetch from API: $curlError, HTTP code: $httpCode");
        return ["Failed to fetch from API: $curlError", ''];
    }
    $json = json_decode($response, true);

    $pages = $json['query']['pages'] ?? [];
    // ---
    foreach ($pages as $page) {
        $missing = $page['missing'] ?? '';
        $redirect = $page['redirect'] ?? '';
        // ---
        if (!empty($redirect)) {
            return ['Page is redirect', ""];
        }
        // ---
        if (!empty($missing)) {
            return ['Page is missing', ""];
        }
        // ---
        $main = $page['revisions'][0]['slots']['main'] ?? [];
        $text = $main['content'] ?? $main['*'] ?? '';
        // ---
        if (!empty($text)) {
            return ["", $text];
        }
    }
    // ---
    return ["notext", ""];
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
        return ["Failed to fetch from REST API: $curlError", ''];
    }
    $json = json_decode($output, true);
    // var_export(json_encode($json, JSON_PRETTY_PRINT));

    if (isset($json['source'])) {
        return ["", $json['source']];
    }

    if ($httpCode !== 200) {
        error_log("REST API returned HTTP code: $httpCode");
        return ["REST API returned HTTP code: $httpCode", ''];
    }

    return ["notext", ""];
}

function get_wikipedia_text($title, $lang)
{
    if (empty($title)) {
        return ["title is empty", ""];
    }
    // ---
    if (empty($lang)) {
        return ["lang is empty", ""];
    }
    // ---
    // Normalize title for both methods
    $title = trim($title);
    // ---
    [$err, $text] = from_api($title, $lang);
    // ---
    if (empty($text) && $err === "notext") {
        [$err, $text] = from_rest($title, $lang);
    }
    // ---
    return [$err, $text];
}
