<?php

require('header.php');

?>
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>WikiProjectMed Tools</h3>
    </div>
    <div class="card-body">
		<ul>
			<li><a href="Translation_Dashboard/index.php">Translation Dashboard</a> </li>
			<li><a href="prior/index.php">Prior List</a> </li>
		</ul>
		<div class='container'>
			<div class='row'>
			  <div class='col-md'>
				<h4>mdwiki tools:</h4>
				<ul>
					<li><a href="mdwiki3.php">Med updater</a> </li>
					<li><a href="redirect.php">Create redirects</a> </li>
					<li><a href="import-history.php">Import history</a> </li>
					<li><a href="replace.php">Find and replace</a> (<a href="replace-log.php">Logs</a>)</li>
					<li><a href="dup.php">Fix duplicte redirects</a> </li>
					<li><a href="fixred.php">Fix redirects</a> </li>
					<li><a href="fixref.php">Normalize references</a> </li>
				</ul>
			  </div>
			  <div class='col-md'>
				<h4>wikipedia's tools:</h4>
				<ul>
					<li><a href="fixwikirefs.php">Fix references</a> </li>
				</ul>
			  </div>
			</div>
		</div>
    </div>
<?php

require('foter.php');

?>