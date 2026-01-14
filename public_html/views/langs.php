<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WikiProject Medicine Pageviews | Language Details</title>

    <!-- CSS Frameworks -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <link href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css' rel='stylesheet'>

    <style>
        :root {
            --primary-color: #4f46e5;
            --primary-hover: #4338ca;
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border-color: #e2e8f0;
            --accent-color: #10b981;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
            --radius-md: 12px;
            --radius-lg: 16px;
        }

        body {
            background-color: var(--bg-body);
            color: var(--text-main);
            overflow-x: hidden;
            letter-spacing: -0.01em;
        }

        /* Loading Overlay */
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.9);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            backdrop-filter: blur(8px);
            transition: all 0.4s ease;
        }

        .spinner-custom {
            width: 48px;
            height: 48px;
            border: 4px solid var(--border-color);
            border-bottom-color: var(--primary-color);
            border-radius: 50%;
            animation: rotation 1s linear infinite;
        }

        @keyframes rotation {
            0% {
                transform: rotate(0deg)
            }

            100% {
                transform: rotate(360deg)
            }
        }

        /* Navbar / Header */
        .dashboard-header {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            padding: 1.25rem 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .dashboard-title {
            font-weight: 700;
            font-size: 1.5rem;
            color: var(--primary-color);
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .dashboard-title i {
            font-size: 1.25rem;
        }

        /* Controls */
        .form-select-custom {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            font-weight: 500;
            color: var(--text-main);
            padding: 0.5rem 2.5rem 0.5rem 1rem;
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
            cursor: pointer;
        }

        .form-select-custom:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
            outline: none;
        }

        /* Cards */
        .card-premium {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 2rem;
            overflow: hidden;
        }

        .card-premium:hover {
            box-shadow: var(--shadow-lg);
        }

        .card-header-premium {
            background: transparent;
            border-bottom: 1px solid var(--border-color);
            padding: 1.25rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .card-header-premium h2 {
            font-size: 1.1rem;
            font-weight: 600;
            margin: 0;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .card-body-premium {
            padding: 1.5rem;
        }

        /* Table Styling */
        #langTable_wrapper .dataTables_info,
        #langTable_wrapper .dataTables_paginate {
            margin-top: 1.5rem;
            font-weight: 500;
        }

        .table-premium {
            border-collapse: separate;
            border-spacing: 0;
        }

        .table-premium thead th {
            background-color: #f1f5f9;
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            padding: 1rem 1.5rem;
            border-bottom: 2px solid var(--border-color);
            text-align: center;
        }

        .table-premium tbody td {
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
            vertical-align: middle;
            font-weight: 500;
            text-align: center;
        }

        .table-premium tbody tr:last-child td {
            border-bottom: none;
        }

        .table-premium tbody tr:hover {
            background-color: rgba(79, 70, 229, 0.02);
            transition: background 0.2s ease;
        }

        .table-premium tr.summary-row {
            background-color: #eef2ff !important;
            font-weight: 700;
            color: var(--primary-color);
        }

        .table-premium a {
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 600;
            transition: color 0.2s ease;
        }

        .table-premium a:hover {
            color: var(--primary-hover);
            text-decoration: underline;
        }

        /* Animations */
        .fade-in {
            animation: fadeIn 0.8s ease-out;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-body);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-muted);
        }

        .chart-container {
            position: relative;
            height: 350px;
            width: 100%;
        }

        .badge-lang {
            background: rgba(79, 70, 229, 0.1);
            color: var(--primary-color);
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-family: monospace;
            font-weight: 700;
        }

        .btn-return {
            color: var(--text-muted);
            text-decoration: none;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: color 0.2s ease;
        }

        .btn-return:hover {
            color: var(--primary-color);
        }
    </style>
</head>

<?php
$lang = basename($_GET['lang'] ?? '');
$sub_dir_selected = $_GET['sub_dir'] ?? 'all-agents';

if (!$lang) {
    header("Location: index.php");
    exit;
}

$type_titles = [
    "all-agents" => "All Agents",
    "users-agents" => "Users Agents",
];
?>

