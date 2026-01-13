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

$total_views_by_year = [];
foreach ($years_data as $year => $year_counts) {
    $total_views_by_year[$year] = array_sum($year_counts);
}

// Return JSON for Chart
echo json_encode([
    "labels" => array_keys($total_views_by_year),
    "data" => array_values($total_views_by_year)
], JSON_PRETTY_PRINT);
