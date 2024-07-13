<?php
include_once __DIR__ . '/../d/db1.php';
http_response_code(404);

echo <<<HTML
<div class="wrapper">
	<div class="header">
		<h1>404 Error</h1>
		<p>The page you requested was not found.</p>
	</div>
</div>
HTML;
