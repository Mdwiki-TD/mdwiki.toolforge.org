<!DOCTYPE html>
<HTML lang=en dir=ltr xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> 
	<meta name="robots" content="noindex">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>WikiProjectMed Tools</title>
<?php 
//---
if ($_REQUEST['test'] != '') {
	// echo(__file__);
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);
};
//---
function print_head() {
	$hoste = 'https://tools-static.wmflabs.org/cdnjs';
	if ( $_SERVER['SERVER_NAME'] == 'localhost' )  $hoste = 'https://cdnjs.cloudflare.com';
	//---
    echo "
		<link href='$hoste/ajax/libs/font-awesome/5.15.3/css/all.min.css' rel='stylesheet' type='text/css'>
		<script src='$hoste/ajax/libs/jquery/3.6.1/jquery.min.js'></script>
		
		<script src='$hoste/ajax/libs/popper.js/1.16.1/umd/popper.min.js'></script>
		<!--
		<script src='$hoste/ajax/libs/twitter-bootstrap/4.6.2/js/bootstrap.min.js'></script>
		<link href='$hoste/ajax/libs/twitter-bootstrap/4.6.2/css/bootstrap.min.css' rel='stylesheet' type='text/css'>
		-->
		<script src='$hoste/ajax/libs/twitter-bootstrap/5.2.3/js/bootstrap.min.js'></script>
		<link href='$hoste/ajax/libs/twitter-bootstrap/5.2.3/css/bootstrap.min.css' rel='stylesheet' type='text/css'>

		<script src='$hoste/ajax/libs/datatables/1.10.21/js/jquery.dataTables.min.js'></script>
		<link href='$hoste/ajax/libs/datatables/1.10.21/css/jquery.dataTables.min.css' rel='stylesheet' type='text/css'>
		<link href='$hoste/ajax/libs/datatables/1.10.21/css/dataTables.bootstrap4.min.css' rel='stylesheet' type='text/css'>
        <link href='Translation_Dashboard/dashboard_new1.css' rel='stylesheet'>
		";
};
//---
function add_quotes($str) {
	// if str have ' then use "
	// else use '
	$value = "'$str'";
	if (preg_match("/[\']+/", $str)) $value = '"' . $str . '"';
	return $value;
};
//---
print_head();
//---
?>
	
</head>
<style> 
a {
text-decoration: none;
}</style>
<body>
<header>
	<nav id="mainnav" class="navbar navbar-expand-md bg-light shadow">
	   	<div class="container-fluid" id="navbardiv">
			<a class="navbar-brand mb-0 h1" href="index.php" style="color:blue;">WikiProjectMed Tools</a>
			<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
				<span class="navbar-toggler-icon"></span>
			</button>
			<div class="collapse navbar-collapse" id="collapsibleNavbar">
				<ul class="navbar-nav me-auto">
					<a class="nav-link" target="_blank" href="https://github.com/MrIbrahem/mdwiki.toolforge.org">Github</a>
				</ul>
				<div class="d-flex">
					<ul class="nav navbar-nav ml-auto">
						<li class="nav-item" id="">
						</li>
					</ul>
				</div>
			</div>
		</div>
	</nav>
</header>
<main id="body">
    <br>
	<!-- <div id="maindiv" class="container-fluid"> -->
	<div id="maindiv" class="container">
		<div class="card">