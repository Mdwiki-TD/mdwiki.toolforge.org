<?PHP

if (isset($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};

require 'header.php';
require 'tables.php';
include_once 'functions.php';

$langs = $_REQUEST['lang'] ?? '';

if ($langs !== '') {
    require 'top/langs.php';
} else {
    require 'top/index.php';
}

require 'foter.php';
?>