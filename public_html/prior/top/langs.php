<?php

namespace TopLangs;

use function LeadHelp\make_table_lead;
use function Functions\ColSm;
use function Functions\makeColSm4;
use function LeaderTables\NumbsTableNew;
use function LeaderTables\UsersTableNew;
use function LeaderTables\module_copy;
// include_once 'tables.php';
/**
 * Build and return an HTML string which represents a table with categories,
 * specified by the provided language.
 *
 * @return string The generated HTML string.
 */
function print_cat_table_lang(): string
{
    $numbersTable = NumbsTableNew();
    $numbersCol = ColSm('Numbers', $numbersTable);
    // ---
    $copy_module = module_copy();

    $modal_a = <<<HTML
        <button type="button" class="btn-tool" href="#" data-bs-toggle="modal" data-bs-target="#targets">
            <i class="fas fa-copy"></i>
        </button>
    HTML;
    //---
    $usersTable = UsersTableNew();
    $usersCol = makeColSm4('Top Translators', $usersTable, 5, $table2 = $copy_module, $title2 = $modal_a);
    // ---
    return <<<HTML
        <div class="row">
            <div class="col-md-4">
                $numbersCol
            </div>
            <div class="col-md-8">
                $usersCol
            </div>
        </div>
    HTML;
}

function make_lang_tab(): void
{
    global $translates_by_lang;

    // Get the main language from the request or use an empty string as default
    $mainlang = $_REQUEST['lang'] ?? '';

    // Generate and sort the table of translations for the specified language
    $dd = $translates_by_lang[$mainlang]['titles'];
    krsort($dd);
    $tat = make_table_lead($dd, $lang = $mainlang);

    // Generate the category table HTML for the main language
    $tablex = print_cat_table_lang();

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
        <div class='card-header'>
            <h3 class='card-title text-center'>Translations</h3>
        </div>
        <div class='card-body' style='padding:5px 0px 5px 5px;'>
        $tat
        </div>
    </div>
    HTML;
}
