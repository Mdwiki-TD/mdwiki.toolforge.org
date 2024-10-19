<?php
require __DIR__ . '/../header.php';

$test = isset($_GET['test']) ? htmlspecialchars($_GET['test']) : '';
$id = isset($_GET['id']) ? filter_var($_GET['id']) : '';
$to = isset($_GET['to']) ? filter_var($_GET['to']) : '';

$valid_to = in_array($to, ['stop', 'restart']);

if (!$valid_to || empty($id) || !ctype_alnum($id)) {
    echo "Invalid request";
    exit;
}
//---
// $id_folder = __DIR__ . "/find/$id";
$id_folder = __DIR__ . "/find/" . basename($id);
//---
if (!is_dir($id_folder) || !ctype_alnum(basename($id))) {
    echo "Invalid id";
    exit;
}
//---
if ($to == 'stop') {
    $stop_file = $id_folder . "/done.txt";

    $fp = fopen($stop_file, 'w');
    if (flock($fp, LOCK_EX)) {
        fwrite($fp, "stop");
        flock($fp, LOCK_UN);
    }
    fclose($fp);

    echo "The job will be stopped in seconds.";
    exit;
} elseif ($to == 'restart') {
    $done_file = $id_folder . "/done.txt";
    // ---
    if (file_exists($done_file)) {
        if (!unlink($done_file)) {
            echo "Failed to restart the job. Please try again.";
            exit;
        }
    }

    echo "The job will be restarted in seconds.";
    exit;
}
// ---
require __DIR__ . '/../footer.php';
//---
