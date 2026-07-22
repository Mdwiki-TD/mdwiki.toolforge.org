<?php
include_once __DIR__ . '/header.php';
?>

<div class="card">
	<div class="card-header aligncenter" style="font-weight:bold;">
		<h3>WikiProjectMed Tools</h3>
	</div>
	<div class="card-body">
		<ul>
			<li><a href="Translation_Dashboard/index.php">Translation Dashboard</a></li>
			<li><a href="prior/index.php">Prior List</a></li>
			<li><a href="WHO/index.php">World Health Organization essential medicines list</a></li>
			<li><a href="//ncc.toolforge.org/ncc2/index.php">NC Commons Import Bot Leaderboard</a></li>
		</ul>

		<div class='container'>
			<div class='row'>
				<div class='col-md'>
					<h4>mdwiki tools:</h4>
					<ul>
						<li><a href="https://mdw.toolforge.org/newupdater/">Med updater</a></li>
						<li><a href="https://mdw.toolforge.org/jobs/create_redirects">Create redirects</a></li>
						<li><a href="https://mdw.toolforge.org/jobs/import_history">Import history</a></li>
						<li><a href="https://mdw.toolforge.org/jobs/find_and_replace">Find and replace</a>
						<li><a href="https://mdw.toolforge.org/fixred/">Fix redirects</a></li>
						<li><a href="https://mdw.toolforge.org/jobs/fixref">Normalize references</a></li>
					</ul>
				</div>

				<div class='col-md'>
					<h4>wikipedia's tools:</h4>
					<ul>
						<li><a href="fixwikirefs.php">Fix references</a></li>
					</ul>
				</div>
			</div>
		</div>
	</div>
</div>

<?php
include_once __DIR__ . '/footer.php';
?>
