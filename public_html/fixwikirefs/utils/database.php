<?php

namespace RefsOAuth\MdwikiSql;

use PDO;
use PDOException;

class Database
{

    private $db;
    private $host;
    private $user;
    private $password;
    private $dbname;
    private $groupByModeDisabled = false;

    public function __construct(string $dbname_var = 'DB_NAME')
    {
        $this->set_db($dbname_var);
    }

    private function envVar(string $key)
    {
        $value = getenv($key);
        if ($value !== false) {
            return $value;
        }

        if (array_key_exists($key, $_ENV)) {
            return $_ENV[$key];
        }

        return "";
    }
    private function set_db(string $dbname_var)
    {
        $this->host = $this->envVar('DB_HOST') ?: 'tools.db.svc.wikimedia.cloud';
        $this->dbname = $this->envVar($dbname_var);
        $this->user = $this->envVar('TOOL_TOOLSDB_USER');
        $this->password = $this->envVar('TOOL_TOOLSDB_PASSWORD');

        try {
            $this->db = new PDO("mysql:host=$this->host;dbname=$this->dbname", $this->user, $this->password);
            $this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch (PDOException $e) {
            // Log the error message
            error_log($e->getMessage());
            // In testing mode, re-throw the exception so tests can catch it and skip
            if (getenv('APP_ENV') === 'testing') {
                throw $e;
            }
            // Display a generic message
            echo "Unable to connect to the database. Please try again later.";
            exit();
        }
    }

    public function disableFullGroupByMode($sql_query)
    {
        // if the query contains "GROUP BY", disable ONLY_FULL_GROUP_BY, strtoupper() is for case insensitive
        if (strpos(strtoupper($sql_query), 'GROUP BY') !== false && !$this->groupByModeDisabled) {
            try {
                // More precise SQL mode modification
                $this->db->exec("SET SESSION sql_mode=(SELECT REPLACE(@@SESSION.sql_mode,'ONLY_FULL_GROUP_BY',''))");
                $this->groupByModeDisabled = true;
            } catch (PDOException $e) {
                // Log error but don't fail the query
                error_log("Failed to disable ONLY_FULL_GROUP_BY: " . $e->getMessage());
            }
        }
    }
    public function executequery($sql_query, $params = null)
    {
        try {
            $this->disableFullGroupByMode($sql_query);

            $q = $this->db->prepare($sql_query);
            if ($params) {
                $q->execute($params);
            } else {
                $q->execute();
            }

            // Check if the query starts with "SELECT"
            $query_type = strtoupper(substr(trim((string) $sql_query), 0, 6));
            if ($query_type === 'SELECT') {
                // Fetch the results if it's a SELECT query
                $result = $q->fetchAll(PDO::FETCH_ASSOC);
                return $result;
            } else {
                // Otherwise, return null
                return [];
            }
        } catch (PDOException $e) {
            // In testing mode, re-throw to allow tests to skip
            if (getenv('APP_ENV') === 'testing') {
                throw $e;
            }
            echo "sql error:" . $e->getMessage() . "<br>" . $sql_query;
            return [];
        }
    }

    public function fetchquery($sql_query, $params = null)
    {
        try {
            $this->disableFullGroupByMode($sql_query);

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
            // In testing mode, re-throw to allow tests to skip
            if (getenv('APP_ENV') === 'testing') {
                throw $e;
            }
            echo "SQL Error:" . $e->getMessage() . "<br>" . $sql_query;
            // error_log("SQL Error: " . $e->getMessage() . " | Query: " . $sql_query);
            return [];
        }
    }

    public function __destruct()
    {
        $this->db = null;
    }
}


function fetch_queries($sql_query, $params = null)
{
    // Create a new database object
    $db = new Database('DB_NAME');

    // Execute a SQL query
    if ($params) {
        $results = $db->fetchquery($sql_query, $params);
    } else {
        $results = $db->fetchquery($sql_query);
    }

    // Print the results
    // foreach ($results as $row) echo $row['column1'] . " " . $row['column2'] . "<br>";

    // Destroy the database object
    $db = null;

    //---
    return $results;
};
