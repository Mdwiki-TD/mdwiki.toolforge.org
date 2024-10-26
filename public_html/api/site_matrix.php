<?php

namespace API\SiteMatrix;
/*
Usage:
use function API\SiteMatrix\get_site_matrix;
*/

use function API\Langs\get_url_result_curl;
use function API\Langs\get_lang_names;

function site_maxtrix()
{
    // ---
    $params = [
        "action" => "sitematrix",
        "format" => "json",
        "smtype" => "language",
        "smlimit" => "max",
        "utf8" => 1,
        "formatversion" => "2"
    ];
    $end_point = "https://meta.wikimedia.org/w/api.php";

    $url = $end_point . "?" . http_build_query($params);

    $result = get_url_result_curl($url);

    $result = json_decode($result, true);

    $data =  $result['sitematrix'];

    return $data;
}

function by_code($data)
{
    $new = [];

    foreach ($data as $item) {
        $code = $item['code'] ?? '';
        if (empty($code)) {
            continue;
        }
        // ---
        if (isset($item["site"])) unset($item['site']);
        if (isset($item["dir"])) unset($item['dir']);
        // ---
        $item_data = [
            "code" => $code,
            "autonym" => $item['name'] ?? '',
            "name" => $item['localname'] ?? '',
        ];
        // ---
        $new[$code] = $item_data;
    }

    return $new;
}


function fiter_last($data)
{
    $u = get_lang_names();
    // return only if not in $u
    $data = array_filter($data, function ($item) use ($u) {
        return !in_array($item['code'], array_keys($u));
    });

    return $data;
}
function fiter_codes($data)
{
    $skip_t = [
        "wg-en",
        "ten",
        "test",
        "test2",
    ];

    // filter code in $skip_t
    $data = array_filter($data, function ($item) use ($skip_t) {
        return !in_array($item['code'], $skip_t);
    });

    return $data;
}

function get_site_matrix($ty)
{
    $data = site_maxtrix();
    $data = by_code($data);

    // $data = fiter_codes($data);

    if ($ty == "only") {
        $data = fiter_last($data);
    };

    ksort($data);

    return $data;
};
