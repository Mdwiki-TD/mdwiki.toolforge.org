<?PHP

if (isset($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};
include_once __DIR__ . '/../Translation_Dashboard/vendor_load.php';

include_once __DIR__ . '/mdwiki_sql.php';

include_once __DIR__ . '/config.php';
include_once __DIR__ . '/do_edit.php';
include_once __DIR__ . '/add_to_db.php';
include_once __DIR__ . '/get_token.php';
include_once __DIR__ . '/helps.php';
include_once __DIR__ . '/text_fix.php';
include_once __DIR__ . '/wd.php';
