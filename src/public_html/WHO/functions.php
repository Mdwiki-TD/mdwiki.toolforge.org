<?php
namespace Functions;

if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

function escape_string($unescaped_string)
{
    // Alternative mysql_real_escape_string without mysql connection
    $replacementMap = [
        "\0" => "\\0",
        "\n" => "",
        "\r" => "",
        "\t" => "",
        chr(26) => "\\Z",
        chr(8) => "\\b",
        '"' => '\"',
        "'" => "\'",
        '_' => "\_",
        "%" => "\%",
        '\\' => '\\\\'
    ];

    return \strtr($unescaped_string, $replacementMap);
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
    $url = 'https://pageviews.wmcloud.org/?' . http_build_query( array(
        'project' => "$lang.wikipedia.org",
        'platform' => 'all-access',
        'agent' => 'all-agents',
        'range' => 'all-time',
        'redirects' => '0',
        'pages' => $target,
    ));

    $link = "<a target='_blank' href='$url'>$numb2</a>";
    return $link;
};
