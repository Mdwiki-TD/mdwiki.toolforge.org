﻿<!DOCTYPE html>
<HTML lang=en dir=ltr data-bs-theme="light" xmlns="http://www.w3.org/1999/xhtml">
<?php
//---
echo <<<HTML
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<meta name="robots" content="noindex">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>WikiProjectMed Tools</title>
HTML;
//---
$test   = $_REQUEST['test'] ?? '';
if ($test != '' || $_SERVER['SERVER_NAME'] == 'localhost') {
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);
};
//---
ini_set('session.use_strict_mode', '1');
//---
$dir_t = __DIR__;
//---
if (strpos(__FILE__, "I:\\") !== false) $dir_t = "I:/mdwiki/";
//---
include_once $dir_t  . '/auth/auth/user_infos.php';
//---
$hoste = '';
//---
function print_h3_title($h3_title)
{
	echo <<<HTML
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>$h3_title</h3>
    </div>
    <div class="card-body">
HTML;
}
//---
function print_head()
{
	global $hoste;
	$hoste = 'https://tools-static.wmflabs.org/cdnjs';
	if ($_SERVER['SERVER_NAME'] == 'localhost')  $hoste = 'https://cdnjs.cloudflare.com';
	//---
	echo <<<HTML
		<link href='/Translation_Dashboard/css/styles.css' rel='stylesheet' type='text/css'>
		<link href='/Translation_Dashboard/css/Responsive_Table.css' rel='stylesheet' type='text/css'>
		<link href='/Translation_Dashboard/css/dashboard_new1.css' rel='stylesheet' type='text/css'>
		<link href='$hoste/ajax/libs/font-awesome/5.15.3/css/all.min.css' rel='stylesheet' type='text/css'>
		<link href='$hoste/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css' rel='stylesheet' type='text/css'>
		<link href='$hoste/ajax/libs/datatables.net-bs5/1.13.1/dataTables.bootstrap5.css' rel='stylesheet' type='text/css'>
		<link href='$hoste/ajax/libs/jqueryui/1.13.2/themes/base/jquery-ui.min.css' rel='stylesheet' type='text/css'>
		<link href="$hoste/ajax/libs/bootstrap-icons/1.11.3/font/bootstrap-icons.min.css" rel='stylesheet' type='text/css'>

		<script src='$hoste/ajax/libs/jquery/3.7.0/jquery.min.js'></script>
		<script src='$hoste/ajax/libs/popper.js/2.11.8/umd/popper.min.js'></script>
		<script src='$hoste/ajax/libs/bootstrap/5.3.3/js/bootstrap.min.js'></script>
		<script src='$hoste/ajax/libs/datatables.net/2.1.1/jquery.dataTables.min.js'></script>
		<script src='$hoste/ajax/libs/datatables.net-bs5/1.13.1/dataTables.bootstrap5.min.js'></script>
		<script src='$hoste/ajax/libs/jqueryui/1.13.2/jquery-ui.min.js'></script>

		<script type="module" src="/Translation_Dashboard/js/color-modes.js"></script>
		<script src='/Translation_Dashboard/js/sorttable.js'></script>
		<script src='/Translation_Dashboard/js/to.js'></script>

		<style>
		a {
			text-decoration: none;
		}</style>
	HTML;
};
//---
function add_quotes($str)
{
	// if str have ' then use "
	// else use '
	$value = "'$str'";
	if (preg_match("/[\']+/", $str)) $value = '"' . $str . '"';
	return $value;
};
//---
print_head();
//---
echo "</head>";
//---
$them_li = <<<HTML
	<button class="btn btn-link nav-link py-2 px-0 px-lg-2 dropdown-toggle d-flex align-items-center" id="bd-theme" type="button" aria-expanded="false" data-bs-toggle="dropdown"
		data-bs-display="static" aria-label="Toggle theme (light)">
		<span class="theme-icon-active my-1">
			<i class="bi bi-sun-fill"></i>
		</span>
		<span class="d-lg-none ms-2" id="bd-theme-text"></span>
	</button>
	<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="bd-theme-text">
		<li>
			<button type="button" class="dropdown-item d-flex align-items-center active" data-bs-theme-value="light" aria-pressed="true">
				<i class="bi bi-sun-fill me-2 opacity-50 theme-icon"></i> Light
			</button>
		</li>
		<li>
			<button type="button" class="dropdown-item d-flex align-items-center" data-bs-theme-value="dark" aria-pressed="false">
				<i class="bi bi-moon-stars-fill me-2 opacity-50 theme-icon"></i> Dark
			</button>
		</li>
		<li>
			<button type="button" class="dropdown-item d-flex align-items-center" data-bs-theme-value="auto" aria-pressed="false">
				<i class="bi bi-circle-half me-2 opacity-50 theme-icon"></i> Auto
			</button>
		</li>
	</ul>
