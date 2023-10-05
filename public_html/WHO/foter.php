</div>
</main>

<script>
	
	$(document).ready(function() {
		var table = $('.soro2').DataTable( {
			// paging: false,
			info: false,
			lengthMenu: [
				[30, 50, 100, 150, 200],
				[30, 50, 100, 150, 200]
			],
			searching: false,
			// lengthChange: false
		} );
	
		$('[data-toggle="tooltip"]').tooltip();

		$('.sortable').DataTable({
			lengthMenu: [
				[50, 100, 150],[50, 100, 150]
			],
		});
		$('.datatable').DataTable({
			paging: false,
			info: false,
			searching: false
		});
		$('.soro').DataTable({
			lengthMenu: [
				[200, 300, 2500],
				[200, 300, 2500]
			],
		});
	});
</script>
</body>

</html>