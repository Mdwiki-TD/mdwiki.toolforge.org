<?PHP
namespace LeaderGraph;

if (isset($_GET['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};

//---
echo '
<script src="/Translation_Dashboard/js/g.js"></script>';
//---
function print_graph() {
	global $langs_count_files;
    //---
    $ms = array_keys($langs_count_files);
    $cs = array_values($langs_count_files);
    //---
    $ms = json_encode($ms);
    $cs = json_encode($cs);
    //---
    $graph =  <<<HTML
        <div class="card">
            <div class="card-header aligncenter" style="font-weight:bold;">
            </div>
            <div class="card-body">
                <div class="position-relative mb-4">
                    <canvas id="chart12" height="200"></canvas>
                </div>
            </div>
        </div>
        <script>
            graph_js(
                $ms,
                $cs,
                "chart12"
            )
        </script>
    HTML;
    return $graph;
}

function print_graph_tab() {
    $g = print_graph();
    echo <<<HTML
        <div class="container">
            <div class="col-md-10">
                $g
            </div>
        </div>
    HTML;
}
//---
if (isset($_GET['x'])) {
    print_graph();
}
//---
