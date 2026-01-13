<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>All Languages</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <link href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css' rel='stylesheet'>
    <link href='/Translation_Dashboard/css/dashboard_new1.css' rel='stylesheet'>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script type="module" src="/Translation_Dashboard/js/c.js"></script>
</head>

<?php

if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}
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

    return $table_done;
    // ---
}

$dir_with_sub = [
    "all-agens" => "views_by_year_all_agens",
    "users-agents" => "views_by_year_users_agents",
];

$type_titles = [
    "all-agens" => "All Agents",
    "users-agents" => "Users Agents",
];

$sub_dir_selected = $_GET['sub_dir'] ?? 'all-agens';


$sub_dir = $dir_with_sub[$sub_dir_selected] ?? 'views_by_year_all_agens';

$lang = $_GET['lang'] ?? '';
if (!$lang) {
    header("Location: index.php?sub_dir=$sub_dir_selected");
    exit;
}

$years_dirs = glob("$base_path/$sub_dir/*");
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
$table_done = render_data_all_new($lang, $years_data);

$type_title = $type_titles[$sub_dir_selected] ?? "All Agents";
// write form to select $type_title
$type_title_form = <<<HTML
    <form method="get" action="views_new_one_lang.php">
        <input type="hidden" name="lang" value="$lang"/>
        <select name="sub_dir" onchange="this.form.submit()">
HTML;
foreach ($type_titles as $type => $title) {
    $selected = ($type === $sub_dir_selected) ? 'selected' : '';
    $type_title_form .= "<option value=\"$type\" $selected>$title</option>";
}
$type_title_form .= <<<HTML
        </select>
    </form>
HTML;

$header = <<<HTML
    <div class="text-center d-flex align-items-center justify-content-between">
        <span>
            $type_title_form
        </span>
        <span class="h3">WikiProject Medicine Pageviews (lang: $lang)</span>
        <a class='h2 btn btn-secondary' href='index.php'> >> Return</a>
    </div>
    <hr/>
HTML;
$chart_card = build_card_with_table("Total Views by Year", "<canvas id='viewsChart' height='60'></canvas>", "");
$card_done = build_card_with_table("Views data", $table_done, "collapsed-card1");
$table = $header . $chart_card . $card_done;

$total_views_by_year = render_total_by_year($years_data);

$labels = json_encode(array_keys($total_views_by_year));
$data_values = json_encode(array_values($total_views_by_year));

$chart_script = make_chart_script($labels, $data_values);

?>

<body>
    <div class="container-fluid mt-4">
        <?= $table ?>
    </div>
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js"></script>
    <?= $chart_script ?>
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
