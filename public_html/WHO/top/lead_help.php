<?PHP

namespace LeadHelp;

use function Functions\make_target_url;
use function Functions\make_mdwiki_title;
use function Functions\make_view_by_number;

function make_table_lead($dd, $lang = '')
{

    global $md_titles_to_cat;

    $sato = <<<HTML
        <table class='table table-striped compact soro table-mobile-responsive table-mobile-sided'>
            <thead>
                <tr>
                    <th>#</th>
                    <th>MDtitle</th>
                    <th>Title</th>
                    <!-- <th>Section</th> -->
                    <th>Views</th>
                </tr>
            </thead>
            <tbody>
        HTML;


    $noo = 0;
    foreach ($dd as $tat => $tabe) {

        $noo += 1;

        $mdtitle = $tabe['mdtitle'] ?? "";
        $nana = make_mdwiki_title($mdtitle);

        $section = $md_titles_to_cat[$mdtitle] ?? '';

        $title = $tabe['title'] ?? "";
        $title_url = make_target_url($title, $lang);

        $views   = number_format($tabe['views']);
        $views_url = make_view_by_number($title, $views, $lang);

        $laly = <<<HTML
            <tr class='filterDiv show2'>
                <th data-content="#">$noo</th>
                <td data-content="MDtitle">$nana</td>
                <td data-content="Title">$title_url</td>
                <!-- <td data-content="Section">$section</td> -->
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
