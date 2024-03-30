<?php
namespace TopLangs;
use function LeadHelp\make_table_lead;
use function Functions\ColSm;
use function LeaderTables\NumbsTableNew;


function LangTable($mainlang): string {
    global $titles_by_lang;

    // Define the keys that should be skipped
    $total_views = $titles_by_lang[$mainlang]['views'];
    $total_Articles = count($titles_by_lang[$mainlang]['titles']);
    
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
