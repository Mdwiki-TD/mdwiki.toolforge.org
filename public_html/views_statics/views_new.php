<?php

if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}
require_once __DIR__ . '/helpers.php';

$dir_with_sub = [
    "views_new" => "views_new/all",
];

$base_path = __DIR__ . "/update_med_views/";

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

    $stats = json_decode(file_get_contents("$base_path/views_new/stats.json"), true);

    $count_all = count($stats);

    $i = 1;

    foreach ($stats as $lang => $org_data) {

        $all_titles += $org_data['not_empty'] ?? 0;
        $url_non_0 = "views_new_one_lang.php?lang=$lang&data_type=non_zero";

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

$main_dir = $_GET['main_dir'] ?? 'views_new';
$lang = $_GET['lang'] ?? '';
$data_type = $_GET['data_type'] ?? 'non_zero';

$dir = "$base_path/views_new/all";

$files = glob("$dir/*.json");
$all_data = json_decode(file_get_contents("$base_path/languages_counts.json"), true);
// ---
$table = render_data_all_new($base_path, $all_data);


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
