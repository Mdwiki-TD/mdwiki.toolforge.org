<?php
namespace TopLangs;
use function LeadHelp\make_table_lead;
// use function Functions\ColSm;
// use function LeaderTables\NumbsTableNew;

if (isset($_GET['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};



function LangTable($mainlang): string {
    global $langs_count_files, $langs_count_views;

    // Define the keys that should be skipped
    $total_views = number_format($langs_count_views[$mainlang] ?? 0);
    $total_Articles = number_format($langs_count_files[$mainlang] ?? 0);
    
    $table1 = <<<HTML
            <!-- <table class='table table-sm table-striped' style='width:70%;'> -->
            <table class="table table-striped table-sm">
            <tr><td><b>Views: </b></td><td><span id='hrefjsontoadd'>$total_views</span></td></tr>
            <tr><td><b>Files: </b></td><td><span id='all_files'>$total_Articles</span></td></tr>
            </table>
        HTML;
    //---
    return $table1;
};

function make_lang_tab($mainlang): void {

    $tat = make_table_lead($mainlang);

    // Generate the category table HTML for the main language
    $Numbs = LangTable($mainlang);
    // Display the HTML output
    echo <<<HTML
        <div class='container'>
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
        </div>
    HTML;
}
?>
