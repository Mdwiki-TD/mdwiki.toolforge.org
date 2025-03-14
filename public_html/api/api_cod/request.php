<?php

if (isset($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}
header('Content-Type: application/json');

include_once __DIR__ . '/include.php';

use function API\Langs\get_lang_names_new;
use function API\Langs\get_lang_names;
use function API\SQL\fetch_query;
use function API\InterWiki\get_inter_wiki;
use function API\SiteMatrix\get_site_matrix;
use function API\Helps\sanitize_input;
use function API\Helps\add_li_params;
use function API\Helps\add_group;
use function API\Helps\add_order;
use function API\Helps\add_limit;
use function API\Qids\qids_qua;
use function API\Leaderboard\leaderboard_table_format;
use function API\Status\make_status_query;
use function API\TitlesInfos\titles_query;
use function API\Missing\missing_query;
use function API\Missing\missing_qids_query;

$other_tables = [
    'assessments',
    'refs_counts',
    'enwiki_pageviews',
    'categories',
    'full_translators',
    'projects',
    'settings',
    'translate_type',
    // 'pages',
    // 'pages_users',
];

$DISTINCT = (isset($_GET['distinct'])) ? 'DISTINCT ' : '';
$get = filter_input(INPUT_GET, 'get', FILTER_SANITIZE_SPECIAL_CHARS); //$_GET['get']

// if (!isset($_GET['limit'])) $_GET['limit'] = '50';

$qua = "";
$query = "";
$params = [];
$results = [];
$execution_time = 0;

$select_valids = [
    'count(title) as count',
    'YEAR(date) AS year',
    'YEAR(pupdate) AS year',
    'lang',
    'user',
];

$SELECT = (isset($_GET['select'])) ? filter_input(INPUT_GET, 'select', FILTER_SANITIZE_SPECIAL_CHARS) : '*';

if (!in_array($SELECT, $select_valids)) {
    $SELECT = '*';
};

// load endpoint_params.json
$endpoint_params = json_decode(file_get_contents(__DIR__ . '/../endpoint_params.json'), true);
$endpoint_params = $endpoint_params[$get]['params'] ?? [];
// ---
switch ($get) {

    case 'missing':
        $tab = missing_query($endpoint_params);
        $query = $tab['qua'];
        $params = $tab['params'];
        // echo json_encode($tab);
        break;

    case 'missing_qids':
        $tab = missing_qids_query($endpoint_params);
        $query = $tab['qua'];
        $params = $tab['params'];
        // echo json_encode($tab);
        break;

    case 'users':
        $query = "SELECT username FROM users";
        if (isset($_GET['userlike'])) {
            $added = filter_input(INPUT_GET, 'userlike', FILTER_SANITIZE_SPECIAL_CHARS);
            if ($added !== null) {
                $query .= " WHERE username like ?";
                $params[] = "$added%";
            }
        }
        break;

    case 'titles':
        $tab = titles_query($endpoint_params);
        $query = $tab['qua'];
        $params = $tab['params'];
        // echo json_encode($tab);
        break;

    case 'coordinator':
        $qua = "SELECT $SELECT FROM coordinator";
        $qua = add_limit($qua);
        break;

    case 'leaderboard_table':
    case 'leaderboard_table_formated':
        // ---
        $query = "SELECT p.title,
            p.target, p.cat, p.lang, p.word, YEAR(p.pupdate) AS pup_y, p.user, u.user_group, LEFT(p.pupdate, 7) as m, v.views
            FROM pages p
            LEFT JOIN users u
                ON p.user = u.username
            LEFT JOIN views_new_all v
                ON p.target = v.target
                AND p.lang = v.lang
            WHERE p.target != ''
        ";
        // ---
        $tab = add_li_params($query, [], $endpoint_params);
        // ---
        $query = $tab["qua"];
        // ---
        // $query .= " \n group by v.target, v.lang";
        $query .= " ORDER BY 1 DESC";
        //---
        $params = $tab["params"];
        break;

    case 'status':
        $status = make_status_query();
        $query = $status['qua'];
        $params = $status['params'];
        break;

    case 'views_old':
        $query = <<<SQL
            SELECT *
            FROM views v
            LEFT JOIN pages p
                ON p.target = v.target
                AND p.lang = v.lang
        SQL;
        $tab = add_li_params($query, [], $endpoint_params);
        $query = $tab['qua'];
        $params = $tab['params'];
        break;

    case 'views':
    case 'views_new':
        $query = <<<SQL
            SELECT p.title, v.target, v.lang, v.views as views
            FROM views_new_all v
            LEFT JOIN pages p
                ON p.target = v.target
                AND p.lang = v.lang
        SQL;
        $tab = add_li_params($query, [], $endpoint_params);
        $query = $tab['qua'];
        $params = $tab['params'];
        // $query .= " group by v.target, v.lang"; // used with views_new and sum(v.views)
        $query .= " ORDER BY 1 DESC";
        break;

    case 'user_access':
        $query = "SELECT id, user_name, created_at FROM access_keys";
        $tab = add_li_params($query, [], $endpoint_params);
        $query = $tab['qua'];
        $params = $tab['params'];
        break;

    case 'qids':
        $qua = qids_qua($get);
        break;

    case 'qids_others':
        $qua = qids_qua($get);
        break;

    case 'count_pages':
        $query = "SELECT DISTINCT user, count(target) as count from pages";
        $tab = add_li_params($query, [], $endpoint_params);
        $query = $tab['qua'];
        $params = $tab['params'];
        $query .= " group by user order by count desc";
        break;

    case 'users_by_wiki':
        // , sum(target_count) AS sum_target
        $qua = <<<SQL
            SELECT user, lang, MAX(target_count) AS max_target
                FROM (
                    SELECT user, lang, COUNT(target) AS target_count
                    FROM pages
                    GROUP BY user, lang
                ) AS subquery
            GROUP BY user
            ORDER BY 3 DESC
        SQL;
        break;

    case 'users_by_last_pupdate':
        $qua = <<<SQL
            WITH RankedPages AS (
                SELECT
                    p1.target,
                    p1.user,
                    p1.pupdate,
                    p1.lang,
                    ROW_NUMBER() OVER (PARTITION BY p1.user ORDER BY p1.pupdate DESC) AS rn
                FROM pages p1
                WHERE p1.target != ''
            )
            SELECT target, user, pupdate, lang
            FROM RankedPages
            WHERE rn = 1
            ORDER BY pupdate DESC;
        SQL;
        break;

    case 'lang_names':
        $results = get_lang_names();
        break;

    case 'lang_names_new':
        $results = get_lang_names_new();
        break;

    case 'inter_wiki':
        $ty = sanitize_input($_GET['type'] ?? 'all', '/^[a-zA-Z ]+$/');
        $results = get_inter_wiki($ty);
        break;

    case 'site_matrix':
        $ty = sanitize_input($_GET['type'] ?? 'all', '/^[a-zA-Z ]+$/');
        $results = get_site_matrix($ty);
        break;

    case 'user_views':
    case 'user_views2':
        if (isset($_GET['user'])) {
            $query = <<<SQL
                SELECT p.title, v.target, v.lang, v.views
                FROM views_new_all v
                JOIN pages p
                    ON p.target = v.target
                    AND p.lang = v.lang
            SQL;
            // ---
            $tab = add_li_params($query, [], $endpoint_params);
            // ---
            $query = $tab['qua'];
            // ---
            // $query .= " GROUP BY v.target, v.lang";
            // ---
            $params = $tab['params'];
            // ---
        };
        break;

    case 'lang_views':
    case 'lang_views2':
        if (isset($_GET['lang'])) {
            $query = <<<SQL
                SELECT v.target, v.lang, v.views
                FROM views_new_all v
                LEFT JOIN pages p
                    ON p.target = v.target
                    AND p.lang = v.lang
            SQL;
            // ---
            $tab = add_li_params($query, [], $endpoint_params);
            // ---
            $query = $tab['qua'];
            // $query .= " GROUP BY v.target, v.lang";
            // ---
            $params = $tab['params'];
        };
        break;

    case 'graph_data':
        $qua = <<<SQL
            SELECT LEFT(pupdate, 7) as m, COUNT(*) as c
            FROM pages
            WHERE target != ''
            GROUP BY LEFT(pupdate, 7)
            ORDER BY LEFT(pupdate, 7) ASC
        SQL;
        break;

    case 'words':
        $params = [];
        $query = "SELECT * FROM words ";
        // ---
        $tab = add_li_params($query, [], $endpoint_params);
        // ---
        $query = $tab['qua'];
        $params = $tab['params'];
        // ---
        /*
        // التحقق من عنوان الكلمات
        $title = sanitize_input($_GET['title'] ?? '', '/^[a-zA-Z0-9\s_-]+$/');
        if ($title !== null) {
            $query .= " AND w_title = ?";
            $params[] = $title;
        }

        // التحقق من عدد كلمات المقدمة
        $lead_words = sanitize_input($_GET['lead_words'] ?? '', '/^\d+$/');
        if ($lead_words !== null) {
            $query .= " AND w_lead_words = ?";
            $params[] = $lead_words;
        }

        // التحقق من عدد كل الكلمات
        $all_words = sanitize_input($_GET['all_words'] ?? '', '/^\d+$/');
        if ($all_words !== null) {
            $query .= " AND w_all_words = ?";
            $params[] = $all_words;
        }
        */
        break;

    case 'pages_by_user_or_lang':
        // ---
        $qua = <<<SQL
            SELECT DISTINCT *
            FROM pages p
            LEFT JOIN views_new_all v
                ON p.target = v.target
                AND p.lang = v.lang
        SQL;
        // ---
        $tab = add_li_params($qua, [], $endpoint_params);
        // ---
        $query = $tab['qua'];
        $params = $tab['params'];
        // ---
        $query = add_group($query);
        $query = add_order($query);
        // ---
        break;

    case 'pages':
    case 'pages_users':
        // ---
        $qua = "SELECT $DISTINCT $SELECT FROM $get";
        // ---
        $tab = add_li_params($qua, [], $endpoint_params);
        // ---
        $query = $tab['qua'];
        $params = $tab['params'];
        // ---
        $title_not_in_pages = (isset($_GET['title_not_in_pages'])) ? true : false;
        // ---
        if ($title_not_in_pages) {
            $query .= " and title not in (select p.title from pages p WHERE p.lang = lang and p.target != '') ";
        }
        // ---
        $query = add_group($query);
        $query = add_order($query);
        // ---
        break;

    default:
        if (in_array($get, $other_tables)) {
            $query = "SELECT * FROM $get";
            $tab = add_li_params($query, [], $endpoint_params);
            $query = $tab['qua'];
            $params = $tab['params'];
            break;
        }
        $results = ["error" => "invalid get request"];
        break;
}

if ($results === [] && ($qua !== "" || $query !== "")) {
    $start_time = microtime(true);
    if ($query !== "") {
        $query = add_limit($query);
        // apply $params to $qua
        $qua = sprintf(str_replace('?', "'%s'", $query), ...$params);
        $results = fetch_query($query, $params);
    } else {
        $qua = add_limit($qua);
        $results = fetch_query($qua);
    }
    $end_time = microtime(true);
    $execution_time = $end_time - $start_time;
    $execution_time = number_format($execution_time, 2);
}

$qua = str_replace(["\n", "\r"], " ", $qua);
$qua = preg_replace("/ +/", " ", $qua);

// ---
switch ($get) {
    case 'leaderboard_table_formated':
        $results = leaderboard_table_format($results);
        break;
}
$out = [
    "time" => $execution_time,
    // "query" => $qua,
    "length" => count($results),
    "results" => $results
];

// if server is localhost then add query to out
if ($_SERVER['SERVER_NAME'] === 'localhost') {
    $out = [
        "query" => $qua,
        "time" => $execution_time,
        "length" => count($results),
        "results" => $results
    ];
};
$out["supported_params"] = [];
foreach ($endpoint_params as $param) {
    $out["supported_params"][] = $param["name"];
};

echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