<body>
    <div id="loading" class="loading-overlay">
        <div class="spinner-custom"></div>
        <p class="mt-3 font-weight-600 text-muted">Preparing language data...</p>
    </div>

    <!-- Header -->
    <header class="dashboard-header mb-4">
        <div class="container">
            <div class="d-flex flex-column flex-md-row align-items-center justify-content-between gap-3">
                <div class="d-flex align-items-center gap-4">
                    <a href="index.php?sub_dir=<?= $sub_dir_selected ?>" class="btn-return">
                        <i class="fa-solid fa-arrow-left"></i>
                        <span>Back</span>
                    </a>
                    <h1 class="dashboard-title">
                        <i class="fa-solid fa-language"></i>
                        Details for: <span class="ms-2 badge-lang" style="font-size: 1.2rem;"><?= htmlspecialchars($lang) ?></span>
                    </h1>
                </div>

                <div class="d-flex align-items-center gap-3">
                    <form method="get" id="subDirForm" class="m-0">
                        <input type="hidden" name="lang" value="<?= htmlspecialchars($lang) ?>">
                        <select name="sub_dir" class="form-select-custom" onchange="this.form.submit()">
                            <?php foreach ($type_titles as $type => $title): ?>
                                <option value="<?= $type ?>" <?= $type === $sub_dir_selected ? 'selected' : '' ?>><?= $title ?></option>
                            <?php endforeach; ?>
                        </select>
                    </form>
                </div>
            </div>
        </div>
    </header>

    <main class="container fade-in">
        <!-- Chart Section -->
        <div class="card-premium">
            <div class="card-header-premium">
                <h2><i class="fa-solid fa-wave-square me-2" style="color: var(--primary-color)"></i> Traffic Trends</h2>
                <span class="text-muted small font-weight-500">Language Pageviews by Year</span>
            </div>
            <div class="card-body-premium">
                <div class="chart-container">
                    <canvas id="viewsChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Table Section -->
        <div class="card-premium">
            <div class="card-header-premium">
                <h2><i class="fa-solid fa-table me-2" style="color: var(--primary-color)"></i> Article Distribution</h2>
                <div class="d-flex gap-2">
                    <span class="badge" style="background: var(--bg-body); border: 1px solid var(--border-color); color: var(--text-muted);">
                        <i class="fa-solid fa-book-medical me-1"></i> Article details
                    </span>
                </div>
            </div>
            <div class="card-body-premium">
                <div class="table-responsive">
                    <table id="langTable" class="table table-premium w-100">
                    </table>
                </div>
            </div>
        </div>
    </main>

    <!-- Scripts -->
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <script>
        const lang = <?= json_encode($lang) ?>;
        const subDir = <?= json_encode($sub_dir_selected) ?>;

        async function loadChart() {
            try {
                const response = await fetch(`api.php?lang=${lang}&sub_dir=${subDir}&chart_data=1`);
                const res = await response.json();

                const ctx = document.getElementById('viewsChart').getContext('2d');

                // Create gradient
                const gradient = ctx.createLinearGradient(0, 0, 0, 400);
                gradient.addColorStop(0, 'rgba(79, 70, 229, 0.4)');
                gradient.addColorStop(1, 'rgba(79, 70, 229, 0)');

                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: res.labels,
                        datasets: [{
                            label: 'Total Views',
                            data: res.data,
                            borderColor: '#4f46e5',
                            borderWidth: 3,
                            backgroundColor: gradient,
                            fill: true,
                            tension: 0.4,
                            pointRadius: 4,
                            pointBackgroundColor: '#fff',
                            pointBorderColor: '#4f46e5',
                            pointBorderWidth: 2,
                            pointHoverRadius: 6,
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {
                            mode: 'index',
                            intersect: false,
                        },
                        plugins: {
                            legend: {
                                display: false
                            },
                            tooltip: {
                                backgroundColor: '#1e293b',
                                titleFont: {
                                    size: 14,
                                    weight: 'bold'
                                },
                                bodyFont: {
                                    size: 13
                                },
                                padding: 12,
                                cornerRadius: 8,
                                displayColors: false,
                                callbacks: {
                                    label: function(context) {
                                        return context.parsed.y.toLocaleString() + ' Views';
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                border: {
                                    display: false
                                },
                                grid: {
                                    color: '#f1f5f9'
                                },
                                ticks: {
                                    color: '#64748b',
                                    font: {
                                        size: 12
                                    },
                                    callback: function(value) {
                                        if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M';
                                        if (value >= 1000) return (value / 1000).toFixed(1) + 'K';
                                        return value;
                                    }
                                }
                            },
                            x: {
                                border: {
                                    display: false
                                },
                                grid: {
                                    display: false
                                },
                                ticks: {
                                    color: '#64748b',
                                    font: {
                                        size: 12
                                    }
                                }
                            }
                        }
                    }
                });
            } catch (err) {
                console.error('Error fetching chart data:', err);
            }
        }

    async function loadTable() {
        try {
            // First fetch to get columns/years metadata
            const initResponse = await fetch(`api.php?lang=${lang}&sub_dir=${subDir}&start=0&length=1`);
            const initRes = await initResponse.json();

            if (initRes.error) {
                alert(initRes.error);
                return;
            }

            const years = initRes.years;
            const columns = [
                { data: 'index', title: '#' },
                {
                    data: 'title',
                    title: 'Article Title',
                    render: function(data, type, row) {
                        if (row.is_summary) return `<strong>Total Stats</strong>`;
                        const encodedTitle = encodeURIComponent(data);
                        return `<div class="d-flex align-items-center">
                                    <i class="fa-brands fa-wikipedia-w me-2 text-muted"></i>
                                    <a href='https://${lang}.wikipedia.org/wiki/${encodedTitle}' target='_blank'>${data}</a>
                                </div>`;
                    }
                }
            ];

            years.forEach(year => {
                columns.push({
                    data: year,
                    title: String(year),
                    render: function(data, type, row) {
                        const val = Number(data).toLocaleString();
                        if (row.is_summary) return `<strong>${val}</strong>`;

                        const params = {
                            project: `${lang}.wikipedia.org`,
                            platform: 'all-access',
                            agent: (subDir === 'users-agents') ? 'user' : 'all-agents',
                            redirects: 0,
                            start: `${year}-01`,
                            end: `${year}-12`,
                            pages: row.title
                        };
                        const queryString = new URLSearchParams(params).toString();
                        return `<a class="text-decoration-none" style="font-weight: 500;" href="https://pageviews.wmcloud.org/pageviews/?${queryString}" target="_blank">${val}</a>`;
                    }
                });
            });

            columns.push({
                data: 'total',
                title: 'Cumulative',
                render: function(data, type, row) {
                    const val = Number(data).toLocaleString();
                    return `<strong>${val}</strong>`;
                }
            });

            $('#langTable').DataTable({
                serverSide: true,
                ajax: {
                    url: 'api.php',
                    data: function(d) {
                        d.lang = lang;
                        d.sub_dir = subDir;
                    },
                    dataSrc: 'data'
                },
                columns: columns,
                paging: true,
                pageLength: 500,
                lengthChange: true,
                lengthMenu: [[100, 500, 1000, 5000], [100, 500, 1000, 5000]],
                searching: false,
                order: [[0, 'asc']],
                dom: '<"d-flex justify-content-between align-items-center mb-3"lp>rtip',
                language: {
                    paginate: {
                        previous: '<i class="fa-solid fa-chevron-left"></i>',
                        next: '<i class="fa-solid fa-chevron-right"></i>'
                    }
                },
                columnDefs: [
                    { targets: 0, width: "40px" }
                ],
                createdRow: function(row, data, dataIndex) {
                    if (data.is_summary) {
                        $(row).addClass('summary-row');
                    }
                }
            });
        } catch (err) {
            console.error('Error fetching table data:', err);
        }
    }

        $(document).ready(async function() {
            await Promise.all([
                loadChart(),
                loadTable()
            ]);

            $('#loading').fadeOut(600);
        });
    </script>
</body>

</html>
