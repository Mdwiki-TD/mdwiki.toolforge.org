<!DOCTYPE html>
<HTML lang=en dir=ltr data-bs-theme="light" xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> 
	<meta name="robots" content="noindex">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="color-scheme" content="light dark" />

    <meta name="theme-color" content="#111111" media="(prefers-color-scheme: light)" />
    <meta name="theme-color" content="#eeeeee" media="(prefers-color-scheme: dark)" />
	<title>World Health Organization essential medicines list</title>
<?php

if ($_REQUEST['test'] != '' || $_SERVER['SERVER_NAME'] == 'localhost') {
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);
};

include_once('functions.php');
// include_once('../Translation_Dashboard/login5.php');
$hoste = '';

function print_head() {
	global $hoste;
	$hoste = 'https://tools-static.wmflabs.org/cdnjs';
	if ( $_SERVER['SERVER_NAME'] == 'localhost' )  $hoste = 'https://cdnjs.cloudflare.com';

	if (isset($_GET['noboot']) == '') {
		echo <<<HTML
		<link href='/Translation_Dashboard/css/styles.css' rel='stylesheet' type='text/css'>
		<link href='/Translation_Dashboard/css/Responsive_Table.css' rel='stylesheet' type='text/css'>
		<link href='/Translation_Dashboard/css/dashboard_new1.css' rel='stylesheet' type='text/css'>
		<link href='$hoste/ajax/libs/font-awesome/5.15.3/css/all.min.css' rel='stylesheet' type='text/css'>
		<link href='$hoste/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css' rel='stylesheet' type='text/css'>
		<link href='$hoste/ajax/libs/datatables.net-bs5/1.13.5/dataTables.bootstrap5.css' rel='stylesheet' type='text/css'>
		<!-- <link href='$hoste/ajax/libs/datatables.net-buttons-bs5/2.4.1/buttons.bootstrap5.css' rel='stylesheet' type='text/css'> -->
		<!-- <link href='$hoste/ajax/libs/jqueryui/1.13.2/themes/base/jquery-ui.min.css' rel='stylesheet' type='text/css'> -->
		<link rel="stylesheet" href="$hoste/ajax/libs/bootstrap-select/1.14.0-beta3/css/bootstrap-select.css" rel='stylesheet' type='text/css'>

		<script src='$hoste/ajax/libs/jquery/3.7.0/jquery.min.js'></script>
		<script src='$hoste/ajax/libs/popper.js/2.11.8/umd/popper.min.js'></script>
		<script src='$hoste/ajax/libs/bootstrap/5.3.0/js/bootstrap.min.js'></script>
		<script src='$hoste/ajax/libs/datatables.net/2.1.1/jquery.dataTables.min.js'></script>
		<script src='$hoste/ajax/libs/datatables.net-bs5/1.13.5/dataTables.bootstrap5.min.js'></script>
		<!-- <script src='$hoste/ajax/libs/jqueryui/1.13.2/jquery-ui.min.js'></script> -->
		<script src="$hoste/ajax/libs/bootstrap-select/1.14.0-beta3/js/bootstrap-select.min.js"></script>

		<!-- <script src='$hoste/ajax/libs/datatables.net-buttons/2.4.1/js/dataTables.buttons.min.js'></script>
		<script src='$hoste/ajax/libs/datatables.net-buttons-bs5/2.4.1/buttons.bootstrap5.min.js'></script>
		<script src="$hoste/ajax/libs/datatables.net-buttons/2.4.1/js/buttons.html5.min.js"></script>
		<script src="$hoste/ajax/libs/datatables.net-buttons/2.4.1/js/buttons.print.min.js"></script> -->

		<script type="module" src="/Translation_Dashboard/js/color-modes.js"></script>
		<script src='/Translation_Dashboard/plugins/chart.js/Chart.min.js'></script>
		<!-- <script src='/Translation_Dashboard/js/sorttable.js'></script> -->

		<style> 
		a {
			text-decoration: none;
		}</style>
		HTML;
	};

};

print_head();

echo "
</head>";

