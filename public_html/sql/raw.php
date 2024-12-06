<?php
//---
function raw($qua, $pass, $raw, $sqlpass)
{
    if (!empty($qua) and ($pass == $sqlpass or $_SERVER['SERVER_NAME'] == 'localhost')) {
        //---
        include_once __DIR__ . '/sql_result.php';
        make_sql_result($qua, $raw);
        //---
    };
}
