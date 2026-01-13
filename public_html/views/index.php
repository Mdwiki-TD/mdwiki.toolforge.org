<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>WikiProject Medicine Pageviews</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <link href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css' rel='stylesheet'>
    <link href='/Translation_Dashboard/css/dashboard_new1.css' rel='stylesheet'>
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

        .DataTable thead th {
            text-align: center;
        }
    </style>
</head>

<?php
$sub_dir_selected = $_GET['sub_dir'] ?? 'all-agens';
$type_titles = [
    "all-agens" => "All Agents",
    "users-agents" => "Users Agents",
];
?>

<body>
    <div id="loading" class="loading-overlay">
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>

    <div class="container-fluid mt-4">
        <div class="text-center d-flex align-items-center justify-content-between">
            <span>
                <form method="get" id="subDirForm">
                    <select name="sub_dir" class="form-select form-select-sm" onchange="this.form.submit()">
                        <?php foreach ($type_titles as $type => $title): ?>
                            <option value="<?= $type ?>" <?= $type === $sub_dir_selected ? 'selected' : '' ?>><?= $title ?></option>
                        <?php endforeach; ?>
                    </select>
                </form>
            </span>
            <span class="h3">WikiProject Medicine Pageviews</span>
            <span></span>
        </div>
        <hr />

        <div class="card mb-4">
            <div class="card-header">
                <span class="card-title h2">Total Views by Year</span>
            </div>
            <div class="card-body">
                <canvas id="viewsChart" height="60"></canvas>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <span class="card-title h2">Views data</span>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table id="mainTable" class="table table-striped table-bordered table-sm w-100">
                    </table>
                </div>
            </div>
        </div>
    </div>

</body>

<script>
    const subDirSelected = '<?= $sub_dir_selected ?>';

    async function loadChart(subDir) {
        try {
            const response = await fetch(`api.php?chart_data=1&sub_dir=${subDir}`);
            const res = await response.json();

            new Chart(document.getElementById('viewsChart'), {
                type: 'line',
                data: {
                    labels: res.labels,
                    datasets: [{
                        label: 'Total Views by Year',
                        data: res.data,
                        borderColor: '#007bff',
                        backgroundColor: 'rgba(0, 123, 255, 0.1)',
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        } catch (err) {
            console.error('Error fetching chart data:', err);
        }
    }

    async function loadTable(subDir) {
        try {
            const response = await fetch(`api.php?sub_dir=${subDir}`);
            const res = await response.json();

            const columns = [
                { data: 'index', title: '#' },
                {
                    data: 'lang',
                    title: 'Lang',
                    render: function(data, type, row) {
                        return row.is_summary ? `<strong>${data}</strong>` : data;
                    }
                },
                {
                    data: 'titles',
                    title: 'Titles',
                    render: function(data, type, row) {
                        const val = Number(data).toLocaleString();
                        if (row.is_summary) return `<strong>${val}</strong>`;
                        return `<a class='item' href='langs.php?lang=${row.lang}&sub_dir=${subDirSelected}'>${val}</a>`;
                    }
                }
            ];

            res.years.forEach(year => {
                columns.push({
                    data: year,
                    title: year,
                    render: function(data, type, row) {
                        const val = Number(data).toLocaleString();
                        return row.is_summary ? `<strong>${val}</strong>` : val;
                    }
                });
            });

            columns.push({
                data: 'total',
                title: 'Total',
                render: function(data, type, row) {
                    const val = Number(data).toLocaleString();
                    return row.is_summary ? `<strong>${val}</strong>` : val;
                }
            });

            $('#mainTable').DataTable({
                data: res.data,
                columns: columns,
                paging: false,
                searching: false,
                order: [
                    [0, 'asc']
                ],
                columnDefs: [{
                    targets: 0,
                    width: "5%"
                }],
                createdRow: function(row, data, dataIndex) {
                    if (data.is_summary) {
                        $(row).addClass('table-primary');
                    }
                }
            });
        } catch (err) {
            console.error('Error fetching table data:', err);
            alert('Failed to load table data. Check console for details.');
        }
    }

    $(document).ready(async function() {
        const subDir = '<?= $sub_dir_selected ?>';

        await Promise.all([
            loadChart(subDir),
            loadTable(subDir)
        ]);

        $('#loading').fadeOut();
    });
</script>

</html>
