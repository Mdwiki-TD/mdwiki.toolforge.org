<?php
http_response_code(404);

// Include header
include_once __DIR__ . '/header.php';
include_once __DIR__ . '/db404.php';

echo <<<HTML
<div class="card-header aligncenter" style="font-weight:bold;">
    <h3>404 Error.</h3>
</div>
<div class="card-body">
<div class="wrapper">
	<div class="header">
		<p>The page you requested was not found.</p>
	</div>
</div>
HTML;

// Include footer
include_once __DIR__ . '/footer.php';
