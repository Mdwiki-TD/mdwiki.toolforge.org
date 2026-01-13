<?php

if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

function render_total_by_year($years_data): array
{
    $total_by_year = [];
    foreach ($years_data as $year => $data) {
        // sum all data values for this year
        $y_count =  0;
        foreach ($data as $lang => $count) {
            $y_count += $count;
        }
        $total_by_year[$year] = $y_count;
    }
    return $total_by_year;
}
function make_chart_script($labels, $data_values): string
{

    return <<<HTML
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            new Chart(document.getElementById('viewsChart'), {
                type: 'line',
                data: {
                    labels: $labels,
                    datasets: [{
                        label: 'Total Views by Year',
                        data: $data_values,
                        borderColor: '#007bff',
                        backgroundColor: 'rgba(0, 123, 255, 0.1)',
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: true }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        });
    </script>
    HTML;
}

function build_card_with_table(string $title, string $table_html, string $extra_classes = ''): string
{
    return <<<HTML
        <div class="card $extra_classes">
            <div class="card-header">
                <span class="card-title h2">$title</span>
                <div class="card-tools">
                    <button type="button" class="btn-tool" data-card-widget="collapse">
                        <i class="fas fa-minus"></i>
                    </button>
                </div>
            </div>
            <div class="card-body">
                $table_html
            </div>
        </div>
    HTML;
}
