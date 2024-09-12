<?PHP

if (isset($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};

$td_dir = __DIR__ . '/../Translation_Dashboard';

include_once $td_dir . '/vendor_load.php';

include_once $td_dir . '/Tables/sql_tables.php';
include_once $td_dir . '/Tables/tables.php';
include_once $td_dir . '/actions/functions.php';
include_once $td_dir . '/actions/mdwiki_sql.php';
include_once $td_dir . '/actions/curl_api.php';

include_once $td_dir . '/auth/config.php';
include_once $td_dir . '/auth/helps.php';
include_once $td_dir . '/auth/send_edit.php';

include_once __DIR__ . '/helps.php';
include_once __DIR__ . '/add_to_db.php';
include_once __DIR__ . '/text.php';
