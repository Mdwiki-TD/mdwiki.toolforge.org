<?php
//---

/*
// ---
UPDATE pages

SET title = REPLACE(title, char(9), ''),
target = REPLACE(target, char(9), '')
// ---
delete from pages where (target = '' OR target IS NULL) and date < ADDDATE(CURDATE(), INTERVAL -7 DAY)
select * from pages where (target = '' OR target IS NULL) and date < ADDDATE(CURDATE(), INTERVAL -7 DAY)
// ---
delete table
DROP table views_by_month ;
// ---
// add columns
ALTER TABLE `pages` ADD `add_date` VARCHAR(120) NULL DEFAULT NULL AFTER `target`;
// ---
CREATE TABLE coordinator (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(120) NOT NULL
    )
// ---
INSERT INTO categories (category, display) SELECT 'RTT', '';
CREATE TABLE categories (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(120) NOT NULL,
    display VARCHAR(120) NOT NULL
    )
// ---
CREATE TABLE qids (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(120) NOT NULL,
    qid VARCHAR(120) NULL
    )
// ---
INSERT INTO qids (title, qid) SELECT DISTINCT p.title, '' from pages p WHERE NOT EXISTS (SELECT 1 FROM qids q WHERE q.title= p.title)
// ---
CREATE TABLE pages (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(120) NOT NULL,
    word INT(6) NULL,
    translate_type VARCHAR(20) NULL,
    cat VARCHAR(120) NULL,
    lang VARCHAR(30) NULL,
    date VARCHAR(120) NULL,
    user VARCHAR(120) NULL,
    pupdate VARCHAR(120) NULL,
    target VARCHAR(120) NULL
    )
// ---
CREATE TABLE words (
    w_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    w_title VARCHAR(120) NOT NULL,
    w_lead_words INT(6) NULL,
    w_all_words INT(6) NULL
    )
*/

use function OAuth\MdwikiSql\fetch_queries;
use function OAuth\MdwikiSql\execute_queries;

function make_sql_result($qua)
{
    //---
    $start_time = microtime(true);
    //---
    $uu = execute_queries($qua);
    //---
    $execution_time = number_format(microtime(true) - $start_time, 2);
    //---
    $start = <<<HTML
    <table class="table table-striped sortable">
        <thead>
            <tr>
                <th>#</th>
    HTML;
    //---
    $text = '';
    //---
    $number = 0;
    //---
    foreach ($uu as $id => $row) {
        $number = $number + 1;
        $tr = '';
        //---
        // echo var_export(json_encode($row, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), 1) . "<br>";
        // '{ "user": "Dr3939", "targets": 1, "words": null, "views": "3922" }'
        // ---
        foreach ($row as $column => $value) {
            // if (!empty($column)) {
            // ---
            if (!preg_match('/^\d+$/', $column, $m)) {
                // ---
                $value = strval($value);
                // ---
                $tr .= "<td>$value</th>";
                // ---
                if ($number == 1) {
                    $start .= "<th class='text-nowrap'>$column</th>";
                };
            };
        }
        //---
        if (!empty($tr)) {
            $text .= "<tr><td>$number</td>$tr</tr>";
        };
        //---
    };
    //---
    $start .= <<<HTML
        </tr>
        </thead>
    HTML;
    //---
    // echo "<h4>sql results:$number. (time:$execution_time)</h4>";
    echo "<h4>SQL Results: $number (Execution time: $execution_time seconds)</h4>";
    //---
    echo $start . $text . '</table>';
    //---
    if (isset($_GET['test'])) var_export($uu);
    //---
    if (empty($text)) {
        if (isset($_GET['test'])) {
            print_r($uu);
        } else {
            echo var_dump($uu);
        };
    };
}

function get_sql_pass()
{
    // ---
    $pathParts = explode('public_html', __FILE__)[0];
    // if root path find (I:\) then $ROOT_PATH = ""
    if (strpos($pathParts, "I:\\") !== false) {
        $pathParts = "I:/mdwiki/mdwiki/";
    }
    // ---
    $_dir = $pathParts . '/confs/';
    // ---
    $ini = parse_ini_file($_dir . 'OAuthConfig.ini');
    // ---
    return $ini['sqlpass'];
}

function get_sql_result($qua, $pass)
{
    if ($_SERVER['SERVER_NAME'] == 'localhost') {
        return make_sql_result($qua);
    }
    // ---
    $sqlpass = get_sql_pass();
    // ---
    if ($pass == $sqlpass) {
        return make_sql_result($qua);
    }
}
