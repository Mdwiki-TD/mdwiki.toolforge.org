<?php
header('Content-Type: application/json');

// Error reporting for testing
if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

// Configuration
$base_path = __DIR__ . "/update_med_views/";
$dir_with_sub = [
    "all-agents" => "views_by_year_all_agents",
    "users-agents" => "views_by_year_users_agents",
];

// Parameters
$sub_dir_selected = $_GET['sub_dir'] ?? 'all-agents';
$sub_dir = $dir_with_sub[$sub_dir_selected] ?? 'views_by_year_all_agents';
$lang = basename($_GET['lang'] ?? '');
$chart_requested = isset($_GET['chart_data']);

if ($lang) {
    handle_lang_request($base_path, $sub_dir, $lang, $chart_requested);
} else {
    handle_global_request($base_path, $sub_dir, $chart_requested);
}

/**
 * Handles requests for language-specific article pageviews.
 */
function handle_lang_request($base_path, $sub_dir, $lang, $chart_requested)
{
    // Load article data from yearly directories
    $years_dirs = glob("$base_path/$sub_dir/*", GLOB_ONLYDIR);
    $years_data = [];
    foreach ($years_dirs as $year_dir) {
        $year = basename($year_dir);
        $file_path = "$year_dir/$lang.json";
        $data = file_exists($file_path) ? json_decode(file_get_contents($file_path), true) : [];
        $years_data[$year] = is_array($data) ? $data : [];
    }
    ksort($years_data);

    // Chart Mode
    if ($chart_requested) {
        $totals = [];
        foreach ($years_data as $year => $data) {
            $totals[$year] = array_sum($data);
        }
        echo json_encode([
            "labels" => array_keys($totals),
            "data" => array_values($totals)
        ], JSON_PRETTY_PRINT);
        return;
    }

    // DataTable Mode: Article summary
    $titles_to_year = [];
    foreach ($years_data as $year => $titles) {
        foreach ($titles as $title => $count) {
            if (!isset($titles_to_year[$title])) $titles_to_year[$title] = [];
            $titles_to_year[$title][$year] = $count;
        }
    }

    // Summary Row Calculation
    $all_titles_count = count($titles_to_year);
    $summary_row = ["index" => "0", "title" => (string)$all_titles_count, "is_summary" => true];
    $all_total_views = 0;
    foreach ($years_data as $year => $data) {
        $y_sum = array_sum($data);
        $all_total_views += $y_sum;
        $summary_row[$year] = $y_sum;
    }
    $summary_row["total"] = $all_total_views;

    // Article Rows
    $all_rows = [];
    $i = 1;
    foreach ($titles_to_year as $title => $counts) {
        $row = ["index" => (string)$i, "title" => $title, "is_summary" => false];
        $total = 0;
        foreach ($years_data as $year => $_) {
            $c = $counts[$year] ?? 0;
            $total += $c;
            $row[$year] = $c;
        }
        $row["total"] = $total;
        $all_rows[] = $row;
        $i++;
    }

    // Server-side pagination and search parameters
    $start = isset($_GET['start']) ? (int)$_GET['start'] : 0;
    $length = isset($_GET['length']) ? (int)$_GET['length'] : 500;
    $search_value = $_GET['search']['value'] ?? '';

    $total_records = count($all_rows);
    $filtered_rows = $all_rows;

    // Apply Server-side search
    if (!empty($search_value)) {
        $filtered_rows = array_filter($all_rows, function($row) use ($search_value) {
            return mb_stripos($row['title'], $search_value) !== false;
        });
    }

    $records_filtered = count($filtered_rows);

    // Slice data for current page from filtered results
    $paged_data = array_slice($filtered_rows, $start, $length);

    // Include summary row ONLY on the first page of NON-SEARCH results
    $final_data = $paged_data;
    if ($start === 0 && empty($search_value)) {
        array_unshift($final_data, $summary_row);
    }

    echo json_encode([
        "draw" => isset($_GET['draw']) ? (int)$_GET['draw'] : 1,
        "recordsTotal" => $total_records + 1,
        "recordsFiltered" => empty($search_value) ? ($total_records + 1) : $records_filtered,
        "data" => $final_data,
        "years" => array_keys($years_data)
    ], JSON_PRETTY_PRINT);
}

/**
 * Handles global requests for all languages summary.
 */
function handle_global_request($base_path, $sub_dir, $chart_requested)
{
    // Load language summary data from yearly JSON files
    $year_files = glob("$base_path/$sub_dir/*.json");
    $years_data = [];
    foreach ($year_files as $file) {
        $year = basename($file, '.json');
        $year = str_replace('_languages_counts', '', $year);
        $data = json_decode(file_get_contents($file), true);
        if (is_array($data)) $years_data[$year] = $data;
    }
    ksort($years_data);

    // Chart Mode
    if ($chart_requested) {
        $totals = [];
        foreach ($years_data as $year => $counts) {
            $totals[$year] = array_sum($counts);
        }
        echo json_encode([
            "labels" => array_keys($totals),
            "data" => array_values($totals)
        ], JSON_PRETTY_PRINT);
        return;
    }

    // DataTable Mode: All languages summary
    $all_data_file = "$base_path/languages_counts.json";
    $all_data = file_exists($all_data_file) ? json_decode(file_get_contents($all_data_file), true) : [];

    $data_rows = [];
    $all_langs_count = count($all_data);
    $all_titles_sum = array_sum($all_data);

    // Summary Row
    $summary_row = ["index" => "0", "lang" => (string)$all_langs_count, "titles" => $all_titles_sum, "is_summary" => true];
    $grand_total = 0;
    foreach ($years_data as $year => $counts) {
        $y_sum = array_sum($counts);
        $grand_total += $y_sum;
        $summary_row[$year] = $y_sum;
    }
    $summary_row["total"] = $grand_total;
    $data_rows[] = $summary_row;

    // Language Rows
    $i = 1;
    foreach ($all_data as $l => $count) {
        $row = ["index" => (string)$i, "lang" => $l, "titles" => $count ?? 0, "is_summary" => false];
        $total = 0;
        foreach ($years_data as $year => $counts) {
            $c = $counts[$l] ?? 0;
            $total += $c;
            $row[$year] = $c;
        }
        $row["total"] = $total;
        $data_rows[] = $row;
        $i++;
    }

    echo json_encode(["data" => $data_rows, "years" => array_keys($years_data)], JSON_PRETTY_PRINT);
}
