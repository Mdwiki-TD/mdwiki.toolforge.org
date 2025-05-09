<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<title>Translated Pages</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
	<link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css">
	<link rel="stylesheet" href="https://cdn.datatables.net/buttons/2.4.1/css/buttons.bootstrap5.min.css">
	<style>
		tfoot input {
			width: 100%;
			padding: 3px;
			box-sizing: border-box;
		}

		th {
			text-align: center !important;
		}

		.stats-box {
			margin-bottom: 15px;
		}

		.filter-buttons {
			margin-bottom: 15px;
		}
	</style>
</head>

<body dir="ltr">
	<nav class="navbar navbar-expand-lg bg-body-tertiary shadow mb-4">
		<div class="container-fluid">
			<span class="navbar-brand">Translated Pages</span>
			<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
				<span class="navbar-toggler-icon"></span>
			</button>
			<div class="collapse navbar-collapse" id="navbarNav">
				<ul class="navbar-nav">
					<li class="nav-item">
						<a class="nav-link" href="#">#</a>
					</li>
				</ul>
			</div>
		</div>
	</nav>

	<div class="container">
		<div class="card shadow">
			<div class="card-header">
				<h4 class="card-title mb-0 text-center">Titles</h4>
			</div>
			<div class="card-body">
				<div class="row mb-2">
					<div class="col-md-10">
						<div class="row mb-3">
							<div class="col-md-3">
								<form id="limitForm" class="d-flex">
									<input type="number" id="limitInput" class="form-control" min="1" value="100" placeholder="عدد السجلات">
									<button type="submit" class="btn btn-outline-primary me-2">تحديد</button>
								</form>
							</div>
						</div>
					</div>
				</div>

				<table id="catsTable" class="table table-striped table-bordered" style="width:100%">
					<thead>
						<tr>
							<th>#</th>
							<th>User</th>
							<th>Lang.</th>
							<th>Title</th>
							<th>Translated</th>
							<th>Publication date</th>
							<th>Edit</th>
						</tr>
					</thead>
					<tfoot>
					</tfoot>
					<tbody></tbody>
				</table>
			</div>
		</div>
	</div>

	<!-- مكتبات JS -->
	<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
	<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
	<script src="https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js"></script>
	<script src="https://cdn.datatables.net/buttons/2.4.1/js/dataTables.buttons.min.js"></script>
	<script src="script.js"></script>
	<script>
		$(document).ready(function() {
			load_data();
		});
	</script>

</body>

</html>