$them_li = <<<HTML
	<button class="btn btn-link nav-link py-2 px-0 px-lg-2 dropdown-toggle d-flex align-items-center" id="bd-theme" type="button" aria-expanded="false" data-bs-toggle="dropdown" data-bs-display="static" aria-label="Toggle theme (light)">
	<svg class="bi my-1 theme-icon-active"><use href="#sun-fill"></use></svg>
	<span class="d-lg-none ms-2" id="bd-theme-text"></span>
	</button>
	<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="bd-theme-text">
	<li>
			<button type="button" class="dropdown-item d-flex align-items-center active" data-bs-theme-value="light" aria-pressed="true">
			<svg class="bi me-2 opacity-50 theme-icon"><use href="#sun-fill"></use></svg>
			Light
			<svg class="bi ms-auto d-none"><use href="#check2"></use></svg>
			</button>
		</li>
		<li>
			<button type="button" class="dropdown-item d-flex align-items-center" data-bs-theme-value="dark" aria-pressed="false">
			<svg class="bi me-2 opacity-50 theme-icon"><use href="#moon-stars-fill"></use></svg>
			Dark
			<svg class="bi ms-auto d-none"><use href="#check2"></use></svg>
			</button>
		</li>
		<li>
			<button type="button" class="dropdown-item d-flex align-items-center" data-bs-theme-value="auto" aria-pressed="false">
			<svg class="bi me-2 opacity-50 theme-icon"><use href="#circle-half"></use></svg>
			Auto
			<svg class="bi ms-auto d-none"><use href="#check2"></use></svg>
			</button>
		</li>
	</ul>
HTML;

echo <<<HTML
<body>
<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
      <symbol id="bootstrap" viewBox="0 0 512 408" fill="currentcolor">
        <path d="M106.342 0c-29.214 0-50.827 25.58-49.86 53.32.927 26.647-.278 61.165-8.966 89.31C38.802 170.862 24.07 188.707 0 191v26c24.069 2.293 38.802 20.138 47.516 48.37 8.688 28.145 9.893 62.663 8.965 89.311C55.515 382.42 77.128 408 106.342 408h299.353c29.214 0 50.827-25.58 49.861-53.319-.928-26.648.277-61.166 8.964-89.311 8.715-28.232 23.411-46.077 47.48-48.37v-26c-24.069-2.293-38.765-20.138-47.48-48.37-8.687-28.145-9.892-62.663-8.964-89.31C456.522 25.58 434.909 0 405.695 0H106.342zm236.559 251.102c0 38.197-28.501 61.355-75.798 61.355h-87.202a2 2 0 01-2-2v-213a2 2 0 012-2h86.74c39.439 0 65.322 21.354 65.322 54.138 0 23.008-17.409 43.61-39.594 47.219v1.203c30.196 3.309 50.532 24.212 50.532 53.085zm-84.58-128.125h-45.91v64.814h38.669c29.888 0 46.373-12.03 46.373-33.535 0-20.151-14.174-31.279-39.132-31.279zm-45.91 90.53v71.431h47.605c31.12 0 47.605-12.482 47.605-35.941 0-23.46-16.947-35.49-49.608-35.49h-45.602z"/>
      </symbol>
      <symbol id="check2" viewBox="0 0 16 16">
        <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>
      </symbol>
      <symbol id="circle-half" viewBox="0 0 16 16">
        <path d="M8 15A7 7 0 1 0 8 1v14zm0 1A8 8 0 1 1 8 0a8 8 0 0 1 0 16z"/>
      </symbol>
      <symbol id="moon-stars-fill" viewBox="0 0 16 16">
        <path d="M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278z"/>
        <path d="M10.794 3.148a.217.217 0 0 1 .412 0l.387 1.162c.173.518.579.924 1.097 1.097l1.162.387a.217.217 0 0 1 0 .412l-1.162.387a1.734 1.734 0 0 0-1.097 1.097l-.387 1.162a.217.217 0 0 1-.412 0l-.387-1.162A1.734 1.734 0 0 0 9.31 6.593l-1.162-.387a.217.217 0 0 1 0-.412l1.162-.387a1.734 1.734 0 0 0 1.097-1.097l.387-1.162zM13.863.099a.145.145 0 0 1 .274 0l.258.774c.115.346.386.617.732.732l.774.258a.145.145 0 0 1 0 .274l-.774.258a1.156 1.156 0 0 0-.732.732l-.258.774a.145.145 0 0 1-.274 0l-.258-.774a1.156 1.156 0 0 0-.732-.732l-.774-.258a.145.145 0 0 1 0-.274l.774-.258c.346-.115.617-.386.732-.732L13.863.1z"/>
      </symbol>
      <symbol id="sun-fill" viewBox="0 0 16 16">
        <path d="M8 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z"/>
      </symbol>
    </svg>

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