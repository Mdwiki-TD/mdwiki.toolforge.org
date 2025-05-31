<?php

$allowed_origins = [
    'http://localhost',
    'http://localhost:55',
    'https://himo.toolforge.org',
    'https://mdwiki.toolforge.org'
];

$origin = $_SERVER['HTTP_ORIGIN'] ?? '';

if (in_array($origin, $allowed_origins)) {
    header("Access-Control-Allow-Origin: $origin");
    header("Access-Control-Allow-Methods: GET");
    header("Access-Control-Allow-Headers: Content-Type");
}

header('Content-Type: application/json');

if (isset($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};

use PDO;
use PDOException;

class Database
{

    private $db;
    private $host;
    private $user;
    private $password;
    private $dbname;

    public function __construct($server_name)
    {
        if ($server_name === 'localhost' || !getenv('HOME')) {
            $this->host = 'localhost:3306';
            $this->dbname = 'mv';
            $this->user = 'root';
            $this->password = 'root11';
        } else {
            $ts_pw = posix_getpwuid(posix_getuid());
            $ts_mycnf = parse_ini_file($ts_pw['dir'] . "/confs/db.ini");
            $this->host = 'tools.db.svc.wikimedia.cloud';
            // ---
            if (getenv('HOME') == "/data/project/mdwiki") {
                $this->dbname = $ts_mycnf['user'] . "__mdwiki_new";
            } else {
                $this->dbname = $ts_mycnf['user'] . "__mv";
            }
            // ---
            $this->user = $ts_mycnf['user'];
            $this->password = $ts_mycnf['password'];
            unset($ts_mycnf, $ts_pw);
        }

        try {
            $this->db = new PDO("mysql:host=$this->host;dbname=$this->dbname", $this->user, $this->password);
            $this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch (PDOException $e) {
            // Log the error message
            error_log($e->getMessage());
            // Display a generic message
            echo "Unable to connect to the database. Please try again later.";
            exit();
        }
    }

    public function fetch_query($sql_query, $params = null)
    {
        try {
            $q = $this->db->prepare($sql_query);
            if ($params) {
                $q->execute($params);
            } else {
                $q->execute();
            }

            // Fetch the results if it's a SELECT query
            $result = $q->fetchAll(PDO::FETCH_ASSOC);
            return $result;
        } catch (PDOException $e) {
            // echo "sql error:" . $e->getMessage() . "<br>" . $sql_query;
            error_log("SQL Error: " . $e->getMessage() . " | Query: " . $sql_query);
            return array();
        }
    }

    public function __destruct()
    {
        $this->db = null;
    }
}


function fetch_query_new($sql_query)
{
    // ---
    // Create a new database object
    $db = new Database($_SERVER['SERVER_NAME'] ?? '');

    // Execute a SQL query
    $results = $db->fetch_query($sql_query, []);

    // Destroy the database object
    $db = null;

    return $results ?? [];
}

$query = "SELECT DISTINCT count(*) as count, action, site, result, username, MIN(timestamp) AS first, MAX(timestamp) AS last
    from login_attempts
    GROUP BY action, site, result, username ORDER BY 1 DESC
";

if (isset($_GET['limit'])) {
    $added = filter_input(INPUT_GET, 'limit', FILTER_SANITIZE_SPECIAL_CHARS);
    $query .= " LIMIT $added";
}
$result = fetch_query_new($query);

echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
