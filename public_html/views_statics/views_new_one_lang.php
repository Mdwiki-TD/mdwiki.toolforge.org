<?php

if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

$dir_with_sub = [
    "views_new" => "views_new/all",
];

require_once __DIR__ . '/helpers.php';

$base_path = __DIR__ . "/update_med_views/";

function build_table_from_dataset(array $dataset, string $lang): string
{
    if (empty($dataset)) return "<p>No rows</p>";

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

$dir = "$base_path/views_new/all";

// if ($lang && !preg_match('/^[a-z]{2,3}(-[a-z0-9]+)*$/i', $lang)) $lang = ''; // Invalid language code

$table = "";
if ($lang) {
    $data = get_data("$dir/$lang.json");
    // ---
    $table = render_data_new($data, $lang, $main_dir, $data_type);
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
