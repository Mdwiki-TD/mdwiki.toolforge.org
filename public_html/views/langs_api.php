<?php
header('Content-Type: application/json');

// Error reporting for testing
if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

// Set base path for data files
$base_path = __DIR__ . "/update_med_views/";

// Directory mapping based on sub_dir parameter
$dir_with_sub = [
    "all-agens" => "views_by_year_all_agens",
    "users-agents" => "views_by_year_users_agents",
];

// Determine selected sub_dir
$sub_dir_selected = $_GET['sub_dir'] ?? 'all-agens';
$sub_dir = $dir_with_sub[$sub_dir_selected] ?? 'views_by_year_all_agens';
$lang = $_GET['lang'] ?? '';

if (!$lang) {
    echo json_encode(["error" => "No language specified"]);
    exit;
}

$chart_data_requested = isset($_GET['chart_data']);

// Load data from yearly directories
$years_dirs = glob("$base_path/$sub_dir/*", GLOB_ONLYDIR);
$years_data = [];

foreach ($years_dirs as $year_dir) {
    $year = basename($year_dir);
    $file_path = "$year_dir/$lang.json";

    if (file_exists($file_path)) {
        $contents = file_get_contents($file_path);
        $data = json_decode($contents, true) ?? [];
        $years_data[$year] = $data;
    } else {
        $years_data[$year] = [];
    }
}

// Sort years ascending
ksort($years_data);

// --- Process for Chart ---
$total_views_by_year = [];
foreach ($years_data as $year => $data) {
    $total_views_by_year[$year] = array_sum($data);
}

if ($chart_data_requested) {
    echo json_encode([
        "labels" => array_keys($total_views_by_year),
        "data" => array_values($total_views_by_year)
    ], JSON_PRETTY_PRINT);
    exit;
}

// --- Process for DataTable ---

// 1. Group by title
$titles_to_year = [];
foreach ($years_data as $year => $titles) {
    foreach ($titles as $title => $count) {
        if (!isset($titles_to_year[$title])) {
            $titles_to_year[$title] = [];
        }
        $titles_to_year[$title][$year] = $count;
    }
}

$data_rows = [];
$all_titles_count = count($titles_to_year);

// 2. Summary/Total row
$summary_row = [
    "0",
    "<strong>" . number_format($all_titles_count) . "</strong>"
];

$all_total_views = 0;
foreach ($years_data as $year => $data) {
    $y_sum = array_sum($data);
    $all_total_views += $y_sum;
    $summary_row[] = "<strong>" . number_format($y_sum) . "</strong>";
}
$summary_row[] = "<strong>" . number_format($all_total_views) . "</strong>";
$data_rows[] = $summary_row;

// 3. Individual Article rows
$i = 1;
// Helper for pageviews link
function make_pv_link($lang, $title, $count, $year)
{
    $project_lang = ($lang == 'be-x-old') ? 'be-tarask' : $lang;
    $formatted_count = number_format($count);
    return "<a class='item' href='https://pageviews.wmcloud.org/pageviews/?project=$project_lang.wikipedia.org&platform=all-access&agent=all-agents&redirects=0&start=$year-01&end=$year-12&pages=$title' target='_blank'>$formatted_count</a>";
}

foreach ($titles_to_year as $title => $counts_by_year) {
    $article_url = "<a class='item' href='https://$lang.wikipedia.org/wiki/" . urlencode($title) . "' target='_blank'>$title</a>";
    $row = [
        (string)$i,
        $article_url
    ];

    $row_total = 0;
    foreach ($years_data as $year => $_) {
        $c = $counts_by_year[$year] ?? 0;
        $row_total += $c;
        $row[] = make_pv_link($lang, $title, $c, $year);
    }
    $row[] = number_format($row_total);
    $data_rows[] = $row;
    $i++;
}

echo json_encode([
    "data" => $data_rows,
    "years" => array_keys($years_data)
], JSON_PRETTY_PRINT);
