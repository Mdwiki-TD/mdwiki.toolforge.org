</div> <!-- <div class="card-body"> -->
</div> <!-- <div class="card"> -->
</div> <!-- <div id="maindiv" class="container"> -->
</main>
<!-- Footer -->
<footer class='app-footer'>
</footer>
<script>
	$(document).ready(function () {
		// $('[data-toggle="tooltip"]').tooltip();
		const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
		const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
	});

</script>
</body>

</html>
