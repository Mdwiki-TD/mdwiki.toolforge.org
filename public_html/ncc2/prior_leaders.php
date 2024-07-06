<?PHP

namespace LeaderTables;
use function Functions\make_target_url;

if (isset($_GET['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};

function NumbsTableNew(): string
{
    global $numbers;

    $Files = number_format($numbers['Files']);
    $Languages = number_format($numbers['Languages']);
    $Views = number_format($numbers['Views']);
    // Initialize the HTML string with the table header
    $Numbers_table = <<<HTML
    <table class="datatable table table-striped table-sm">
        <thead>
            <tr>
                <th class="spannowrap">Type</th>
                <th>Number</th>
            </tr>
        </thead>
        <tbody>
            <tr><td><b>Files</b></td><td><span id="all_files">$Files</span></td></tr>
            <tr><td><b>Languages</b></td><td><span id="all_langs">$Languages</span></td></tr>
            <tr><td><b>Views</b></td><td><span id="all_views">$Views</span></td></tr>
        </tbody>
    </table>
    HTML;

    // Return the resulting HTML string
    return $Numbers_table;
};

function LangsTableNew($cat): string
{
    global $langs_count_views, $langs_count_files;
    // Sort the array in reverse order by value
    arsort($langs_count_files);
    // Initialize the HTML text for the table with headers
    $text = <<<HTML
        <table class='sortable table table-striped table-sm'>
        <thead>
            <tr>
                <th>#</th>
                <th class='spannowrap'>Language</th>
                <th>Cat</th>
                <th>Files</th>
                <th>Views</th>
            </tr>
        </thead>
        <tbody>
    HTML;

    // Initialize row number
    $numb = 0;
    // Loop through each language in the array
    foreach ($langs_count_files as $langcode => $comp) {
        // Get the Files numbers, words and views
        $views = number_format($langs_count_views[$langcode] ?? 0);

        // Only add a table row if there are Files for this language
        // if ( $comp > 0 ) {
        $numb++;
        $url = "index.php?lang=$langcode&cat=$cat";
        // Add a table row with the language details
        $trarget = make_target_url("Category:$cat", $langcode, $name = 'Category');
        $viewsurl = "<a target='_blank' href='https://pageviews.wmcloud.org/massviews/?platform=all-access&agent=all-agents&source=category&range=all-time&subjectpage=0&subcategories=0&sort=views&direction=1&view=list&target=https://af.wikipedia.org/wiki/Category:$cat'>$views</a>";
        $text .= <<<HTML
                <tr>
                    <td>$numb</td>
                    <td><a href='$url'>$langcode</a></td>
                    <td>$trarget</td>
                    <td>$comp</td>
                    <td>$viewsurl</td>
                </tr>
            HTML;
        // };
    };

    // Close the table body and table tags in the HTML
    $text .= <<<HTML
        </tbody>
        </table>
    HTML;

    // Return the HTML text
    return $text;
}
