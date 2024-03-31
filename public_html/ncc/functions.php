<?php
namespace Functions;

if (isset($_GET['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

function ColSm($title, $table)
{
    return <<<HTML
        <div class="card">
            <div class="card-header aligncenter" style="font-weight:bold;">
                $title
            </div>
            <div class="card-body">
                $table
            </div>
            <!-- <div class="card-footer"></div> -->
        </div>
        <br>
    HTML;
};

function make_mdwiki_title($title)
{
    if ($title != '') {
        $encoded_title = rawurlencode(str_replace(' ', '_', $title));
        return "<a target='_blank' href='https://mdwiki.org/wiki/$encoded_title'>$title</a>";
    }
    return $title;
}

function make_target_url($target, $lang, $name = '')
{
    $display_name = ($name != '') ? $name : $target;
    if ($target != '') {
        $encoded_target = rawurlencode(str_replace(' ', '_', $target));
        return "<a target='_blank' href='https://$lang.wikipedia.org/wiki/$encoded_target'>$display_name</a>";
    }
    return $target;
}

function make_view_by_number($target, $numb, $lang) {
    // remove spaces and tab characters
    $target = trim($target);
    $numb2 = ($numb != '') ? $numb : "?";
    $start = '2019-01-01';
    $end = date("Y-m-d", strtotime("yesterday"));
    // https://pageviews.wmcloud.org/?project=sq.wikipedia.org&platform=all-access&agent=all-agents&redirects=0&range=all-time&pages=Sindroma_Asperger
    $url = 'https://pageviews.wmcloud.org/?' . http_build_query( array(
        'project' => "$lang.wikipedia.org",
        'platform' => 'all-access',
        'agent' => 'all-agents',
        // 'start' => $start,
        // 'end' => $end,
        'range' => 'all-time',
        'redirects' => '0',
        'pages' => $target,
    ));
    $start2 = '20190101';

    $hrefjson = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/' . $lang . '.wikipedia/all-access/all-agents/' . rawurlencode($target) . '/monthly/' . $start2 . '/2030010100';

    $link = "<a target='_blank' href='$url'>$numb2</a>";

    if ($numb2 == '?' || $numb2 == 0 || $numb2 == '0') {
        $link = "<a target='_blank' name='toget' hrefjson='$hrefjson' href='$url'>$numb2</a>";
    };
    return $link;
};
