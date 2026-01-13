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

// Load yearly data
$year_files = glob("$base_path/$sub_dir/*.json");
$years_data = [];

foreach ($year_files as $file) {
    $year = basename($file, '.json');
    $year = str_replace('_languages_counts', '', $year);
    $data = json_decode(file_get_contents($file), true);
    if (is_array($data)) {
        $years_data[$year] = $data;
    }
}

// Sort years ascending
ksort($years_data);

$get_chart_data = $_GET['chart_data'] ?? null;

$total_views_by_year = [];
foreach ($years_data as $year => $year_counts) {
    $total_views_by_year[$year] = array_sum($year_counts);
}

// Return JSON for Chart
if ($get_chart_data) {
    echo json_encode([
        "labels" => array_keys($total_views_by_year),
        "data" => array_values($total_views_by_year)
    ], JSON_PRETTY_PRINT);
    exit;
}

// Load main language counts
$all_data_file = "$base_path/languages_counts.json";
$all_data = [];
if (file_exists($all_data_file)) {
    $all_data = json_decode(file_get_contents($all_data_file), true);
}

$data_rows = [];

// 1. Summary/Total row
$all_langs = count($all_data);
$all_titles = 0;
foreach ($all_data as $count) {
    $all_titles += $count ?? 0;
}

$summary_row = [
    "index" => "0",
    "lang" => (string)$all_langs,
    "titles" => $all_titles,
    "is_summary" => true
];

$all_total_views = 0;
foreach ($years_data as $year => $year_counts) {
    $y_sum = array_sum($year_counts);
    $all_total_views += $y_sum;
    $summary_row[$year] = $y_sum;
}
$summary_row["total"] = $all_total_views;

$data_rows[] = $summary_row;

// 2. Individual language rows
$i = 1;
foreach ($all_data as $lang => $count) {
    $row = [
        "index" => (string)$i,
        "lang" => $lang,
        "titles" => $count ?? 0,
        "is_summary" => false
    ];

    $lang_total = 0;
    foreach ($years_data as $year => $year_counts) {
        $y_count = $year_counts[$lang] ?? 0;
        $row[$year] = $y_count;
        $lang_total += $y_count;
    }
    $row["total"] = $lang_total;
    $data_rows[] = $row;
    $i++;
}

// Return JSON for DataTables
echo json_encode([
    "data" => $data_rows,
    "years" => array_keys($years_data),
], JSON_PRETTY_PRINT);
