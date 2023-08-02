<?php
// Import required files and functions
require('lead_help.php');
require('leader_tables.php');

/**
 * Build and return an HTML string which represents a table with categories,
 * specified by the provided language.
 *
 * @return string The generated HTML string.
 */
function print_cat_table_lang(): string {
    $numbersTable = createNumbersTable();
    $numbersCol = makeColSm4('Numbers', $numbersTable, $numb = '3');
    $usersTable = makeUsersTable();
    $usersCol   = makeColSm4('Top Translators', $usersTable, $numb = '6');

    return <<<HTML
        <div class="row">
            $numbersCol
            $usersCol
        </div>
    HTML;
}

// Get the main language from the request or use an empty string as default
$mainlang = $_REQUEST['lang'] ?? '';
$mainlang = rawurldecode(str_replace('_', ' ', $mainlang));

// Get the language name from the code_to_lang array or use the main language code
$langname = $code_to_lang[$mainlang] ?? $mainlang;

// Generate and sort the table of translations for the specified language
$dd = $translates_by_lang[$mainlang]['titles'];
krsort($dd);
$tat = make_table_lead($dd, $lang = $mainlang);

// Generate the category table HTML for the main language
$tablex = print_cat_table_lang($mainlang);

// Display the HTML output
echo <<<HTML
<div class='row content'>
    <div class='col-md-4'></div>
    <div class='col-md-4'><h2 class='text-center'>Language: $mainlang</h2></div>
    <div class='col-md-4'></div>
</div>
$tablex
<hr>
<div class='card'>
    <div class='card-body' style='padding:5px 0px 5px 5px;'>
    $tat
    </div>
</div>
HTML;
?>
