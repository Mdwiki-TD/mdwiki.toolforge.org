<?php

if (isset($_REQUEST['test'])) {
    $print_t = true;
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}
header('Content-Type: application/json');
include_once __DIR__ . '/sql.php';

use function API\SQL\fetch_query;

$get = $_GET['get'];

function  add_li($qua, $types)
{
    foreach ($types as $type) {
        if (isset($_GET[$type])) {
            // filter input
            $added = filter_input(INPUT_GET, $type, FILTER_SANITIZE_SPECIAL_CHARS);
            $where_or_and = (strpos($qua, 'WHERE') !== false) ? ' AND ' : ' WHERE ';
            $qua .= " $where_or_and $type = '$added' ";
        }
    }
    return $qua;
}

switch ($get) {
    case 'users':
        $qua = "SELECT username FROM users";
        if (isset($_GET['userlike'])) {
            $added = filter_input(INPUT_GET, 'userlike', FILTER_SANITIZE_SPECIAL_CHARS);
            $qua .= " WHERE username like '$added%'";
        }
        $results = fetch_query($qua);
        // $results = array_map(function ($row) { return $row['username']; }, $results);
        break;

    case 'full_translators':
        $qua = "SELECT * FROM full_translators";
        $results = fetch_query($qua);
        $results = array_map(function ($row) { return $row['user']; }, $results);
        break;

    case 'views':
        $qua = "SELECT * FROM views ";
        $qua = add_li($qua, ['lang']);

        $results = fetch_query($qua);
        break;

    case 'words':
        // {"w_id":1,"w_title":"Second-degree atrioventricular block","w_lead_words":278,"w_all_words":1267}
        $qua = "SELECT * FROM words";
        $results = fetch_query($qua);
        break;


    case 'qids':
        // {"id":18638,"title":"11p deletion syndrome","qid":"Q1892153"}
        $qua = "SELECT * FROM qids";
        $results = fetch_query($qua);
        break;


    default:
        if (in_array($get, ['pages', 'pages_users'])) {
            $qua = "SELECT * FROM $get";

            $qua = add_li($qua, ['lang', 'user', 'translate_type', 'cat', 'title']);

            $results = fetch_query($qua);
            break;
        }
        $results = ["error" => "invalid get request"];
        break;
}

$out = [
    "results" => $results,
    "query" => $qua
];

echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
