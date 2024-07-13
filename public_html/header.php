<!DOCTYPE html>
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
include_once __DIR__ . '/../d/db1.php';
ini_set('session.use_strict_mode', '1');
//---
include_once 'Translation_Dashboard/auth/index.php';
//---
echo "
<span id='myusername' style='display:none'>" . $username . "</span>";
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
		<link href='$hoste/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css' rel='stylesheet' type='text/css'>
		<link href='$hoste/ajax/libs/datatables.net-bs5/1.13.1/dataTables.bootstrap5.css' rel='stylesheet' type='text/css'>
		<link href='$hoste/ajax/libs/jqueryui/1.13.2/themes/base/jquery-ui.min.css' rel='stylesheet' type='text/css'>

		<script src='$hoste/ajax/libs/jquery/3.7.0/jquery.min.js'></script>
		<script src='$hoste/ajax/libs/popper.js/2.11.8/umd/popper.min.js'></script>
		<script src='$hoste/ajax/libs/bootstrap/5.3.0/js/bootstrap.min.js'></script>
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
require("Translation_Dashboard/darkmode.php");
$them_li = dark_mode_icon();
//---
$login_icon = <<<HTML
	<a role="button" class="nav-link py-2 px-0 px-lg-2" href="/Translation_Dashboard/auth.php?a=login">
		<i class="fas fa-sign-in-alt fa-sm fa-fw mr-2"></i> <span class="navtitles">Login</span>
	</a>
HTML;
//---
echo <<<HTML
<body>
	<header class="mb-3 border-bottom">
		<nav id="mainnav" class="navbar navbar-expand-lg shadow">
			<div class="container-fluid" id="navbardiv">
				<a class="navbar-brand mb-0 h1" href="index.php" style="color:#0d6efd;">
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
						<li class="nav-item col-4 col-lg-auto" id="">
							<a id="username_li" href="#" class="nav-link py-2 px-0 px-lg-2" style="display:none">
								<i class="fas fa-user fa-sm fa-fw mr-2"></i> <span class="navtitles" id="user_name"></span>
							</a>
						</li>
						<li class="nav-item col-4 col-lg-auto" id="loginli">
							$login_icon
						</li>
						<li class="nav-item col-4 col-lg-auto">
							<a id="logout_btn" class="nav-link py-2 px-0 px-lg-2" href="/Translation_Dashboard/auth.php?a=logout" style="display:none">
								<i class="fas fa-sign-out-alt fa-sm fa-fw mr-2"></i> <span class="d-lg-none navtitles">Logout</span>
							</a>
						</li>
					</ul>
				</div>
			</div>
		</nav>
	</header>
HTML;
?>
<script>
	// $(document).ready(function() {
	var lo = $('#myusername').text();
	if (lo != '') {
		$('#myboard').show();
		$('#user_name').text(lo);

		$('#login_btn, #loginli').hide();
		$("#doit_btn, #username_li, #logout_btn").show();

	} else {
		$('#login_btn, #loginli').show();
		$("#doit_btn, #username_li, #logout_btn").hide();
	};
	// });
</script>
<main id="body">
	<br>
	<!-- <div id="maindiv" class="container-fluid"> -->
	<div id="maindiv" class="container">
		<div class="card">
