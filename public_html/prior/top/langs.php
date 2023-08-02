<?PHP

require('lead_help.php');

$test = $_REQUEST['test'] ?? '';
$mainlang = $_REQUEST['lang'] ?? '';
$mainlang = rawurldecode( str_replace ( '_' , ' ' , $mainlang ) );

require 'leader_tables.php';

function print_cat_table_lang(): string {
    
    global $mainlang;
    
    $numbersTable = createNumbersTable();
    $numbersCol   = makeColSm4('Numbers', $numbersTable, $numb = '3');
    
    $usersTable   = makeUsersTable();
    $usersCol     = makeColSm4('Top Translators', $usersTable, $numb = '6');
    
    return <<<HTML
        <div class="row">
            $numbersCol
            $usersCol
        </div>
    HTML;
}

$langname = $code_to_lang[$mainlang] ?? $mainlang;

$dd = $translates_by_lang[$mainlang]['titles'];

krsort($dd);

$tat = make_table_lead($dd, $lang=$mainlang);

$tablex = print_cat_table_lang();

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

