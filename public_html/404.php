<?php
http_response_code(404);

// Include header
require('header.php');
//---
// the root path is the first part of the split file path
$pathParts = explode('public_html', __FILE__);
$ROOT_PATH = $pathParts[0];
//---
// Output HTML structure
print_h3_title("404 Error.");

echo <<<HTML
<div class="wrapper">
	<div class="header">
		<p>The page you requested was not found.</p>
	</div>
</div>
HTML;

// Include footer
require 'footer.php';
