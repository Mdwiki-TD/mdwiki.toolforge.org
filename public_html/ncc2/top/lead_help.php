<?PHP
namespace LeadHelp;
use function Functions\make_target_url;
use function Functions\make_view_by_number;

if (isset($_GET['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};

function make_table_lead($lang) {
    global $langs_to_titles, $langs_to_titles_views;

    $sato = <<<HTML
        <table class='table table-striped compact soro'>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Title</th>
                    <th>Views</th>
                </tr>
            </thead>
            <tbody>
        HTML;
    // Generate and sort the table of  for the specified language
    $dd = $langs_to_titles[$lang] ?? [];
    krsort($dd);

    $views_tab = $langs_to_titles_views[$lang] ?? [];
    $noo = 0;
    foreach ( $dd AS $tat => $title ) {

        $noo += 1;
        $title_url = make_target_url($title, $lang);

        $views   = $views_tab[$title] ?? "?";
        $views_url = make_view_by_number($title, $views, $lang);

        $laly = <<<HTML
            <tr class='filterDiv show2'>
                <th data-content="#">$noo</th>
                <td data-content="Title">$title_url</td>
                <td data-content='Views'>$views_url</td>
            </tr>
            HTML;

        $sato .= $laly;

    };

    $sato .= <<<HTML
        </tbody>
    </table>
    HTML;

    return $sato;

};