HTML;
//---
$li_user = <<<HTML
	<li class="nav-item col-4 col-lg-auto">
		<a role="button" class="nav-link py-2 px-0 px-lg-2" href="/auth/index.php?a=login">
			<i class="fas fa-sign-in-alt fa-sm fa-fw mr-2"></i> <span class="navtitles">Login</span>
		</a>
	</li>
HTML;
//---
if (defined('global_username') && global_username != '') {
	$u_name = global_username;
	$li_user = <<<HTML
	<li class="nav-item col-4 col-lg-auto">
		<a href="#" class="nav-link py-2 px-0 px-lg-2">
			<i class="fas fa-user fa-sm fa-fw mr-2"></i> <span class="navtitles">$u_name</span>
		</a>
	</li>
	<li class="nav-item col-4 col-lg-auto">
		<a class="nav-link py-2 px-0 px-lg-2" href="/auth/index.php?a=logout">
			<i class="fas fa-sign-out-alt fa-sm fa-fw mr-2"></i> <span class="d-lg-none navtitles">Logout</span>
		</a>
	</li>
HTML;
};
//---
echo <<<HTML
<body>
	<header class="mb-3 border-bottom">
		<nav id="mainnav" class="navbar navbar-expand-lg shadow">
			<div class="container-fluid" id="navbardiv">
				<a class="navbar-brand mb-0 h1" href="/index.php" style="color:#0d6efd;">
					WikiProjectMed Tools
				</a>
				<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar"
					aria-controls="collapsibleNavbar" aria-expanded="false" aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				</button>
				<div class="collapse navbar-collapse" id="collapsibleNavbar">
					<ul class="navbar-nav flex-row flex-wrap bd-navbar-nav">
						<li class="nav-item col-4 col-lg-auto">
							<a class="nav-link py-2 px-0 px-lg-2" href="/Translation_Dashboard/index.php" target="_blank">
								<span class="navtitles">Translation Dashboard</span>
							</a>
						</li>
						<li class="nav-item col-4 col-lg-auto">
							<a class="nav-link py-2 px-0 px-lg-2" href="/Translation_Dashboard/leaderboard.php" target="_blank">
								<span class="navtitles">Leaderboard</span>
							</a>
						</li>
						<li class="nav-item col-4 col-lg-auto">
							<a class="nav-link py-2 px-0 px-lg-2" href="https://github.com/MrIbrahem/mdwiki.toolforge.org" target="_blank">
								<span class="navtitles">Github</span>
							</a>
						</li>
					</ul>
					<hr class="d-lg-none text-black-50">
					<ul class="navbar-nav flex-row flex-wrap bd-navbar-nav ms-lg-auto">
						<li class="nav-item col-4 col-lg-auto dropdown">
							$them_li
						</li>
						$li_user
					</ul>
				</div>
			</div>
		</nav>
	</header>
HTML;
?>
<main id="body">
	<!-- <div id="maindiv" class="container-fluid"> -->
	<div id="maindiv" class="container">
		<div class="card">
