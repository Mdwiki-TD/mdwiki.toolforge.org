        </div>
    </div>
</main>
<!-- Footer -->
<footer class='app-footer'>
</footer>
<script>
	$( function() {
		// attach autocomplete behavior to input field
		$("#title").autocomplete({
			source: function(request, response) {
				// make AJAX request to Wikipedia API
				$.ajax({
				url: "https://mdwiki.org/w/api.php",
				dataType: "jsonp",
				data: {
					action: "query",
					list: "prefixsearch",
					format: "json",
					pssearch: request.term,
					psnamespace: 0,
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