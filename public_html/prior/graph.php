<?PHP
namespace LeaderGraph;
//---
require_once('tables.php');
//---
echo '<script src="/Translation_Dashboard/js/g.js"></script>';
//---
function print_graph() {
	global $top_langs;
    //---
    $ms = array_keys($top_langs);
    $cs = array_values($top_langs);
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
if (isset($_REQUEST['x'])) {
    print_graph_tab();
}
//---
?>