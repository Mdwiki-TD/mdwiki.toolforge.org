<?php

if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

$dir_with_sub = [
    "views_new" => "views_new/all",
];

$base_path = getenv('HOME') ?: __DIR__ . "/../../../";

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

function build_table_head(): string
{
    return <<<HTML
        <thead>
            <tr>
                <th style="width: 10%">#</th>
                <th>Lang</th>
                <th>Titles</th>
                <th>2015</th>
                <th>2016</th>
                <th>2017</th>
                <th>2018</th>
                <th>2019</th>
                <th>2020</th>
                <th>2021</th>
                <th>2022</th>
                <th>2023</th>
                <th>2024</th>
                <th>2025</th>
            </tr>
        </thead>
    HTML;
}


function render_data_all_new(string $base_path, array $all_data): string
{
    $rows_done = '';
    $done_all = 0;

    $all_titles = 0;

    $stats = json_decode(file_get_contents("$base_path/pybot/md_core/update_med_views/views_new/stats.json"), true);

    $count_all = count($stats);

    $i = 1;

    foreach ($stats as $lang => $org_data) {

        $all_titles += $org_data['not_empty'] ?? 0;
        $url_non_0 = "?lang=$lang&data_type=non_zero";

        // ---
        $count = $org_data['not_empty'];
        // ---
        $years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"];
        // ---
        $row = <<<HTML
            <tr>
                <td>$i</td>
                <td>$lang</td>
                <td><a class='item' href='$url_non_0'>$count</a></td>
        HTML;
        // ---
        foreach ($years as $year) {
            $y_count = $org_data['views'][$year] ?? 0;
            $y_count = number_format($y_count);
            $row .= "<td>$y_count</td>";
        };
        // ---
        $row .= "</tr>";
        // ---
        $rows_done .= $row;
        $done_all++;
        $i++;
    }

    $all_titles = number_format($all_titles);

    $header = <<<HTML
        <div class="text-center d-flex align-items-center justify-content-between">
            <span class="h2">All Languages: $count_all</span>
            <span class="h3">All Titles: $all_titles</span>
            <span></span>
        </div>
        <hr/>
    HTML;

    $thead = build_table_head();
    $table_done = "<table class='table table-striped table-bordered table-sm DataTable'>$thead<tbody>$rows_done</tbody></table>";
    $card_done = build_card_with_table("", $table_done, "collapsed-card1");

    return $header . $card_done;
    // ---
}

function get_columns(array $dataset): array
{
    $all_keys = [];
    // ---
    foreach ($dataset as $item) {
        foreach (array_keys($item) as $key) {
            $all_keys[$key] = true;
        }
    }
    $columns = array_keys($all_keys);
    // ---
    sort($columns);
    // ---
    // remove any key < 2015 and not = "all"
    $columns = array_filter($columns, fn($c) => $c == "all" || $c >= "2015");
    // ---
    return $columns;
}

function pageviews_link(string $lang, string $title, int $count): string
{
    $lang = ($lang == 'be-x-old') ? 'be-tarask' : $lang;
    $url = "https://pageviews.wmcloud.org/?project=$lang.wikipedia.org&platform=all-access&agent=all-agents&redirects=0&start=2015-07-01&end=2025-06-27&pages=$title";

    return "<a class='item' href='$url' target='_blank'>$count</a>";
}
function build_table_from_dataset(array $dataset, string $lang): string
{
    if (empty($dataset)) return "<p>No rows</p>";

    // $columns = get_columns($dataset);
    $columns = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "all"];

    $thead = '<thead><tr><th>#</th><th>title</th>' . implode('', array_map(fn($c) => "<th>$c</th>", $columns)) . '</tr></thead>';
    $tbody = '';

    $i = 1;

    foreach ($dataset as $key => $values) {
        $lang = ($lang == 'be-x-old') ? 'be-tarask' : $lang;
        $row = "<tr><td>$i</td><td><a class='item' href='https://$lang.wikipedia.org/wiki/$key' target='_blank'>$key</a></td>";
        foreach ($columns as $col) {
            $val = $values[$col] ?? 0;
            if ($col === 'all') {
                $val = pageviews_link($lang, $key, $val);
            }
            $row .= "<td>$val</td>";
        }
        $tbody .= $row . '</tr>';
        $i++;
    }
    // ---
    $class_1 = (count($dataset) > 10000) ? "" : "DataTable";
    // ---
    return "<table class='table table-striped table-bordered $class_1'>$thead<tbody>$tbody</tbody></table>";
}

function render_data_new(array $org_data, string $lang, string $main_dir, string $data_type = 'non_zero'): string
{
    $data_types = ['non_zero', 'zero', 'hash'];
    $data_type = in_array($data_type, $data_types) ? $data_type : 'non_zero';

    [$data, $data_with_hash, $non_zero, $zero] = split_data_hash($org_data);

    if ($data_type === 'non_zero') {
        $data_filtered = $non_zero;
        $title = "Non-Zero Data (" . count($data_filtered) . ")";
        // ---
    } elseif ($data_type === 'zero') {
        $data_filtered = $zero;
        $title = "Zero Data Only (" . count($data_filtered) . ")";
        // ---
    } elseif ($data_type === 'hash') {
        $data_filtered = $data_with_hash;
        $title = "Hash Data (" . count($data_filtered) . ")";
    }

    $all_views = array_sum(array_column($data_filtered, 'all'));
    $all_views = number_format($all_views);

    $header = <<<HTML
        <div class="text-center d-flex align-items-center justify-content-between">
            <span class="card-title h2">Language code: $lang</span>
            <span class="h3">All Views: $all_views</span>
            <a class='h2 btn btn-secondary' href='views_new.php'> >> Return</a>
        </div>
        <hr/>
    HTML;
    $table = build_table_from_dataset($data_filtered, $lang);
    $card = build_card_with_table($title, $table);

    return $header . $card;
}

$main_dir = $_GET['main_dir'] ?? 'views_new';
$lang = $_GET['lang'] ?? '';
$data_type = $_GET['data_type'] ?? 'non_zero';

$dir = "$base_path/pybot/md_core/update_med_views/views_new/all";

// if ($lang && !preg_match('/^[a-z]{2,3}(-[a-z0-9]+)*$/i', $lang)) $lang = ''; // Invalid language code

if ($lang) {
    $data = get_data("$dir/$lang.json");
    // ---
    $table = render_data_new($data, $lang, $main_dir, $data_type);
} else {
    $files = glob("$dir/*.json");
    $all_data = json_decode(file_get_contents("$base_path/pybot/md_core/update_med_views/languages_counts.json"), true);
    // ---
    $table = render_data_all_new($base_path, $all_data);
}

?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>All Languages</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <link href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css' rel='stylesheet'>
    <link href='/Translation_Dashboard/css/dashboard_new1.css' rel='stylesheet'>
    <script type="module" src="/Translation_Dashboard/js/c.js"></script>
</head>

<body>
    <div class="container-fluid mt-4">
        <?= $table ?>
    </div>
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js"></script>
    <script>
        $(document).ready(function() {
            $('.DataTable').DataTable({
                paging: false,
                searching: false
            });
            $('#pending').DataTable({
                paging: false,
                searching: false,
                order: [
                    [4, 'desc']
                ]
            });
        });
    </script>
</body>

</html>
