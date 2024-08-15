<?php

$usr_agent = 'WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)';

function get_url_params_result(string $url): string
{
    global $usr_agent;
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    // curl_setopt($ch, CURLOPT_COOKIEJAR, "cookie.txt");
    // curl_setopt($ch, CURLOPT_COOKIEFILE, "cookie.txt");
    curl_setopt($ch, CURLOPT_USERAGENT, $usr_agent);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);

    $output = curl_exec($ch);
    curl_close($ch);
    return $output;
}

function get_parse_text(string $title): array
{
    $end_point = "https://mdwiki.org/w/api.php";
    // ---
    $params = [
        "action" => "parse",
        "format" => "json",
        "page" => $title,
        "prop" => "text|revid",
        "parsoid" => 1,
        "utf8" => 1,
        "formatversion" => "2"
    ];
    // ---
    $url = $end_point . '?' . http_build_query($params);
    // ---
    $text = "";
    $revid = 0;
    // ---
    try {
        $res = get_url_params_result($url);
        if ($res) {
            $data = json_decode($res, true);
            $text = $data['parse']['text'];
            $revid = $data['parse']['revid'];
        }
    } catch (Exception $e) {
        $text = "";
    };
    // ---
    return [$text, $revid];
}


function get_text_html($title, $revision) {
    // ---
    // replace " " by "_"
    $title = str_replace(" ", "_", $title);
    // ---
	$url = $revision !== '' ? "https://mdwiki.org/w/rest.php/v1/revision/$revision/html"  : "https://mdwiki.org/w/rest.php/v1/page/$title/html";
    // ---
    $text = "";
    // ---
    try {
        $res = get_url_params_result($url);
        if ($res) {
            $text = $res;
        }
    } catch (Exception $e) {
        $text = "";
    };
    // ---
    return $text;
}
