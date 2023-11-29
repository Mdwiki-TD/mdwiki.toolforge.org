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
$jsub2 = "jsub -N updatemd $path/update_mdcore.sh";
//---
echo '<br>' . $jsub2 . '<br>';
//---
$result = shell_exec( $jsub2 );
//---
echo $result;
//---
?>