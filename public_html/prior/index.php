<?PHP
//---
if (isset($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};

require 'header.php';
require 'tables.php';
include_once 'functions.php';

$users = $_REQUEST['user'] ?? '';
$langs = $_REQUEST['lang'] ?? '';

if ($users !== '') {
    require 'top/users.php';
} elseif ($langs !== '') {
    require 'top/langs.php';
} else {
    require 'top/index.php';
}

require 'foter.php';
?>