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

function build_table_head($years_data): string
{
    $years_ths = '';
    foreach ($years_data as $year => $data) {
        $years_ths .= "<th>$year</th>";
    }
    return <<<HTML
        <thead>
            <tr>
                <th style="width: 10%">#</th>
                <th>Lang</th>
                <th>Titles</th>
                $years_ths
                <th>Total</th>
            </tr>
        </thead>
    HTML;
}


function render_data_all_new(array $all_data, $years_data): string
{
    $rows_done = '';
    $done_all = 0;

    $all_titles = 0;

    $all_langs = count($all_data);

    $i = 1;

    foreach ($all_data as $lang => $count) {

        $all_titles += $count ?? 0;
        $url_non_0 = "views_new_one_lang.php?lang=$lang&data_type=non_zero";
        // ---
        $row = <<<HTML
            <tr>
                <td>$i</td>
                <td>$lang</td>
                <td><a class='item' href='$url_non_0'>$count</a></td>
        HTML;
        // ---
        $lang_total = 0;
        // ---
        foreach ($years_data as $year => $data) {
            $y_count = $data[$lang] ?? 0;
            $y_count = number_format($y_count);
            $row .= "<td>$y_count</td>";
            $lang_total += $data[$lang] ?? 0;
        }
        // ---
        $lang_total = number_format($lang_total);
        $row .= "<td>$lang_total</td>";
        $row .= "</tr>";
        // ---
        $rows_done .= $row;
        $done_all++;
        $i++;
    }

    $all_titles = number_format($all_titles);

    $header = <<<HTML
        <div class="text-center d-flex align-items-center justify-content-between">
            <span class="h2">All Languages: $all_langs</span>
            <span class="h3">All Titles: $all_titles</span>
            <span></span>
        </div>
        <hr/>
    HTML;

    $row_total = <<<HTML
        <tr class="table-primary">
            <td><strong>0</strong></td>
            <td><strong>$all_langs</strong></td>
            <td><strong>$all_titles</strong></td>
    HTML;
    $all_total = 0;
    foreach ($years_data as $year => $data) {
        // sum all data values for this year
        $y_count =  0;
        foreach ($data as $lang => $count) {
            $y_count += $count;
        }
        $all_total += $y_count;
        $y_count = number_format($y_count);
        $row_total .= "<td><strong>$y_count</strong></td>";
    }
    $all_total = number_format($all_total);
    $row_total .= <<<HTML
            <td><strong>$all_total</strong></td>
        </tr>
    HTML;
    $thead = build_table_head($years_data);

    $table_done = <<<HTML
        <table class='table table-striped table-bordered table-sm DataTable'>
            $thead
            <tbody>
                $row_total
                $rows_done
            </tbody>
        </table>
    HTML;

    $card_done = build_card_with_table("", $table_done, "collapsed-card1");

    return $header . $card_done;
    // ---
}

$main_dir = $_GET['main_dir'] ?? 'views_new';
$lang = $_GET['lang'] ?? '';
$data_type = $_GET['data_type'] ?? 'non_zero';

$years = glob("$base_path/views_by_year/*.json");
$years_data = [];

foreach ($years as $year_file) {
    $year = basename($year_file, '.json');
    $year = str_replace('_languages_counts', '', $year);
    $years_data[$year] = json_decode(file_get_contents($year_file), true);
}
// sort years_data by year ascending
ksort($years_data);

$all_data = json_decode(file_get_contents("$base_path/languages_counts.json"), true);
// ---
$table = render_data_all_new($all_data, $years_data);


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
