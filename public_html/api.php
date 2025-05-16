<?php

if (!isset($_GET['get'])) {
    header("Location: api/test.html");
    exit();
}

require(__DIR__ . '/api/index.php');
