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

function makeColSm4($title, $table, $numb = 4, $table2 = '', $title2 = '')
{
    return <<<HTML
        <div class="card mb-3">
            <div class="card-header aligncenter">
                <span class="card-title" style="font-weight:bold;">
                    $title
                </span>
                <div style='float: right'>
                    $title2
                </div>
                <div class="card-tools">
                    <button type="button" class="btn-tool" data-card-widget="collapse"><i class="fas fa-minus"></i></button>
                </div>
            </div>
            <div class="card-body">
                $table
            </div>
            <!-- <div class="card-footer"></div> -->
            $table2
        </div>
    HTML;
};
function ColSm($title, $table)
{
    return <<<HTML
        <div class="card">
            <div class="card-header aligncenter" style="font-weight:bold;">
                <span class="card-title" style="font-weight:bold;">
                    $title
                </span>
                <div class="card-tools">
                    <button type="button" class="btn-tool" data-card-widget="collapse"><i class="fas fa-minus"></i></button>
                </div>
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
