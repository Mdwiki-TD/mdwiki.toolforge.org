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
                <th>Title</th>
                $years_ths
                <th>Total</th>
            </tr>
        </thead>
    HTML;
}

function pageviews_link(string $lang, string $title, $y_count, $year): string
{
    $lang = ($lang == 'be-x-old') ? 'be-tarask' : $lang;
    // <!-- https://pageviews.wmcloud.org/pageviews/?project=oc.wikipedia.org&platform=all-access&agent=all-agents&redirects=0&start=2025-01&end=2025-12&pages=Arsenic -->

    $year_link = <<<HTML
        <a class='item' href='https://pageviews.wmcloud.org/pageviews/?project=$lang.wikipedia.org&platform=all-access&agent=all-agents&redirects=0&start=$year-01&end=$year-12&pages=$title' target='_blank'>$y_count</a>
    HTML;
    return $year_link;
}


function render_data_all_new($lang, $years_data): string
{
    $rows_done = '';
    $done_all = 0;

    $titles_to_year = [];
    foreach ($years_data as $year => $titles) {
        foreach ($titles as $title => $count) {
            if (!isset($titles_to_year[$title])) {
                $titles_to_year[$title] = [];
            }
            $titles_to_year[$title][$year] = $count;
        }
    }

    $all_titles = count($titles_to_year);

    $i = 1;
    foreach ($titles_to_year as $title => $years) {
        $articleUrl = "<a class='item' href='https://$lang.wikipedia.org/wiki/$title' target='_blank'>$title</a>";
        // ---
        $row = <<<HTML
            <tr>
                <th>$i</th>
                <td>$articleUrl</td>
        HTML;
        // ---
        $lang_total = 0;
        // ---
        // foreach ($years as $year => $y_count) {
        foreach ($years_data as $year => $_) {
            $y_count = $years[$year] ?? 0;

            $lang_total += $y_count;
            $y_count = number_format($y_count);
            // <!-- https://pageviews.wmcloud.org/pageviews/?project=oc.wikipedia.org&platform=all-access&agent=all-agents&redirects=0&start=2025-01&end=2025-12&pages=Arsenic -->

            $year_link = pageviews_link($lang, $title, $y_count, $year);

            $row .= "<td>$year_link</td>";
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
            <span></span>
            <span class="h3">WikiProject Medicine Pageviews (lang: $lang)</span>
            <a class='h2 btn btn-secondary' href='index.php'> >> Return</a>
        </div>
        <hr/>
    HTML;
    $row_total = <<<HTML
        <tr class="table-primary">
            <td style="width: 5%">0</td>
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

$table = "";
if ($lang) {
    $years_dirs = glob("$base_path/views_by_year/*");
    $years_data = [];

    foreach ($years_dirs as $year_dir) {
        if (!is_dir($year_dir)) continue;
        $year = basename($year_dir);
        $file_path = "$year_dir/$lang.json";

        $contents = $file_path && file_exists($file_path)
            ? file_get_contents($file_path)
            : '{}';

        $years_data[$year] = json_decode($contents, true) ?? [];
    }
    // ---
    $table = render_data_all_new($lang, $years_data);
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
                searching: false,
                order: [
                    [0, 'asc']
                ]
            });
        });
    </script>
</body>

</html>
