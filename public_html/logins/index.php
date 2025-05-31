<!DOCTYPE html>
<html lang="en">
<?php
require_once __DIR__ . "/header1.php";

// تحديد رابط API من الرابط (query parameter)
$apiUrl = isset($_GET['api']) ? $_GET['api'] : '/logins/api.php';

$apis = [
	'/logins/api.php' => 'Local',
	'https://mdwiki.toolforge.org/logins/api.php' => 'MDWiki',
	'https://himo.toolforge.org/logins/api.php' => 'Himo'
];

?>

<body dir="ltr" class="mt-3">
	<div class="container">
		<div class="card shadow">
			<div class="card-header">
				<div class="row">
					<div class="col-md-6">
						<h2 class="card-title mb-0 text-center">API requests statistics</h2>
					</div>
					<div class="col-md-6">
						<!-- قائمة اختيار مصدر API -->
						<form method="GET" class="mb-0">
							<label for="api" class="form-label fw-bold">API source:</label>
							<select name="api" id="api" class="form-select w-auto d-inline-block" onchange="this.form.submit()">
								<?php
								foreach ($apis as $url => $name) {
									echo '<option value="' . $url . '" ' . ($url === $apiUrl ? 'selected' : '') . '>' . $name . '</option>';
								};
								?>
							</select>
						</form>
					</div>
				</div>
			</div>
			<div class="card-body">
				<div class="row">
					<div class="col-md-6">
						<canvas id="loginsChart" height="70"></canvas>
					</div>
					<div class="col-md-6" id="ActionsChartContainer">
						<canvas id="ActionsChart" height="70"></canvas>
					</div>
				</div>
				<hr>
				<ul id="navs" class="nav nav-tabs" role="tablist">
					<li class="nav-item">
						<button class="nav-link active" id="All-tab" data-bs-toggle="tab" data-bs-target="#All-tab-pane"
							site="All" table-id="catsTableAll"
							type="button" role="tab" aria-controls="All-tab-pane" aria-selected="false">All</button>
					</li>
				</ul>
				<div class="tab-content" id="TabContents">
					<div class="tab-pane fade show active pt-3" id="All-tab-pane" role="tabpanel" aria-labelledby="All-tab" tabindex="0">
						<table id="catsTableAll" class="table table-striped table-bordered" style="width:100%">
							<thead>
								<tr>
									<th>#</th>
									<th>Count</th>
									<th>action</th>
									<th>site</th>
									<th>result</th>
									<th>username</th>
									<th>first</th>
									<th>last</th>
									<th>diff</th>
								</tr>
							</thead>
							<tbody></tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
	</div>
	<script src="index.js"></script>
	<script>
		const apiUrl = <?= json_encode($apiUrl) ?>;
		$(document).ready(async function() {
			await start(apiUrl);
		});
	</script>
</body>

</html>
