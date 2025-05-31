<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<title>Logins</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<!-- <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> -->
	<?php

	$hoste = ($_SERVER["SERVER_NAME"] == "localhost")
		? "https://cdnjs.cloudflare.com"
		: "https://tools-static.wmflabs.org/cdnjs";

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
	foreach ($scripts as $js) {
		echo "\n\t<script src='" . $js . "'></script>";
	}
	foreach ($scripts_module as $js) {
		echo "\n\t<script type='module' src='" . $js . "'></script>";
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
