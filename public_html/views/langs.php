<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>WikiProject Medicine Pageviews - Lang</title>
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
$lang = $_GET['lang'] ?? '';
$sub_dir_selected = $_GET['sub_dir'] ?? 'all-agens';

if (!$lang) {
    header("Location: index.php");
    exit;
}

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
                    <input type="hidden" name="lang" value="<?= htmlspecialchars($lang) ?>">
                    <select name="sub_dir" class="form-select form-select-sm" onchange="this.form.submit()">
                        <?php foreach ($type_titles as $type => $title): ?>
                            <option value="<?= $type ?>" <?= $type === $sub_dir_selected ? 'selected' : '' ?>><?= $title ?></option>
                        <?php endforeach; ?>
                    </select>
                </form>
            </span>
            <span class="h3">WikiProject Medicine Pageviews (lang: <?= htmlspecialchars($lang) ?>)</span>
            <a class='h2 btn btn-secondary' href='index.php'> >> Return</a>
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
                    <table id="langTable" class="table table-striped table-bordered table-sm w-100">
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        const lang = '<?= $lang ?>';
        const subDir = '<?= $sub_dir_selected ?>';

        async function loadChart() {
            try {
                const response = await fetch(`langs_api.php?lang=${lang}&sub_dir=${subDir}&chart_data=1`);
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
                console.error('Error loading chart:', err);
            }
        }

        async function loadTable() {
            try {
                const response = await fetch(`langs_api.php?lang=${lang}&sub_dir=${subDir}`);
                const res = await response.json();

                if (res.error) {
                    alert(res.error);
                    return;
                }

                const columns = [
                    { data: 'index', title: '#' },
                    {
                        data: 'title',
                        title: 'Title',
                        render: function(data, type, row) {
                            if (row.is_summary) return `<strong>${data}</strong>`;
                            const encodedTitle = encodeURIComponent(data);
                            return `<a class='item' href='https://${lang}.wikipedia.org/wiki/${encodedTitle}' target='_blank'>${data}</a>`;
                        }
                    }
                ];

                res.years.forEach(year => {
                    columns.push({
                        data: year,
                        title: String(year),
                        render: function(data, type, row) {
                            const val = Number(data).toLocaleString();
                            if (row.is_summary) return `<strong>${val}</strong>`;
                            const encodedTitle = encodeURIComponent(row.title);
                            const projectLang = (lang === 'be-x-old') ? 'be-tarask' : lang;
                            return `<a class='item' href='https://pageviews.wmcloud.org/pageviews/?project=${projectLang}.wikipedia.org&platform=all-access&agent=all-agents&redirects=0&start=${year}-01&end=${year}-12&pages=${encodedTitle}' target='_blank'>${val}</a>`;
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

                $('#langTable').DataTable({
                    data: res.data,
                    columns: columns,
                    paging: true,
                    pageLength: 50,
                    searching: true,
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
                console.error('Error loading table:', err);
            }
        }

        $(document).ready(async function() {
            await Promise.all([
                loadChart(),
                loadTable()
            ]);
            $('#loading').fadeOut();
        });
    </script>
</body>

</html>
