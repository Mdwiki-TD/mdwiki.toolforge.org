<?PHP
//---
if (isset($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};
//---
require 'leader_tables.php';
//---
function print_cat_table(): string {
    global $sql_users_tab, $Articles_numbers, $Words_total, $sql_Languages_tab, $global_views;
    //---
    $numbersTable = createNumbersTable();
    $numbersCol   = makeColSm4('Numbers', $numbersTable, $numb = '3');
    //---
    // $usersTable   = makeUsersTable();
    // $usersCol     = makeColSm4('Top Translators', $usersTable, $numb = '5');
    $usersCol     = '';

    $languagesTable = makeLangTable();
    $languagesCol = makeColSm4('Top Languages', $languagesTable, $numb = '6');
    //---
    return <<<HTML
        <span align="center">
            <h3>Leaderboard</h3>
        </span>
        <div class="row">
            $numbersCol
            <!-- $usersCol -->
            $languagesCol
        </div>
    HTML;
}
//---
$uux = print_cat_table();
//---
echo <<<HTML
<style>
    .table>tbody>tr>td,
    .table>tbody>tr>th,
    .table>thead>tr>td,
    .table>thead>tr>th {
        padding: 6px;
        line-height: 1.42857143;
        vertical-align: top;
        border-top: 1px solid #ddd;
    }
</style>
<div class="container-fluid">
    $uux
</div>
HTML;
//---
?>