<?php
//---
if ($_REQUEST['test'] != '') {
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);
};
//---
$path = explode('/public_html', __FILE__)[0];
//---
$jobsc = "toolforge jobs run updatemd --command '$path/update_mdcore.sh' --image mariadb";
//---
echo '<br>' . $jobsc . '<br>';
//---
$result = shell_exec( $jobsc );
//---
echo $result;
//---

