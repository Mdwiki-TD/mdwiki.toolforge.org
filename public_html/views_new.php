<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>All JSON Files</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <link href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css' rel='stylesheet' type='text/css'>
    <link href='/Translation_Dashboard/css/dashboard_new1.css' rel='stylesheet' type='text/css'>
    <script type="module" src="/Translation_Dashboard/js/c.js"></script>
</head>

<?php

echo "<body>";
function build_card_with_table(string $title, string $table_html, string $extra_classes = ''): string
{
    return <<<HTML
        <div class="card $extra_classes">
            <div class="card-header">
                <span class="card-title h2">$title</span>
                <div class="card-tools">
                    <button type="button" class="btn-tool" data-card-widget="collapse">
                        <i class="fas fa-minus"></i>
                    </button>
                </div>
            </div>
            <div class="card-body">
                $table_html
            </div>
        </div>
    HTML;
}

function render_data_all($files, $main_dir, $all_data)
{
    $done_all = 0;
    $pending_all = 0;
    $i = 1;
    $rows_done = '';
    $rows_pending = '';

    foreach ($files as $file) {
        $basename = basename($file);
        $lang_n = str_replace('.json', '', $basename);
        $exploreUrl = "?main_dir=$main_dir&lang=$lang_n";
        $count = $all_data[$lang_n] ?? 0;

        $ready_data = json_decode(file_get_contents($file), true);
        $ready = count(array_filter($ready_data, fn($value) => $value['all'] != 0));
        $done = $count == $ready;
        $still = $count - $ready;

        $row = <<<HTML
            <tr>
                <td>$i</td>
                <td><a class='item' href='$exploreUrl'>$lang_n</a></td>
                <td>$count</td>
                <td>$ready</td>
                <td>$still</td>
                <td>$done</td>
            </tr>
        HTML;

        if ($done) {
            $done_all++;
            $rows_done .= $row;
        } else {
            $pending_all++;
            $rows_pending .= $row;
        }

        $i++;
    }

    $table_thead = <<<HTML
        <thead>
            <tr>
                <th style="width: 10%">#</th>
                <th>Lang</th>
                <th>Count</th>
                <th>Ready</th>
                <th>Still</th>
                <th style="width: 10%">Done!</th>
            </tr>
        </thead>
    HTML;
    // ---
    $table_done = <<<HTML
        <table class="table table-striped table-bordered">
            $table_thead
            <tbody>
                $rows_done
            </tbody>
        </table>
    HTML;

    $table_pending = <<<HTML
        <table class="table table-striped table-bordered">
            $table_thead
            <tbody>
                $rows_pending
            </tbody>
        </table>
    HTML;

    // إنشاء الكاردات باستخدام الدالة الموحدة
    $card_done = build_card_with_table("Completed Languages ($done_all)", $table_done);
    $card_pending = build_card_with_table("Pending Languages ($pending_all)", $table_pending, "mt-4");

    return $card_done . $card_pending;
}


function build_table_from_dataset(array $dataset, string $lang): string
{
    if (empty($dataset)) {
        return "<p>No rows</p>";
    }

    // استخراج جميع الأعمدة المستخدمة
    $all_keys = [];
    foreach ($dataset as $item) {
        $all_keys = array_merge($all_keys, array_keys($item));
    }

    $columns = array_unique($all_keys);
    sort($columns);

    $output = '<table class="table table-striped table-bordered">';
    $output .= "<thead><tr><th>#</th><th>title</th>";
    foreach ($columns as $col) {
        $output .= "<th>$col</th>";
    }
    $output .= "</tr></thead><tbody>";

    $i = 1;
    foreach ($dataset as $key => $values) {
        $row = <<<HTML
            <tr>
                <td>$i</td>
                <td><a class='item' href='https://$lang.wikipedia.org/wiki/$key' target='_blank'>$key</a></td>
        HTML;

        foreach ($columns as $col) {
            $val = isset($values[$col]) ? $values[$col] : '';
            if ($col === "all") {
                $url = "https://pageviews.wmcloud.org/?project=$lang.wikipedia.org&platform=all-access&agent=all-agents&redirects=0&start=2015-07-01&end=2024-12-31&pages=$key";
                $val = "<a class='item' href='$url' target='_blank'>$val</a>";
            }
            $row .= "<td>$val</td>";
        }

        $row .= "</tr>";
        $output .= $row;
        $i++;
    }

    $output .= "</tbody></table>";
    return $output;
}

function render_data_new($data, $lang, $main_dir)
{
    if (empty($data)) {
        return "<p>No data</p>";
    }

    // فصل البيانات
    $data_not_0 = array_filter($data, fn($value) => $value['all'] != 0);
    $data_with_0 = array_filter($data, fn($value) => $value['all'] == 0);

    // إنشاء الجداول
    $table_not_0 = build_table_from_dataset($data_not_0, $lang);
    $table_with_0 = build_table_from_dataset($data_with_0, $lang);

    // عدد الصفوف في كل جدول
    $count_not_0 = count($data_not_0);
    $count_with_0 = count($data_with_0);

    $return_header = <<<HTML
        <div class="text-center d-flex align-items-center justify-content-between">
            <a class='h2 btn btn-secondary' href='views_new.php?main_dir=$main_dir'>Return</a>
            <span class="card-title h2">JSON File: $lang</span>
            <span class=""></span>
        </div>
    HTML;

    $card_not_0 = $return_header;
    $card_not_0 .= build_card_with_table("Non-Zero Data ($count_not_0)", $table_not_0);

    $card_with_0 = build_card_with_table("Zero Data Only ($count_with_0)", $table_with_0, "mt-4");

    return $card_not_0 . $card_with_0;
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
    $table = render_data_new($data, $lang, $main_dir);
} else {
    // ---
    $all_data = json_decode(file_get_contents("$f_dir/pybot/md_core/update_med_views/languages_counts.json"), true);
    // ---
    $table = render_data_all($files, $main_dir, $all_data);
}
echo <<<HTML
    <div class="container-fluid mt-4">
        $table
    </div>
HTML;
?>

<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js"></script>
<script>
    $(document).ready(function() {
        $('.table').DataTable({
            paging: false,
            searching: false
        });
    });
</script>
</body>

</html>
