</div>
</main>

<script>
	$(document).ready(function() {

		$('[data-toggle="tooltip"]').tooltip();

		setTimeout(function() {
			$('.soro2').DataTable({
				// paging: false,
				info: false,
				lengthMenu: [
					[50, 100, 150, 200],
					[50, 100, 150, 200]
				],
				searching: false
			});

			$('.soro').DataTable({
				lengthMenu: [
					[100, 200],
					[100, 200]
				],
			});
		}, 3000);
	});
</script>
</body>

</html>