<!DOCTYPE html>
<HTML lang=en dir=ltr data-bs-theme="light" xmlns="http://www.w3.org/1999/xhtml">
<?php
// ---
$test   = $_REQUEST['test'] ?? '';
if ($test != '' || $_SERVER['SERVER_NAME'] == 'localhost') {
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);
};

include_once('functions.php');

function print_head()
{
	$hoste = 'https://tools-static.wmflabs.org/cdnjs';
	if ($_SERVER['SERVER_NAME'] == 'localhost')  $hoste = 'https://cdnjs.cloudflare.com';
	// ---
	echo <<<HTML
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
			<meta name="robots" content="noindex">
			<meta http-equiv="X-UA-Compatible" content="IE=edge">
			<meta name="viewport" content="width=device-width, initial-scale=1">
			<meta name="color-scheme" content="light dark" />

			<meta name="theme-color" content="#111111" media="(prefers-color-scheme: light)" />
			<meta name="theme-color" content="#eeeeee" media="(prefers-color-scheme: dark)" />
			<title>World Health Organization essential medicines list</title>
	HTML;
	// ---
	if (isset($_GET['noboot']) == '') {
		echo <<<HTML
			<link href='/Translation_Dashboard/css/Responsive_Table.css' rel='stylesheet' type='text/css'>
			<link href='/Translation_Dashboard/css/dashboard_new1.css' rel='stylesheet' type='text/css'>
			<link href='$hoste/ajax/libs/font-awesome/5.15.3/css/all.min.css' rel='stylesheet' type='text/css'>
			<link href='$hoste/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css' rel='stylesheet' type='text/css'>
			<link href='$hoste/ajax/libs/datatables.net-bs5/1.13.5/dataTables.bootstrap5.css' rel='stylesheet' type='text/css'>
			<link rel="stylesheet" href="$hoste/ajax/libs/bootstrap-select/1.14.0-beta3/css/bootstrap-select.css" rel='stylesheet' type='text/css'>

			<script src='$hoste/ajax/libs/jquery/3.7.0/jquery.min.js'></script>
			<script src='$hoste/ajax/libs/popper.js/2.11.8/umd/popper.min.js'></script>
			<script src='$hoste/ajax/libs/bootstrap/5.3.0/js/bootstrap.min.js'></script>
			<script src='$hoste/ajax/libs/datatables.net/2.1.1/jquery.dataTables.min.js'></script>
			<script src='$hoste/ajax/libs/datatables.net-bs5/1.13.5/dataTables.bootstrap5.min.js'></script>
			<script src="$hoste/ajax/libs/bootstrap-select/1.14.0-beta3/js/bootstrap-select.min.js"></script>
			<script src='/Translation_Dashboard/plugins/chart.js/Chart.min.js'></script>

			<style>
			a {
				text-decoration: none;
			}</style>
		</head>
		HTML;
	};
};

print_head();

require __DIR__ . '/../helps/darkmode.php';
$them_li = dark_mode_icon();

echo <<<HTML
<body>

<header class="mb-3 border-bottom">
	<nav id="mainnav" class="navbar navbar-expand-lg shadow">
	   	<div class="container-fluid" id="navbardiv">
			<a class="navbar-brand mb-0 h1" href="index.php" style="color:#0d6efd;">
				WHO essential medicines
			</a>
			<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar"
				aria-controls="collapsibleNavbar" aria-expanded="false" aria-label="Toggle navigation">
				<span class="navbar-toggler-icon"></span>
			</button>
			<div class="collapse navbar-collapse" id="collapsibleNavbar">
				<ul class="navbar-nav flex-row flex-wrap bd-navbar-nav">
					<li class="nav-item col-4 col-lg-auto" id="prior">
						<a class="nav-link py-2 px-0 px-lg-2" href="index.php">
							<span class="navtitles">Top Languages</span>
						</a>
					</li>
					<li class="nav-item col-4 col-lg-auto">
						<a class="nav-link py-2 px-0 px-lg-2" href="https://mdwiki.org/wiki/Category:World_Health_Organization_essential_medicines" target="_blank">
							<span class="navtitles">WHO list</span>
						</a>
					</li>
					<li class="nav-item col-4 col-lg-auto">
						<a class="nav-link py-2 px-0 px-lg-2" href="https://github.com/MrIbrahem/mdwiki.toolforge.org/tree/main/public_html" target="_blank" rel="noopener noreferrer">
							<span class="navtitles">Github</span>
						</a>
					</li>
				</ul>
				<hr class="d-lg-none text-black-50">
				<ul class="navbar-nav flex-row flex-wrap bd-navbar-nav ms-lg-auto">
					<li class="nav-item col-4 col-lg-auto dropdown">
						$them_li
					</li>
				</ul>
			</div>
		</div>
	</nav>
</header>
HTML;
?>
<main id="body">
	<!-- <div id="maindiv" class="container-fluid"> -->
	<div id="maindiv" class="container-fluid">
		<br>
