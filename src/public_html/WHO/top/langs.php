<?php
namespace TopLangs;
use function LeadHelp\make_table_lead;
use function Functions\ColSm;
use function LeaderTables\NumbsTableNew;
use function LeaderTables\UsersTableNew;
use function LeaderTables\UsersTableTarget;


function LangTable($mainlang): string {
    global $titles_by_lang;
    $numbers = [
        'Views' => $titles_by_lang[$mainlang]['views'],
        'Articles' => count($titles_by_lang[$mainlang]['titles']),
    ];    
    // Initialize the HTML string with the table header
    $Numbers_table = <<<HTML
    <table class="table table-striped table-sm">
    <thead>
    </thead>
    <tbody>
    HTML;

    // Define the keys that should be skipped
    $skip_keys = ['Languages'];

    // Loop through each key-value pair in the numbers array
    foreach ($numbers as $key => $value) {

        // If the key is one of the skipped keys and $mainlang is not an empty string, continue to the next iteration
        // This effectively skips the current key-value pair and goes to the next one.
        if (in_array($key, $skip_keys) && $mainlang !== '') {
            continue;
        }

        // if (in_array($key, $skip_keys) && $mainlang !== '') {

        // if type is array then count
        // if (is_array($value)) $value = count($value);

        // Format the value as a number
        // This adds commas as thousands separators for readability
        $value = number_format($value);

        // Add a new row to the table for the current key-value pair
        $Numbers_table .= <<<HTML
        <tr>
            <td><b>$key</b></td>
            <td>$value</td>
        </tr>
    HTML;
    }

    // Close the table body and the table itself
    $Numbers_table .= <<<HTML
    </tbody>
    </table>
    HTML;

    // Return the resulting HTML string
    return $Numbers_table;
};

function make_lang_tab(): void {
    global $titles_by_lang;

    // Get the main language from the request or use an empty string as default
    $mainlang = $_REQUEST['lang'] ?? '';

    // Generate and sort the table of  for the specified language
    $dd = $titles_by_lang[$mainlang]['titles'];
    krsort($dd);
    $tat = make_table_lead($dd, $lang = $mainlang);

    // Generate the category table HTML for the main language
    $Numbs = LangTable($mainlang);
    // Display the HTML output
    echo <<<HTML
    <div class='row content'>
        <div class='col-md-3'>$Numbs</div>
        <div class='col-md-5'><h2 class='text-center'>Language: $mainlang</h2></div>
        <div class='col-md-4'></div>
    </div>
    <div class='card'>
        <div class='card-body' style='padding:5px 0px 5px 5px;'>
        $tat
        </div>
    </div>
    HTML;
}
?>
