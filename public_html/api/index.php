<?php

if (isset($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}
header('Content-Type: application/json');
include_once __DIR__ . '/sql.php';
include_once __DIR__ . '/lang_pairs.php';

use function API\Langs\get_lang_names;
use function API\SQL\fetch_query;

function sanitize_input($input, $pattern)
{
    if (!empty($input) && preg_match($pattern, $input) && $input !== "all") {
        return filter_var($input, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
    }
    return null;
}

function make_status_query()
{
    // https://mdwiki.toolforge.org/api.php?get=status&year=2022&user_group=Wiki&campaign=Main

    $query = <<<SQL
        SELECT LEFT(p.pupdate, 7) as date, COUNT(*) as count
        FROM pages p
        WHERE p.target != ''
    SQL;

    $params = [];

    $year       = sanitize_input($_GET['year'] ?? '', '/^\d+$/');
    $user_group = sanitize_input($_GET['user_group'] ?? '', '/^[a-zA-Z ]+$/');
    $campaign   = sanitize_input($_GET['campaign'] ?? '', '/^[a-zA-Z ]+$/');

    if ($year !== null) {
        $added = $year;
        $query .= " AND YEAR(p.pupdate) = ?";
        $params[] = $added;
    }

    if ($user_group !== null) {
        $query .= " AND p.user IN (SELECT username FROM users WHERE user_group = ?)";
        $params[] = $user_group;
    }

    if ($campaign !== null) {
        $query .= " AND p.cat IN (SELECT category FROM categories WHERE campaign = ?)";
        $params[] = $campaign;
    }

    $query .= <<<SQL
        GROUP BY LEFT(p.pupdate, 7)
        ORDER BY LEFT(p.pupdate, 7) ASC;
    SQL;

    return ["qua" => $query, "params" => $params];
}

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

$get = $_GET['get'];

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
        $results = array_map(function ($row) {
            return $row['user'];
        }, $results);
        break;

    case 'status':
        $d = make_status_query();
        $query = $d["qua"];
        $params = $d["params"];

        $results = fetch_query($query, $params);

        // apply $params to $qua
        $qua = sprintf(str_replace('?', "'%s'", $query), ...$params);

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


    case 'lang_names':
        $results = get_lang_names();
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
    "query" => $qua,
    "results" => $results
];

echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
