<?php

if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

$dir_with_sub = [
    "views_new" => "views_new/all",
    "2021" => "views/2021",
];

$base_path = getenv('HOME') ?: __DIR__ . "/../../../";

$views_dir = "$base_path/pybot/md_core/update_med_views/views";

// add all year folders in $views_dir to $dir_with_sub
$views_dirs = glob("$views_dir/*");

foreach ($views_dirs as $views_dir) {
    $na = basename($views_dir);
    $dir_with_sub[$na] = "views/$na";
};

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

function make_form($main_dir)
{
    global $dir_with_sub;

    $options = array_map(function ($dir) use ($main_dir) {
        $selected = $dir == $main_dir ? 'selected' : '';
        return "<option value='$dir' $selected>$dir</option>";
    }, array_keys($dir_with_sub));

    $options_html = implode("\n", $options);

    $form = <<<HTML
        <form action="" method="get">
            <div class="row">
                <div class="col-9">
                    <div class="input-group">
                        <span class="input-group-text">Folder:</span>
                        <select name="main_dir" class="form-control">
                            $options_html
                        </select>
                    </div>
                </div>
                <div class="col-3">
                    <button type="submit" class="btn btn-primary">Go</button>
                </div>
            </div>
        </form>
    HTML;

    return $form;
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

function build_table_head($y): string
{
    return <<<HTML
        <thead>
            <tr>
                <th style="width: 10%">#</th>
                <th>Lang</th>
                <th>Count</th>
                <th>$y Views</th>
                <th>Ready</th>
                <th>Still</th>
                <th>with_hash</th>
                <th style="width: 10%">Done!</th>
            </tr>
        </thead>
    HTML;
}

function render_data_all(array $files, string $main_dir, array $all_data): string
{
    $rows_done = $rows_pending = '';
    $done_all = $pending_all = $i = 0;
    $count_all = count($files);
    // {'all': 1, 'empty': 0, 'not_empty': 1, 'hash': 0, 'views': {'all': 2554, '2024': 685}}
    // dump_one(/data/project/mdwiki/pybot/md_core/update_med_views/views_new/stats/gag.json), len(data)=5

    $form = make_form($main_dir);
    $all_titles = 0;

    $year = ($main_dir == 'views_new') ? '2024' : 'all';

    foreach ($files as $file) {
        $lang = basename($file, '.json');

        // روابط منفصلة لكل نوع بيانات
        $url_non_0 = "?main_dir=$main_dir&lang=$lang&data_type=non_zero";
        $url_zero  = "?main_dir=$main_dir&lang=$lang&data_type=zero";
        $url_hash  = "?main_dir=$main_dir&lang=$lang&data_type=hash";

        $count = $all_data[$lang] ?? 0;
        $org_data = get_data($file);

        $all_titles += count($org_data);

        [$data, $data_with_hash, $non_zero, $zero] = split_data_hash($org_data);

        // $lang_views = sum all $data ['all'] values
        // $lang_views = array_sum(array_column($data, 'all'));
        $lang_views = array_sum(array_column($data, $year));
        // ---
        $lang_views = number_format($lang_views);
        // ---
        $with_hash = count($data_with_hash);
        $count = $count - $with_hash;
        $count_non_zero = count($non_zero);
        $count_zero = count($zero);
        // ---
        $done = $count == $count_non_zero || $count_zero == 0;
        // ---
        $row = <<<HTML
        <tr>
            <td>$i</td>
            <td>$lang</td>
            <td>$count</td>
            <td>$lang_views</td>
            <td><a class='item' href='$url_non_0'>$count_non_zero</a></td>
            <td><a class='item' href='$url_zero'>$count_zero</a></td>
            <td><a class='item' href='$url_hash'>$with_hash</a></td>
            <td>$done</td>
        </tr>
    HTML;

        if ($done) {
            $rows_done .= $row;
            $done_all++;
        } else {
            $rows_pending .= $row;
            $pending_all++;
        }
        $i++;
    }

    $all_titles = number_format($all_titles);

    $header = <<<HTML
        <div class="text-center d-flex align-items-center justify-content-between">
            <span class="h2">All Languages: $count_all</span>
            <span class="h3">All Titles: $all_titles</span>
            $form
        </div>
        <hr/>
    HTML;

    $thead = build_table_head($year);
    $table_done = "<table class='table table-striped table-bordered DataTable'>$thead<tbody>$rows_done</tbody></table>";
    $table_pending = "<table id='pending' class='table table-striped table-bordered'>$thead<tbody>$rows_pending</tbody></table>";

    $card_done = build_card_with_table("Completed Languages ($done_all)", $table_done, "collapsed-card");
    $card_pending = build_card_with_table("Pending Languages ($pending_all)", $table_pending, "mt-4");

    return $header . $card_done . $card_pending;
}

function get_columns(array $dataset): array
{
    $all_keys = [];
    // ---
    /*
    Fatal error: Maximum execution time of 30 seconds exceeded in /data/project/mdwiki/public_html/views_new.php on line 182

    foreach ($dataset as $item) {
        $all_keys = array_merge($all_keys, array_keys($item));
    }
    $columns = array_unique($all_keys);
    */
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

    $columns = get_columns($dataset);

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
            <a class='h2 btn btn-secondary' href='views_new.php?main_dir=$main_dir'> >> Return</a>
        </div>
        <hr/>
    HTML;
    $table = build_table_from_dataset($data_filtered, $lang);
    $card = build_card_with_table($title, $table);

    return $header . $card;
}


function get_main_dir()
{
    global $dir_with_sub;
    // ---
    $main_dir = $_GET['main_dir'] ?? 'views_new';
    // ---
    $main_dir_with_sub = $dir_with_sub[$main_dir] ?? $main_dir;
    // ---
    return [$main_dir_with_sub, $main_dir];
}
// Main Execution Logic
[$main_dir_with_sub, $main_dir] = get_main_dir();

$lang = $_GET['lang'] ?? '';
$data_type = $_GET['data_type'] ?? 'non_zero';

$dir = "$base_path/pybot/md_core/update_med_views/$main_dir_with_sub";

if ($lang && !preg_match('/^[a-z]{2,3}(-[a-z0-9]+)*$/i', $lang)) {
    $lang = ''; // Invalid language code
}

if ($lang) {
    $data = get_data("$dir/$lang.json");
    // ---
    $table = render_data_new($data, $lang, $main_dir, $data_type);
} else {
    $files = glob("$dir/*.json");
    $all_data = json_decode(file_get_contents("$base_path/pybot/md_core/update_med_views/languages_counts.json"), true);
    // ---
    $table = render_data_all($files, $main_dir, $all_data);
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
