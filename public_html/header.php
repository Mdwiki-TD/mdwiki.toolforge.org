<!DOCTYPE html>
<HTML lang=en dir=ltr data-bs-theme="light" xmlns="http://www.w3.org/1999/xhtml">
<?php
//---

if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);
}

echo <<<HTML
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<meta name="robots" content="noindex">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>WikiProjectMed Tools</title>
HTML;
//---
ini_set('session.use_strict_mode', '1');
//---
$dir_t = __DIR__;
//---
if (strpos(__FILE__, "I:\\") !== false) $dir_t = "I:/mdwiki/";
//---
include_once $dir_t  . '/auth/auth/user_infos.php';

function get_host()
{
	// $hoste = get_host();
	//---
	static $cached_host = null;
	//---
	if ($cached_host !== null) {
		return $cached_host; // استخدم القيمة المحفوظة
	}
	//---
	$hoste = ($_SERVER["SERVER_NAME"] == "localhost")
		? "https://cdnjs.cloudflare.com"
		: "https://tools-static.wmflabs.org/cdnjs";
	//---
	if ($hoste == "https://tools-static.wmflabs.org/cdnjs") {
		$url = "https://tools-static.wmflabs.org";
		$ch = curl_init($url);
		curl_setopt($ch, CURLOPT_HEADER, true);
		curl_setopt($ch, CURLOPT_NOBODY, true); // لا نريد تحميل الجسم
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); // لمنع الطباعة

		curl_setopt($ch, CURLOPT_TIMEOUT, 3); // المهلة القصوى للاتصال
		curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 2);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
		curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2);
		curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (compatible; CDN-Checker)');
		curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false);

		$result = curl_exec($ch);
		$curlError = curl_error($ch);
		$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

		curl_close($ch);

		// إذا فشل الاتصال أو لم تكن الاستجابة ضمن 200–399، نستخدم cdnjs
		if ($result === false || !empty($curlError) || $httpCode < 200 || $httpCode >= 400) {
			$hoste = "https://cdnjs.cloudflare.com";
		}
	}

	$cached_host = $hoste;

	return $hoste;
}

function print_head()
{
	//---
	$hoste = get_host();
	//---
	$stylesheets = [
		"/Translation_Dashboard/css/styles.css",
		"/Translation_Dashboard/css/Responsive_Table.css",
		"/Translation_Dashboard/css/dashboard_new1.css",
		"/Translation_Dashboard/css/theme.css",
		"$hoste/ajax/libs/font-awesome/5.15.3/css/all.min.css",
		"$hoste/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css",
		"$hoste/ajax/libs/datatables.net-bs5/1.13.1/dataTables.bootstrap5.css",
		"$hoste/ajax/libs/jqueryui/1.13.2/themes/base/jquery-ui.min.css",
		"$hoste/ajax/libs/bootstrap-icons/1.11.3/font/bootstrap-icons.min.css",
	];
	foreach ($stylesheets as $css) {
		echo "\n\t<link rel='stylesheet' href='" . $css . "'>";
	}

	$scripts = [
		"$hoste/ajax/libs/jquery/3.7.0/jquery.min.js",
		"$hoste/ajax/libs/popper.js/2.11.8/umd/popper.min.js",
		"$hoste/ajax/libs/bootstrap/5.3.3/js/bootstrap.min.js",
		"$hoste/ajax/libs/datatables.net/2.1.1/jquery.dataTables.min.js",
		"$hoste/ajax/libs/datatables.net-bs5/1.13.1/dataTables.bootstrap5.min.js",
		"$hoste/ajax/libs/jqueryui/1.13.2/jquery-ui.min.js",
		"/Translation_Dashboard/js/sorttable.js",
		"/Translation_Dashboard/js/to.js",
		"/Translation_Dashboard/js/theme.js",
		"$hoste/ajax/libs/ace/1.42.0/ace.js",
	];

	foreach ($scripts as $js) {
		echo "\n\t<script src='" . $js . "'></script>";
	}
	echo <<<HTML
		<script type="module" src="/Translation_Dashboard/js/color-modes.js"></script>
		<style>
		a {
			text-decoration: none;
		}</style>
	HTML;
};
//---
print_head();
//---
echo "</head>";
//---
//---
$li_user = <<<HTML
	<li class="nav-item col-4 col-lg-auto">
		<a role="button" class="nav-link py-2 px-0 px-lg-2" href="/auth/index.php?a=login">
			<i class="fas fa-sign-in-alt fa-sm fa-fw mr-2"></i> <span class="navtitles">Login</span>
		</a>
	</li>
HTML;
//---
if (isset($GLOBALS['global_username']) && $GLOBALS['global_username'] != '') {
	$u_name = $GLOBALS['global_username'];
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
				<a class="tool_title navbar-brand mb-0 h1" href="/index.php" style="color:#0d6efd;">
					WikiProjectMed Tools
				</a>
				<button class="navbar-toggler me_ms_by_dir" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar"
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
						<li class="nav-item col-4 col-lg-auto">
							<span class="nav-link py-2 px-0 px-lg-2" id="load_time"></span>
						</li>
					</ul>
					<hr class="d-lg-none text-dark-subtle text-50">
					<ul class="navbar-nav flex-row flex-wrap bd-navbar-nav ms-lg-auto">
						$li_user
					</ul>
				</div>
				<div class="d-flex ms-2">
					<button class="theme-toggle btn btn-link me-ms-auto" aria-label="Toggle theme">
						<i class="bi bi-moon-stars-fill"></i>
					</button>
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
