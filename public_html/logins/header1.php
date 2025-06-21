<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<title>Logins</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<!-- <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> -->
	<?php
	function get_host()
	{
		// $hoste = get_host();
		//---
		static $cached_host = null;

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

			$result = curl_exec($ch);
			$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
			curl_close($ch);

			// إذا فشل الاتصال أو لم تكن الاستجابة ضمن 200–399، نستخدم cdnjs
			if ($result === false || $httpCode < 200 || $httpCode >= 400) {
				$hoste = "https://cdnjs.cloudflare.com";
			}
		}

		$cached_host = $hoste;

		return $hoste;
	}

	$hoste = get_host();

	$stylesheets = [
		"$hoste/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css",
		"$hoste/ajax/libs/datatables.net-bs5/1.13.6/dataTables.bootstrap5.min.css",
		// "$hoste/ajax/libs/Chart.js/3.0.1/chart.min.css",
		// "$hoste/ajax/libs/datatables.net-buttons-bs5/2.4.1/buttons.bootstrap5.min.css",
	];

	$scripts = [
		"$hoste/ajax/libs/jquery/3.7.1/jquery.min.js",
		"$hoste/ajax/libs/bootstrap/5.3.3/js/bootstrap.min.js",
		"$hoste/ajax/libs/bootstrap/5.3.3/js/bootstrap.bundle.min.js",
		"$hoste/ajax/libs/datatables.net/2.2.2/dataTables.js",
		"$hoste/ajax/libs/datatables.net/1.13.6/jquery.dataTables.min.js",
		"$hoste/ajax/libs/datatables.net-bs5/1.13.6/dataTables.bootstrap5.min.js",
		// "$hoste/ajax/libs/datatables.net-buttons-bs5/2.4.1/buttons.bootstrap5.min.js",

	];

	$scripts_module = [
		"$hoste/ajax/libs/Chart.js/3.0.1/chart.min.js",
	];

	foreach ($stylesheets as $css) {
		echo "\n\t<link rel='stylesheet' href='" . $css . "'>";
	}
	foreach ($scripts_module as $js) {
		echo "\n\t<script type='module' src='" . $js . "'></script>";
	}
	foreach ($scripts as $js) {
		echo "\n\t<script src='" . $js . "'></script>";
	}
	?>
	<style>
		tfoot input {
			width: 100%;
			padding: 3px;
			box-sizing: border-box;
		}

		th {
			text-align: center !important;
		}

		.stats-box {
			margin-bottom: 15px;
		}

		.filter-buttons {
			margin-bottom: 15px;
		}
	</style>
</head>
