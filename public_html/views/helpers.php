<?php

if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

function pageviews_link(string $lang, string $title, int $count): string
{
    $lang = ($lang == 'be-x-old') ? 'be-tarask' : $lang;
    $url = "https://pageviews.wmcloud.org/?project=$lang.wikipedia.org&platform=all-access&agent=all-agents&redirects=0&start=2015-07-01&end=2025-06-27&pages=$title";

    return "<a class='item' href='$url' target='_blank'>$count</a>";
}

function split_data_hash($org_data)
{

    $data_with_hash = array_filter($org_data, function ($v, $k) {
        return strpos($k, '#') !== false;
    }, ARRAY_FILTER_USE_BOTH);

    $data = array_diff_key($org_data, $data_with_hash);

    $non_zero = data_not_zero($data);

    $zero = array_diff_key($data, $non_zero);

    return [$data, $data_with_hash, $non_zero, $zero];
}

function get_data($path)
{
    if (!file_exists($path)) return [];

    $text = file_get_contents($path) ?? "";
    if (empty($text)) return [];

    $data = json_decode($text, true) ?? [];

    foreach ($data as $key => $value) {
        // إذا كانت القيمة ليست مصفوفة، نحولها إلى مصفوفة بمفتاح 'all'
        if (!is_array($value)) {
            $data[$key] = ['all' => $value];
        }
    }

    return $data;
}

function data_not_zero($data): array
{
    if (!is_array($data)) return [];

    return array_filter($data, function ($v) {
        return $v['all'] != 0;
    });
}


function build_card_with_table(string $title, string $table_html, string $extra_classes = ''): string
{
    return <<<HTML
        <div class="card $extra_classes">
            <div class="card-header">
                <span class="card-title h2">$title</span>
                <div class="card-tools">
                    <button type="button" class="btn-tool" data-card-widget="collapse">
                        <i class="fas fa-minus"></i>
                    </button>
                </div>
            </div>
            <div class="card-body">
                $table_html
            </div>
        </div>
    HTML;
}
