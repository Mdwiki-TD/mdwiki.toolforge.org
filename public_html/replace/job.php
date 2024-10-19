<?php
require __DIR__ . '/../header.php';
//---
$test = $_GET['test'] ?? "";
$id  = $_GET['id'] ?? "";
$to  = $_GET['to'] ?? "";
//---
$valid_to = in_array($to, ['stop', 'restart']);
//---
if (!$valid_to || empty($id)) {
    echo "Invalid request";
    exit;
}
//---
$id_folder = $id_dir = __DIR__ . "/find/$id";
//---
if (!is_dir($id_folder)) {
    echo "Invalid id";
    exit;
}
//---
if ($to == 'stop') {
    $stop_file = $id_dir = __DIR__ . "/find/$id/done.txt";
    // ---
    if (!is_file($stop_file)) {
        $myfile = fopen($stop_file, 'w');
        fwrite($myfile, "stop");
        fclose($myfile);
    };
    // ---
    echo "The job will be stopped in seconds.";
    exit;
} elseif ($to == 'restart') {
    $done_file = $id_dir = __DIR__ . "/find/$id/done.txt";
    // ---
    if (is_file($done_file)) {
        unlink($done_file);
    }
    echo "The job will be restarted in seconds.";
    exit;
}
// ---
require __DIR__ . '/../footer.php';
//---
