<?PHP
namespace LeadHelp;

use function Functions\make_target_url;
use function Functions\make_mdwiki_title;
use function Functions\make_view_by_number;

function make_table_lead($dd, $lang='') {

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


    $noo = 0;
    foreach ( $dd AS $tat => $tabe ) {

        $noo += 1;

        $title = $tabe['title'];
        $title_url = make_target_url($title, $lang);

        $views   = $tabe['views'] ?? "?";
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
