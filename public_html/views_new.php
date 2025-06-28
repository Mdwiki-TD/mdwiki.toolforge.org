<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>All JSON Files</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css" rel="stylesheet">
</head>

<?php
echo "<body>";

function render_data_all($files, $main_dir, $all_data)
{
    $output = '<table id="jsonTable" class="table table-striped table-bordered">';
    $done_all = 0;
    $i = 1;
    $output .= <<<HTML
        <thead>
            <tr>
                <th style="width: 10%">#</th>
                <th >Lang</th>
                <th>Count</th>
                <th>Ready</th>
                <th>Still</th>
                <th style="width: 10%">Done!</th>
            </tr>
        </thead>
        <tbody>
    HTML;
    foreach ($files as $file) {
        $basename = basename($file);
        // ---
        $lang_n = str_replace('.json', '', $basename);
        // ---
        $exploreUrl = "?main_dir=$main_dir&lang=$lang_n";
        // ---
        $count = $all_data[$lang_n] ?? 0;
        // ---
        $ready_data = json_decode(file_get_contents($file), true);
        // count keys in $ready_data with value['all'] != 0
        $ready = count(array_filter($ready_data, function ($value) {
            return $value['all'] != 0;
        }));
        // ---
        $done = $count == $ready;
        // ---
        if ($done) {
            $done_all++;
        };
        // ---
        $still = $count - $ready;
        // ---
        $output .= <<<HTML
            <tr>
                <td>$i</td>
                <td><a class='item' href='$exploreUrl'>$lang_n</a></td>
                <td>$count</td>
                <td>$ready</td>
                <td>$still</td>
                <td>$done</td>
            </tr>
        HTML;
        // ---
        $i++;
    }
    // ---
    $output .= '</tbody></table>';
    // ---
    return <<<HTML
        <div class="container mt-4">
            <h2 class="mb-4">
                All JSON Files, langs done: $done_all
            </h2>
            $output
        </div>
    HTML;
}

function render_data_new($data, $lang, $main_dir)
{
    if (empty($data)) {
        return "<p>No data</p>";
    }
    $output = '<table id="jsonTable" class="table table-striped table-bordered">';
    // جمع كل المفاتيح الفرعية من جميع العناصر
    $all_keys = [];
    foreach ($data as $item) {
        $all_keys = array_merge($all_keys, array_keys($item));
    }
    // إزالة المكرر وترتيب المفاتيح
    $columns = array_unique($all_keys);
    sort($columns); // إذا أردت ترتيبها تصاعديًا

    // طباعة رأس الجدول
    $output .= "<thead><tr><th>#</th><th>title</th>";
    foreach ($columns as $col) {
        $output .= "<th>$col</th>";
    }
    $output .= "</tr></thead><tbody>";

    // طباعة الصفوف
    $i = 1;

    $data = array_filter($data, function ($value) {
        return $value['all'] != 0;
    });

    foreach ($data as $key => $values) {
        $row = <<<HTML
            <tr>
                <td>$i</td>
                <td>
                    <a class='item' href='https://$lang.wikipedia.org/wiki/$key' target='_blank'>$key</a>
                </td>
        HTML;
        // ---
        foreach ($columns as $col) {
            $val = isset($values[$col]) ? $values[$col] : '';
            // ---
            if ($col == "all") {
                $url = "https://pageviews.wmcloud.org/?project=$lang.wikipedia.org&platform=all-access&agent=all-agents&redirects=0&start=2015-07-01&end=2024-12-31&pages=$key";
                $val = "<a class='item' href='$url' target='_blank'>$val</a>";
            }
            // ---
            $row .= "<td>$val</td>";
        }
        $row .= "</tr>";
        $output .= $row;
        $i++;
    }
    // ---
    $output .= '</tbody></table>';
    // ---
    return <<<HTML
        <div class="container mt-4">
            <h2 class="mb-4">
                <a class='btn btn-secondary' href='views_new.php?main_dir=$main_dir'> return All Files</a>
                JSON File: $lang
            </h2>
            $output
        </div>
    HTML;
}

$main_dir = (!empty($_GET['main_dir'])) ? $_GET['main_dir'] : "views_new";

// Get language from query or default to 'en'
$lang = $_GET['lang'] ?? "";

$f_dir = __DIR__ . "/../../";

if (!empty(getenv('HOME'))) {
    $f_dir = getenv('HOME');
}

$dir = "$f_dir/pybot/md_core/update_med_views/$main_dir";

$files = glob($dir . '/all/*.json');

$done_all = 0;

$title = "";

$title2 = "";

if (!empty($lang)) {
    $data = json_decode(file_get_contents("$dir/all/$lang.json") ?? "", true) ?? [];
    // ---
    echo render_data_new($data, $lang, $main_dir);
} else {
    // ---
    $all_data = json_decode(file_get_contents("$f_dir/pybot/md_core/update_med_views/languages_counts.json"), true);
    // ---
    echo render_data_all($files, $main_dir, $all_data);
}

?>

<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js"></script>
<script>
    $(document).ready(function() {
        $('#jsonTable').DataTable({
            paging: false,
            searching: false
        });
    });
</script>
</body>

</html>
