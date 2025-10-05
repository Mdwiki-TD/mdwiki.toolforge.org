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

// use function OAuth\MdwikiSql\fetch_queries;
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
    $thead = "";
    //---
    $tbody = '';
    //---
    $number = 0;
    //---
    foreach ($uu as $id => $row) {
        $number += 1;
        //---
        // echo var_export(json_encode($row, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), 1) . "<br>";
        // '{ "user": "Dr3939", "targets": 1, "words": null, "views": "3922" }'
        // ---
        if ($number == 1) {
            foreach ($row as $column => $value) {
                $thead .= "<th class='text-nowrap'>$column</th>";
            }
        }
        // ---
        $tr = '';
        // ---
        foreach ($row as $column => $value) {
            // ---
            if (!preg_match('/^\d+$/', $column, $m)) {
                // ---
                $value = ($value !== null) ? strval($value) : 'null';
                // ---
                $tr .= "<td>$value</td>";
            };
        }
        //---
        if (!empty($tr)) {
            $tbody .= "<tr><td>$number</td>$tr</tr>";
        };
    };
    //---
    // echo "<h4>sql results:$number. (time:$execution_time)</h4>";
    echo <<<HTML
        <h4>SQL Results: $number (Execution time: $execution_time seconds)</h4>
        <table class="table table-striped sortable">
            <thead>
                <tr>
                    <th>#</th>
                $thead
                </tr>
            </thead>
            <tbody>
                $tbody
            </tbody>
        </table>
    HTML;
    //---
    if (isset($_GET['test'])) var_export($uu);
    //---
    if (empty($tbody)) {
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
	$ROOT_PATH = getenv("HOME") ?: 'I:/mdwiki/mdwiki';
    // ---
    $_dir = $ROOT_PATH . '/confs/';
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
