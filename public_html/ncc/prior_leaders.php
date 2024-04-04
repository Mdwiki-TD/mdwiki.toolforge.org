<?PHP

namespace LeaderTables;

include_once('tables.php');

$mainlang = $_GET['lang'] ?? '';
$cat = $_GET['cat'] ?? 'Files_imported_from_NC_Commons';

function NumbsTableNew(): string
{
    global $numbers, $mainlang;

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

function LangsTableNew(): string
{
    global $titles_by_lang, $cat;
    // Sort the array in reverse order by value
    arsort($titles_by_lang);
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
    foreach ($titles_by_lang as $langcode => $table) {
        // Get the Files numbers, words and views
        $comp  = count($table['titles']);
        $views = number_format($table['views']);

        // Only add a table row if there are Files for this language
        // if ( $comp > 0 ) {
        $numb++;
        $url = "index.php?lang=$langcode";
        if ($cat !== '') {
            $url .= "&cat=$cat";
        }
        // Add a table row with the language details
        $text .= <<<HTML
                <tr>
                    <td>$numb</td>
                    <td><a href='$url'>$langcode</a></td>
                    <td><a href='https://$langcode.wikipedia.org/wiki/$cat'>Category</a></td>
                    <td>$comp</td>
                    <td>$views</td>
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
