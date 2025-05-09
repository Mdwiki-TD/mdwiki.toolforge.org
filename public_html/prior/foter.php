</div>
</main>

<script>
	function copy() {
		let textarea = document.getElementById("userslist");
		textarea.select();
		document.execCommand("copy");
	}

	function copy_target_text(id) {
		let textarea = document.getElementById(id);
		textarea.select();
		document.execCommand("copy");
	}
	$(document).ready(function() {
		var table = $('.soro2').DataTable({
			// paging: false,
			info: false,
			lengthMenu: [
				[30, 50, 100, 150, 200],
				[30, 50, 100, 150, 200]
			],
			searching: false,
			// lengthChange: false
		});

		$('[data-toggle="tooltip"]').tooltip();

		$('.sortable').DataTable({
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
