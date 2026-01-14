<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WikiProject Medicine Pageviews | Dashboard</title>

    <!-- Fonts -->

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

        [data-theme="dark"] {
            --bg-body: #0f172a;
            --bg-card: #1e293b;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --border-color: #334155;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.3);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.5);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.6);
        }

        body {
            background-color: var(--bg-body);
            color: var(--text-main);
            overflow-x: hidden;
            letter-spacing: -0.01em;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        /* Theme Toggle */
        .theme-toggle {
            cursor: pointer;
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            transition: all 0.2s ease;
            box-shadow: var(--shadow-sm);
        }

        .theme-toggle:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
            border-color: var(--primary-color);
        }

        /* Loading Overlay */
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--bg-body);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            backdrop-filter: blur(8px);
            transition: all 0.4s ease;
        }

        /* Navbar / Header */
        .dashboard-header {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            padding: 1.25rem 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        [data-theme="dark"] .dashboard-header {
            background: rgba(30, 41, 59, 0.8);
        }

        /* Table Styling */
        .table-premium thead th {
            background-color: var(--bg-body);
            color: var(--text-muted);
            border-bottom: 2px solid var(--border-color);
        }

        [data-theme="dark"] .table-premium thead th {
            background-color: #1e293b;
        }

        .table-premium tbody tr:hover {
            background-color: rgba(79, 70, 229, 0.05);
        }

        .table-premium tr.summary-row {
            background-color: rgba(79, 70, 229, 0.08) !important;
            color: var(--primary-color);
        }

        /* Badges */
        .badge-lang {
            background: rgba(79, 70, 229, 0.15);
            color: var(--primary-color);
        }

        [data-theme="dark"] .btn-return {
            color: #94a3b8;
        }

        [data-theme="dark"] .btn-return:hover {
            color: var(--primary-color);
        }

        [data-theme="dark"] .form-select-custom {
            background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%2394a3b8' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3e%3c/svg%3e");
        }

        [data-theme="dark"] .dataTables_wrapper .dataTables_length,
        [data-theme="dark"] .dataTables_wrapper .dataTables_filter,
        [data-theme="dark"] .dataTables_wrapper .dataTables_info,
        [data-theme="dark"] .dataTables_wrapper .dataTables_processing,
        [data-theme="dark"] .dataTables_wrapper .dataTables_paginate {
            color: var(--text-muted);
        }

        [data-theme="dark"] .page-link {
            background-color: var(--bg-card);
            border-color: var(--border-color);
            color: var(--text-muted);
        }
    </style>
</head>

<?php
$sub_dir_selected = $_GET['sub_dir'] ?? 'all-agents';
$type_titles = [
    "all-agents" => "All Agents",
    "users-agents" => "Users Agents",
];
?>

<body>
    <script>
        // Apply theme immediately to prevent flicker
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
    </script>

    <div id="loading" class="loading-overlay">
        <div class="spinner-custom"></div>
        <p class="mt-3 font-weight-600 text-muted">Preparing your data...</p>
    </div>

    <!-- Header -->
    <header class="dashboard-header mb-4">
        <div class="container">
            <div class="d-flex flex-column flex-md-row align-items-center justify-content-between gap-3">
                <h1 class="dashboard-title">
                    <i class="fa-solid fa-chart-line"></i>
                    WikiProject Medicine Pageviews
                </h1>

                <div class="d-flex align-items-center gap-3">
                    <button class="theme-toggle" onclick="toggleTheme()" title="Toggle Dark/Light Mode">
                        <i class="fa-solid fa-moon dark-icon"></i>
                        <i class="fa-solid fa-sun light-icon d-none"></i>
                    </button>

                    <form method="get" id="subDirForm" class="m-0">
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
                <h2><i class="fa-solid fa-wave-square me-2" style="color: var(--primary-color)"></i> Global Trends</h2>
                <span class="text-muted small font-weight-500">Total Views by Year</span>
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
                <h2><i class="fa-solid fa-table me-2" style="color: var(--primary-color)"></i> Language Distribution</h2>
                <div class="d-flex gap-2">
                    <span class="badge" style="background: var(--bg-body); border: 1px solid var(--border-color); color: var(--text-muted);">
                        <i class="fa-solid fa-globe me-1"></i> Data aggregated
                    </span>
                </div>
            </div>
            <div class="card-body-premium">
                <div class="table-responsive">
                    <table id="mainTable" class="table table-premium w-100">
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
        const subDirSelected = <?= json_encode($sub_dir_selected) ?>;

        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';

            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcons(newTheme);

            // Reload chart to update colors
            if (window.myChart) {
                window.myChart.destroy();
                loadChart(subDirSelected);
            }
        }

        function updateThemeIcons(theme) {
            const moon = document.querySelector('.dark-icon');
            const sun = document.querySelector('.light-icon');
            if (theme === 'dark') {
                moon.classList.add('d-none');
                sun.classList.remove('d-none');
            } else {
                moon.classList.remove('d-none');
                sun.classList.add('d-none');
            }
        }

        // Initialize icons on load
        updateThemeIcons(localStorage.getItem('theme') || 'light');

        async function loadChart(subDir) {
            try {
                const response = await fetch(`api.php?chart_data=1&sub_dir=${subDir}`);
                const res = await response.json();

                const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
                const textColor = isDark ? '#94a3b8' : '#64748b';
                const gridColor = isDark ? 'rgba(51, 65, 85, 0.5)' : '#f1f5f9';

                const ctx = document.getElementById('viewsChart').getContext('2d');

                // Create gradient
                const gradient = ctx.createLinearGradient(0, 0, 0, 400);
                gradient.addColorStop(0, 'rgba(79, 70, 229, 0.4)');
                gradient.addColorStop(1, 'rgba(79, 70, 229, 0)');

                window.myChart = new Chart(ctx, {
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
                            pointBackgroundColor: isDark ? '#1e293b' : '#fff',
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
                                backgroundColor: isDark ? '#0f172a' : '#1e293b',
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
                                    color: gridColor
                                },
                                ticks: {
                                    color: textColor,
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
                                    color: textColor,
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

        async function loadTable(subDir) {
            try {
                const response = await fetch(`api.php?sub_dir=${subDir}`);
                const res = await response.json();

                if (res.error) {
                    alert(res.error);
                    return;
                }

                const columns = [{
                        data: 'index',
                        title: '#'
                    },
                    {
                        data: 'lang',
                        title: 'Lang',
                        render: function(data, type, row) {
                            if (row.is_summary) return `<strong>Global</strong>`;
                            return `<span class="badge-lang">${data}</span>`;
                        }
                    },
                    {
                        data: 'titles',
                        title: 'Articles',
                        render: function(data, type, row) {
                            const val = Number(data).toLocaleString();
                            if (row.is_summary) return `<strong>${val}</strong>`;
                            return `<a href='langs.php?lang=${row.lang}&sub_dir=${subDirSelected}'>${val} <i class="fa-solid fa-arrow-up-right-from-square ms-1 small"></i></a>`;
                        }
                    }
                ];

                res.years.forEach(year => {
                    columns.push({
                        data: year,
                        title: String(year),
                        render: function(data, type, row) {
                            const val = Number(data).toLocaleString();
                            return row.is_summary ? `<strong>${val}</strong>` : val;
                        }
                    });
                });

                columns.push({
                    data: 'total',
                    title: 'Total View',
                    render: function(data, type, row) {
                        const val = Number(data).toLocaleString();
                        return row.is_summary ? `<strong>${val}</strong>` : `<strong>${val}</strong>`;
                    }
                });

                $('#mainTable').DataTable({
                    data: res.data,
                    columns: columns,
                    paging: true,
                    pageLength: 25,
                    lengthChange: false,
                    searching: true,
                    order: [
                        [0, 'asc']
                    ],
                    dom: '<"d-flex justify-content-between align-items-center mb-3"f>rtip',
                    language: {
                        search: "",
                        searchPlaceholder: "Search languages...",
                        paginate: {
                            previous: '<i class="fa-solid fa-chevron-left"></i>',
                            next: '<i class="fa-solid fa-chevron-right"></i>'
                        }
                    },
                    columnDefs: [{
                        targets: 0,
                        width: "40px"
                    }],
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
            const subDir = '<?= $sub_dir_selected ?>';

            await Promise.all([
                loadChart(subDir),
                loadTable(subDir)
            ]);

            $('#loading').fadeOut(600);
        });
    </script>
</body>

</html>
