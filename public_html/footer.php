        	</div> <!-- <div class="card-body"> -->
        	</div> <!-- <div class="card"> -->
        	</div> <!-- <div id="maindiv" class="container"> -->
        	</main>
        	<!-- Footer -->
        	<footer class='app-footer'>
        	</footer>
        	<script>
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
