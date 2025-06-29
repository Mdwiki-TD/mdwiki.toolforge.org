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

$base_path = getenv('HOME') ?: __DIR__ . "/../../";

$views_dir = "$base_path/pybot/md_core/update_med_views/views";

// add all year folders in $views_dir to $dir_with_sub
$views_dirs = glob("$views_dir/*");

foreach ($views_dirs as $views_dir) {
    $na = basename($views_dir);
    $dir_with_sub[$na] = "views/$na";
};

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

function build_table_head(): string
{
    return <<<HTML
        <thead>
            <tr>
                <th style="width: 10%">#</th>
                <th>Lang</th>
                <th>Count</th>
                <th>Ready</th>
                <th>Still</th>
                <th style="width: 10%">Done!</th>
            </tr>
        </thead>
    HTML;
}

function render_data_all(array $files, string $main_dir, array $all_data): string
{
    $rows_done = $rows_pending = '';
    $done_all = $pending_all = $i = 0;
    $count = count($files);

    $form = make_form($main_dir);

    $header = <<<HTML
        <div class="text-center d-flex align-items-center justify-content-between">
            <span class="h2">ALL JSON Files: $count</span>
            <span></span>
            $form
        </div>
        <hr/>
    HTML;

    foreach ($files as $file) {
        $lang = basename($file, '.json');
        $url = "?main_dir=$main_dir&lang=$lang";
        $count = $all_data[$lang] ?? 0;
        $data = get_data($file);
        $ready = count(data_not_zero($data));
        $done = $count == $ready;
        $still = $count - $ready;

        $row = <<<HTML
            <tr>
                <td>$i</td>
                <td><a class='item' href='$url'>$lang</a></td>
                <td>$count</td>
                <td>$ready</td>
                <td>$still</td>
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

    $thead = build_table_head();
    $table_done = "<table class='table table-striped table-bordered'>$thead<tbody>$rows_done</tbody></table>";
    $table_pending = "<table class='table table-striped table-bordered'>$thead<tbody>$rows_pending</tbody></table>";

    $card_done = build_card_with_table("Completed Languages ($done_all)", $table_done, "collapsed-card");
    $card_pending = build_card_with_table("Pending Languages ($pending_all)", $table_pending, "mt-4");

    return $header . $card_done . $card_pending;
}

function get_columns(array $dataset): array
{
    $all_keys = [];
    foreach ($dataset as $item) {
        $all_keys = array_merge($all_keys, array_keys($item));
    }
    $columns = array_unique($all_keys);
    sort($columns);
    return $columns;
}
function pageviews_link(string $lang, string $title, int $count): string
{
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
    return "<table class='table table-striped table-bordered'>$thead<tbody>$tbody</tbody></table>";
}

function render_data_new(array $data, string $lang, string $main_dir): string
{
    // if (!$data || empty($data)) return "<p>No data</p>";

    $header = <<<HTML
        <div class="text-center d-flex align-items-center justify-content-between">
            <span class="card-title h2">JSON File: $lang</span>
            <span></span>
            <a class='h2 btn btn-secondary' href='views_new.php?main_dir=$main_dir'> >> Return</a>
        </div>
        <hr/>
    HTML;

    $data_not_0 = data_not_zero($data);
    $table1 = build_table_from_dataset($data_not_0, $lang);
    $count1 = count($data_not_0);
    $card1 = build_card_with_table("Non-Zero Data ($count1)", $table1, "collapsed-card");

    $data_with_0 = array_diff_key($data, $data_not_0);
    $table2 = build_table_from_dataset($data_with_0, $lang);
    $count2 = count($data_with_0);

    $card2 = build_card_with_table("Zero Data Only ($count2)", $table2, "mt-4");

    return $header . $card1 . $card2;
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

$dir = "$base_path/pybot/md_core/update_med_views/$main_dir_with_sub";

if ($lang && !preg_match('/^[a-z]{2,3}(-[a-z]+)?$/i', $lang)) {
    $lang = ''; // Invalid language code
}

if ($lang) {
    $data = get_data("$dir/$lang.json");
    // ---
    $table = render_data_new($data, $lang, $main_dir);
} else {
    $files = glob("$dir/*.json");
    $all_data = json_decode(file_get_contents("$base_path/pybot/md_core/update_med_views/languages_counts.json"), true);
    $table = render_data_all($files, $main_dir, $all_data);
}

?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>All JSON Files</title>
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
            $('.table').DataTable({
                paging: false,
                searching: false
            });
        });
    </script>
</body>

</html>
