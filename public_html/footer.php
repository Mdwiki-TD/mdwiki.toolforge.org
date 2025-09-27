<?php

if (isset($GLOBALS['global_username']) && $GLOBALS['global_username'] != '') {

	if (!isset($_COOKIE['cookie_alert_dismissed1'])) {
		echo <<<HTML
			<div id="cookie-alert" class="alert alert-dismissible fade show" role="alert">
				<div class="d-flex align-items-center justify-content-center text-center fixed-bottom">
					<div class="card border-warning m-1">
						<div class="card-body">
							<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
							<p class="card-text">This website uses cookies to save your username for a better experience.</p>
						</div>
					</div>
				</div>
			</div>
		HTML;
	}
}
?>
</div> <!-- <div class="card-body"> -->
</div> <!-- <div class="card"> -->
</div> <!-- <div id="maindiv" class="container"> -->
</main>
<!-- Footer -->
<footer class='app-footer'>
</footer>
<script>
	const cookieAlert = document.getElementById('cookie-alert');
	if (cookieAlert) {
		cookieAlert.addEventListener('close.bs.alert', function() {
			document.cookie = "cookie_alert_dismissed=true; max-age=31536000; path=/; Secure; SameSite=Lax";
		});
	}
	$(document).ready(function() {
		// $('[data-toggle="tooltip"]').tooltip();
		const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
		const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
	});

	$(function() {
		// attach autocomplete behavior to input field
		$("#title").autocomplete({
			source: function(request, response) {
				// make AJAX request to Wikipedia API
				$.ajax({
					url: "https://mdwiki.org/w/api.php",
					headers: {
						'Api-User-Agent': "Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
					},
					dataType: "jsonp",
					data: {
						action: "query",
						list: "prefixsearch",
						format: "json",
						pssearch: request.term,
						psnamespace: 0,
						psbackend: "CirrusSearch",
						cirrusUseCompletionSuggester: "yes"
					},
					success: function(data) {
						// extract titles from API response and pass to autocomplete
						response($.map(data.query.prefixsearch, function(item) {
							return item.title;
						}));
					}
				});
			}
		});
	});
</script>
</body>

</html>
